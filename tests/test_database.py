from src.messenger_resources import DataBase
import time
import os

def test_database():

    print("=== Database test ===\n")

    db = DataBase()
    db.add("ola", "3001", 1234)
    db.add("ula", "3003", 0)
    print(db.exists(2))
    print(db.add_subscribtion(2, 1234))
    db.add("ela", "3020", 0)
    print(not db.delete(4)) # deleting unexisting client results in false
    print(db.delete(2))
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


if __name__ == "__main__":
    test_database()
