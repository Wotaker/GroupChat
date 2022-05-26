from src.messenger_resources import DataBase, MsgBuffer, NONE_GROUP_ID

import grpc
import gen.chat_pb2 as chat_pb2
import gen.chat_pb2_grpc as chat_pb2_grpc


class Messenger(chat_pb2_grpc.MessengerServicer):

    # Initialize Messenger with necessary data structures
    def __init__(self) -> None:
        self.client_table = DataBase(name="clients_table")
        self.msg_buffer = MsgBuffer()

    def Init(self, request, context):

        client_id = self.client_table.add(request.nick, request.port, NONE_GROUP_ID)
        backuped = self.client_table.backup()

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

        success = self.client_table.add_subscribtion(request.client_id, request.group_id)

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
    
    def SendTo(self, request, context):
        group_id = request.group_id



