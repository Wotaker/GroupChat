from src.messenger_resources import DataBase
import time
import os
import numpy as np

def test_database():

    print("=== Database test ===\n")

    db = DataBase()
    id_ola, gr_ola = db.add("ola", 1234)
    id_ula, gr_ula = db.add("ula", 0)
    id_ola_v2, gr_ola_v2 = db.add("ola", 0)

    assert id_ola == id_ola_v2
    assert gr_ola == gr_ola_v2
    assert gr_ola_v2 == 1234
    assert db.db.shape == (2, 2)

    assert db.exists_by_id(2)
    assert db.exists_by_nickname("ola")
    assert not db.exists_by_nickname("Zbych")

    assert db.add_subscribtion(2, 1234)
    
    db.add("ela", 0)

    group_1234 = db.get_subscribers(1234)
    print(f"group 1234 subscribers: {group_1234}")
    assert group_1234 == [id_ola, id_ula]
    assert db.get_subscribers(999) == []

    assert not db.delete(4)     # deleting unexisting client results in false
    assert db.delete(2)
    db.show(sep=True)
    print(db.db.dtypes)

    print("  Saving db...")
    time.sleep(1)
    db.backup()
    print("Saved")

    print("  Loading backuped db...")
    db2 = DataBase()
    db2.show(sep=True)
    
    print("Removing database csv file...")
    time.sleep(1)
    os.remove(db.save_path)

    print("\nAll tests passed!")

def prototype():
    db = DataBase()
    id_ola, _ = db.add("ola", 1234)
    id_ula, _ = db.add("ula", 0)
    db.show()

    print(db.db.index[db.db["Nick"] == "ula"].to_list()[0])

if __name__ == "__main__":
    test_database()
    # prototype()
