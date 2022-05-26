import os
import numpy as np
import pandas as pd
from queue import Queue

from gen.chat_pb2 import Message


NONE_GROUP_ID = 0


class DataBase():

    def __init__(self, name="clients_table") -> None:
        
        # Name of the database
        self.name: str = name

        # Path to the backup csv file where the database is stored
        self.resources_dir: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.pardir,
            'resources'
        )
        self.save_path: str = os.path.join(self.resources_dir, f"{name}.csv")

        # The database is build on top of pandas DataFrame
        if not self.load():
            print(f"[Info] No backup {name} database found. Creating empty one.")
            self.db: pd.DataFrame = pd.DataFrame({
                'Id': pd.Series(dtype='int'),
                'Nick': pd.Series(dtype='str'),
                'Port': pd.Series(dtype='str'),
                'GroupId': pd.Series(dtype='int')
            }).set_index("Id")
    

    def exists(self: object, id: int) -> bool:
        """checks if client with given id is in database"""

        return id in self.db.index.to_list()


    def add(self: object, nick: str, port: str, group_id: int) -> int:
        """adds new client to the client table"""

        id = self.db.last_valid_index()
        id = 1 if id is None else id + 1
        self.db.loc[id] = [nick, port, group_id]
        return id


    def delete(self: object, id: int) -> bool:
        """deletes client with given id, returns True on success, False otherwise"""

        if not self.exists(id):
            return False
        self.db.drop([id], inplace=True)
        return True


    def add_subscribtion(self: object, id: int, group_id: int) -> bool:
        """adds sbscribed group for a client with given id, or modifies subscribtion if present.
        Returns False if there is no client with given id, otherwise returns True"""

        if self.exists(id):
            self.db.loc[(id, "GroupId")] = group_id
            return True
        return False

    
    def backup(self: object) -> bool:
        """saves the database to a backup csv file. Returns True if succeeded, 
        False otherwise"""

        try:
            self.db.to_csv(self.save_path)
        except OSError:
            print(f"[Error] Unable to backup {self.name} database!")
            return False
        return True
    

    def load(self: object) -> bool:
        """loads the database from the backup csv file. 
        Returns True if succeeded, False otherwise"""

        csv_name = f"{self.name}.csv"
        if csv_name not in list(os.listdir(self.resources_dir)):
            return False
        
        try:
            self.db = pd.read_csv(
                self.save_path, converters={'Port': str}
            ).set_index("Id")
            print(self.db.dtypes)
        except FileNotFoundError:
            print(f"[Error] Unable to load backup database from {self.save_path}!")
            return False
        return True


    def show(self: object, sep=False):
        """prints the database"""
        space = "\n" if sep else ""
        print(f"{space}{self.db}{space}")


class MsgBuffer():

    def __init__(self: object) -> None:
        self.buffer = dict()


    def put(self: object, id: int, msg: Message):
        """Add message to the buffer of client with given id"""
        
        if not (id in self.buffer.keys()):
            self.buffer[id] = Queue()
        self.buffer[id].put(msg)
    

    def get(self: object, id: int) -> Message:
        """gets the next msg in queue from client with given id."""

