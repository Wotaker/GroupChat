from src.messenger_resources import DataBase, MsgBuffer, NONE_GROUP_ID

import grpc
import gen.group_chat_pb2 as chat_pb2
import gen.group_chat_pb2_grpc as chat_pb2_grpc
from threading import Lock

CLIENT_TABLE = DataBase(name="clients_table")
LOCK_TABLE = Lock()

MSG_BUFFER = MsgBuffer()
LOCK_BUFFER = Lock()


class Messenger(chat_pb2_grpc.MessengerServicer):

    # Initialize Messenger with necessary data structures
    def __init__(self) -> None:
        print("[Info] Server Initialized")

    def Init(self, request, context):

        with LOCK_TABLE:
            client_id = CLIENT_TABLE.add(request.nick, request.port, NONE_GROUP_ID)
            backuped = CLIENT_TABLE.backup()

        if not backuped:
            return chat_pb2.InitStatus(
                code=1,
                new_id=client_id,
                details="Client has not been backuped in the client table"
            )
        
        return chat_pb2.InitStatus(
            code=0,
            new_id=client_id,
            details="Backuped successfully"
        )
    
    def JoinGroup(self, request, context):

        with LOCK_TABLE:
            success = CLIENT_TABLE.add_subscribtion(request.client_id, request.group_id)

        if not success:
            return chat_pb2.Status(
                code=1,
                details=f"Unable to add client '{request.client_id}' to the " +\
                    f"subscribtion group '{request.group_id}'. Client " +\
                    f"'{request.client_id}' does not exist"
            )
        
        return chat_pb2.InitStatus(
            code=0,
            details=f"Client {request.client_id} successfully added to the " +\
                f"{request.group_id} subscribtion group"
        )
    
    def Listen(self, request_iterator, context):

        # Exiting this loop means that we have lost connection with a client
        while True:
            for listen_status in request_iterator:
                served_client = listen_status.client_id
                if not listen_status.confirm:
                    print(f"[Warning] Listen-status from client {served_client} did not confirmed")
                
                # if there are any messages for the client, send those
                with LOCK_BUFFER:
                    potential_msg = MSG_BUFFER.get(served_client)
                    while potential_msg is not None:
                        yield potential_msg
                        potential_msg = MSG_BUFFER.get(served_client)
    



