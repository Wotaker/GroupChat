from src.chat_server import PORT_NUMBER
from src.messenger_resources import MsgHistory
import gen.group_chat_pb2 as chat_pb2
import gen.group_chat_pb2_grpc as chat_pb2_grpc

import grpc
import threading
from tkinter import *
from tkinter import simpledialog
import re

TXT = 1
SUB = 2
CIT = 3


class Client():

    def __init__(self, nickname: str, window) -> None:        
        
        # Create a gRPC channel and stub
        channel = grpc.insecure_channel(f'localhost:{PORT_NUMBER}')
        self.connection = chat_pb2_grpc.MessengerStub(channel)

        # Inform the server that the client is up

            # Create ClientInfo init msg
        self.client_info = chat_pb2.ClientInfo(nickname=nickname)
        print("[Info] Sending Init message to server with client info")

            # Wait for server status respons and print the status when recived
        init_status = self.connection.Init(self.client_info)
        print(f"[Info] Initialization status code: {init_status.code}")
        print(f"[Info] Initialization details: {init_status.details}")

            # Assign client id designated by server, set client nickname, and default group
        self.id = init_status.new_id
        self.nickname = nickname
        self.subscribtion_group = init_status.new_group_id

        # Create the msg history
        self.history = MsgHistory()

        # Create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

        # The frame to put ui components on
        self.window = window
        self.__setup_ui()
        self.window.mainloop()
    
    def parse(self, text):
        """
        Parses the text. 
        If SUB -> returns (SUB, subscribtion group).
        If CIT -> returns (CIT, input text with inserted citation).
        If TXT -> returns (TXT, unchanged input text)
        """

        # Search if the input is subscribtion change
        subscribtion = re.findall(r'\$\d+', text)
        if subscribtion:
            return SUB, int(subscribtion[0][1:])
        
        # Search for a citation in text
        citation = re.findall(r'%\d+%', text)
        if citation:
            citation = self.history.get(int(citation[0][1:-1])).text
            citation = f"cite[{citation}]" if citation else ""
            return CIT, re.sub(r'%\d+%', citation, text)

        # Otherwise no special substring present
        return TXT, text
    
    def change_subscribtion(self, new_group_id):
        """
        Informs the Server that a client is changing his subscribtion group
        """
        
        self.subscribtion_group = new_group_id
        join_info = chat_pb2.JoinInfo(client_id=self.id, group_id=new_group_id)
        status = self.connection.JoinGroup(join_info)
        print(f"[Info] Subscribtion change status code: {status.code}")
        print(f"[Info] Subscribtion change details: {status.details}")

        if status.code == 0:
            print(f"[Info] Changing subscribtion group to {new_group_id}")
            self.chat_list.insert(END, f"\n=== Subscribing group nr {new_group_id} ===\n\n")
    
    def __listen_for_messages(self):
        """
        This method runs in separate thread, becouse listening is blocking. It sends listen status
        confirm when ready for new msg. It displays and saves in history recieved msgs.
        """

        def yield_listen_status():
            while True:
                yield chat_pb2.ListenStatus(confirm=True, client_id=self.id)
        
        for msg in self.connection.Listen(yield_listen_status()):
            if self.subscribtion_group != msg.group_id:
                print(f"[Warning] Recieved msg addressed for wrong subscribtion group {msg.group_id}!")
            else:
                print(f"[Info] Recieved msg from {msg.sender_id} ({msg.sender_nickname})")
                msg_id = self.history.put(msg)
                self.chat_list.insert(END, f"{msg_id:03d} | {msg.sender_nickname}: {msg.text}\n")
    
    def send_msg(self, msg):
        """
        Sends the msg to the server and displays it in chat window. Also saves the msg in history
        """

        print("[Info] Sending msg to the server")
        status = self.connection.SendMsg(msg)
        print(f"[Info] Sending status code: {status.code}")
        print(f"[Info] Sending details: {status.details}")

        # If msg delivered successfully, print on screen
        if status.code == 0:
            msg_id = self.history.put(msg)
            self.chat_list.insert(END, f"{msg_id:03d} | You: {msg.text}\n")

    def parse_input(self, event):
        """
        This method is called when user enters something into the textbox
        """

        entry_text = self.entry_message.get()
        self.entry_message.delete(0, END)

        # Return if there is no text in the entry box
        if not entry_text:
            return
        
        parsed = self.parse(entry_text)

        # User entered some plain text -> Create msg and yeld it
        if parsed[0] == TXT or parsed[0] == CIT:
            print("[Info] Plain text entered")
            self.send_msg(chat_pb2.Message(
                sender_id=self.id,
                sender_nickname=self.nickname,
                group_id=self.subscribtion_group,
                priority=0,
                text=parsed[1],
                mime=None,
                citation=""
            ))
        
        # User wants to change subscribtion group
        elif parsed[0] == SUB:
            print(f"[Info] Changing subscribtion to group {parsed[1]}")
            self.change_subscribtion(parsed[1])

    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.nickname)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.parse_input)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)


if __name__ == '__main__':
    root = Tk()
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    nickname = None
    while nickname is None:
        # retrieve a username so we can distinguish all the different clients
        nickname = simpledialog.askstring("Login", "Please enter your login:", parent=root)
    root.deiconify()
    c = Client(nickname, frame)