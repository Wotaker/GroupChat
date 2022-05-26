import time
import pandas as pd
import numpy as np
import os
from queue import Queue

from src.messenger_resources import DataBase, MsgBuffer
from gen.chat_pb2 import Message, MIME as Mime


def random_msg() -> Message:
    mime = Mime(type="image", subtype="jpeg", data=bytes(np.random.bytes(10)))
    return Message(
        sender_id=np.random.randint(1, 10),
        group_id=np.random.randint(1, 5),
        priority=np.random.randint(1, 4),
        text="Sample Msg",
        mime=mime,
        citation_id=np.random.randint(1, 100)
    )



def test_database():

    print("=== Database test ===\n")

    db = DataBase()
    db.add(1, "3001", 1234)
    db.add(3, "3003", 0)
    print(db.exists(2))
    print(db.add_subscribtion(3, 1234))
    db.add(20, "3020", 0)
    print(db.delete(4))
    db.show(sep=True)
    print(db.db.dtypes)

    print("  Saving db...")
    time.sleep(1)
    db.backup()
    print("Saved")

    print("  Loading backuped db...")
    db2 = DataBase()
    db2.show(sep=True)
    
    print(type(db2.db.loc[20, "Port"]), db2.db.loc[20, "Port"])
    


def test_buffer():
    print("=== Buffer test ===\n")
    buf = MsgBuffer()
    buf.put(1, random_msg())
    buf.put(1, random_msg())
    buf.put(1, random_msg())
    buf.put(3, random_msg())


if __name__ =="__main__":
    test_database()
    # try:
    #     db = pd.read_csv("..\\resources\\clients_table.csv").set_index("Id")
    # except FileNotFoundError:
    #     print("Unable to load Database!")
    # print(db)
    # try:
    #     db.to_csv("dupa\\dupa.csv")
    # except OSError:
    #     print("Dir does not exists!")

    # resources_dir = os.path.join(
    #     os.path.dirname(os.path.abspath(__file__)),
    #     os.path.pardir,
    #     'resources'
    # )
    # print(os.listdir(resources_dir))
    # print(os.path.dirname(os.path.abspath(__file__)))

