from src.chat_server import PORT_NUMBER
from src.messenger_resources import NONE_GROUP_ID
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

def parse(text):

    # Search if the input is subscribtion change
    subscribtion = re.findall(r'\$\d+', text)
    if subscribtion:
        return SUB, int(subscribtion[0][1:])
    
    # Search for a citation in text
    citation = re.findall(r'%\d+%', text)
    if citation:
        return CIT, int(citation[0][1:-1])

    # Otherwise no special substring present
    return TXT, text


class Client():

    def __init__(self, nickname, window) -> None:        
        
        # Create a gRPC channel and stub
        channel = grpc.insecure_channel(f'localhost:{PORT_NUMBER}')
        self.connection = chat_pb2_grpc.MessengerStub(channel)

        # Inform the server that the client is up

            # Create ClientInfo init msg
        self.client_info = chat_pb2.ClientInfo(nickname=self.nickname, port="0000")
        print("[Info] Sending Init message to server with client info")

            # Wait for server status respons and print the status when recived
        init_status = self.connection.Init(self.client_info)
        print(f"[Info] Initialization status code: {init_status.code}")
        print(f"[Info] Initialization details: {init_status.details}")

            # Assign client id designated by server, set client nickname, and default group
        self.id = init_status.new_id
        self.nickname = nickname
        self.subscribtion_group = NONE_GROUP_ID

        # Create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

        # The frame to put ui components on
        self.window = window
        self.__setup_ui()
        self.window.mainloop()
    
    def change_subscribtion(self, new_group_id):
        """
        Informs the Server that a client is changing his subscribtion group
        """
        
        print(f"[Info] Changing subscribtion group to {new_group_id}")
        self.subscribtion_group = new_group_id
        join_info = chat_pb2.JoinInfo(client_id=self.id, group_id=new_group_id)
        status = self.connection.JoinGroup(join_info)
        print(f"[Info] Subscribtion change status code: {status.code}")
        print(f"[Info] Subscribtion change details: {status.details}")
        
    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """

        for msg in self.connection.Listen():
            pass

    def parse_input(self, event):
        """
        This method is called when user enters something into the textbox
        """

        entry_text = self.entry_message.get()

        # Return if there is no text in the entry box
        if not entry_text:
            return
        
        parsed = parse(entry_text)

        # User entered some plain text -> Create msg and yeld it
        if parsed[0] == TXT:
            print("[Info] Plain text entered")

            msg = chat_pb2.Message(
                sender_id=self.id,
                group_id=self.subscribtion_group,
                priority=0,
                text=parsed[1],
                mime=None,
                citation_id=0   # TODO Handle citation. 0 means no citation
            )
        
        # User wants to change subscribtion group
        elif parsed[0] == SUB:
            print(f"[Info] Changing subscribtion to group {parsed[1]}")
            self.change_subscribtion(parsed[1])

        # TODO Handle the citations
        elif parsed[0] == CIT:
            print("[Info] Citation found, unimplemented!")
            pass

    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)
