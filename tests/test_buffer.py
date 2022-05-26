from src.messenger_resources import MsgBuffer
from gen.group_chat_pb2 import Message, MIME as Mime

import numpy as  np


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

def test_buffer():

    print("=== Message Bufffer Test ===\n")
    buf = MsgBuffer()
    buf.put(1, random_msg())
    buf.put(1, random_msg())
    buf.put(2, random_msg())

    msg1_1 = buf.get(1)
    msg1_2 = buf.get(1)

    none_1 = buf.get(1)
    none_2 = buf.get(3)

    assert none_1 is None
    assert none_2 is None
    assert msg1_1 is not None
    assert msg1_2 is not None

    print(msg1_1)
    print(msg1_2)

    print("All tests passed!")

def foo():
    i = 1
    while i < 10:
        yield i
        i += 1

if __name__ == "__main__":
    test_buffer()

    iter = foo()
    print(list(iter))
    