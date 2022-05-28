from src.messenger_resources import DataBase, MsgBuffer, NONE_GROUP_ID
import gen.group_chat_pb2 as chat_pb2
import gen.group_chat_pb2_grpc as chat_pb2_grpc

import grpc
from threading import Lock
from concurrent import futures

CLIENT_TABLE = DataBase(name="clients_table")
LOCK_TABLE = Lock()

MSG_BUFFER = MsgBuffer()
LOCK_BUFFER = Lock()

PORT_NUMBER = 2137


class Messenger(chat_pb2_grpc.MessengerServicer):

    # Initialize Messenger with necessary data structures
    def __init__(self) -> None:
        print("[Info] Server Initialized")

    def Init(self, request, context):

        # Log client initialization
        print(f"[Info] Received Init message from client '{request.nickname}'")

        with LOCK_TABLE:
            client_id, group_id = CLIENT_TABLE.add(request.nickname, NONE_GROUP_ID)
            backuped = CLIENT_TABLE.backup()

        if not backuped:
            return chat_pb2.InitStatus(
                code=1,
                new_id=client_id,
                new_group_id=group_id,
                details="Client has not been backuped in the client table"
            )
        
        return chat_pb2.InitStatus(
            code=0,
            new_id=client_id,
            new_group_id=group_id,
            details="Backuped successfully"
        )
    
    def JoinGroup(self, request, context):

        with LOCK_TABLE:
            success = CLIENT_TABLE.add_subscribtion(request.client_id, request.group_id)
            CLIENT_TABLE.backup()

        if not success:
            return chat_pb2.Status(
                code=1,
                details=f"Unable to add client '{request.client_id}' to the " +\
                    f"subscribtion group '{request.group_id}'. Client " +\
                    f"'{request.client_id}' does not exist"
            )
        
        return chat_pb2.Status(
            code=0,
            details=f"Client {request.client_id} successfully added to the " +\
                f"{request.group_id} subscribtion group"
        )
    
    def Listen(self, request_iterator, context):

        # Exiting this loop means that we have lost connection with a client
        # while True:
        for listen_status in request_iterator:
            served_client = listen_status.client_id
            if not listen_status.confirm:
                print(f"[Warning] Listen-status from client {served_client} did not confirmed")
            
            # if there are any messages for the client, send those
            with LOCK_BUFFER:
                msg = MSG_BUFFER.get(served_client)
                while msg is not None:
                    yield msg
                    msg = MSG_BUFFER.get(served_client)
    
    def SendMsg(self, request, context):

        # Log msg reception
        print(f"[Info] Received message from client {request.sender_id}, addressed to group {request.group_id}")
        
        # Get subscribers of the message target group
        with LOCK_TABLE:
            subscribers = CLIENT_TABLE.get_subscribers(request.group_id)
        
        # Add message to the appropriate message buffers
        with LOCK_BUFFER:
            for client_id in subscribers:
                if request.sender_id != client_id:
                    MSG_BUFFER.put(client_id, request)
        
        return chat_pb2.Status(
            code=0,
            details=f"Message from client {request.sender_id} to " +\
                f"subscribtion group {request.group_id} succesfully delivered"
        )


if __name__ == "__main__":

    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register the server to gRPC
    chat_pb2_grpc.add_MessengerServicer_to_server(servicer=Messenger(), server=server)

    # Assigning port and starting the server
    server.add_insecure_port(f'[::]:{PORT_NUMBER}')
    server.start()
    print("[Info] Server started successfully")

    # Do not exit until the server terminates
    server.wait_for_termination()
