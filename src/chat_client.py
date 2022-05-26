from src.chat_server import PORT_NUMBER
import gen.group_chat_pb2 as chat_pb2
import gen.group_chat_pb2_grpc as chat_pb2_grpc

import grpc
import threading
from tkinter import *
from tkinter import simpledialog


class Client():

    def __init__(self, nickname, window) -> None:

        # Client nickname
        self.nickname = nickname
        
        # Create a gRPC channel and stub
        channel = grpc.insecure_channel(f'localhost:{PORT_NUMBER}')
        self.connection = chat_pb2_grpc.MessengerStub(channel)

        # Create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

        # The frame to put ui components on
        self.window = window
        self.__setup_ui()
        self.window.mainloop()
        
    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """

        pass

    def parse_input(self, event):
        """
        This method is called when user enters something into the textbox
        """

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
