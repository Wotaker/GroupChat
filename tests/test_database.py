from tokenize import group
from src.messenger_resources import DataBase
import time
import os

def test_database():

    print("=== Database test ===\n")

    db = DataBase()
    id_ola = db.add("ola", "3001", 1234)
    id_ula = db.add("ula", "3003", 0)

    assert db.exists(2)
    assert db.add_subscribtion(2, 1234)
    
    db.add("ela", "3020", 0)

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
    
    print(type(db2.db.loc[3, "Port"]), db2.db.loc[3, "Port"])
    
    print("Removing database csv file...")
    time.sleep(1)
    os.remove(db.save_path)

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_database()
