import sqlite3
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
import pyautogui
import ctypes
import pickle

# ArduinoSerial = serial.Serial('com4', 9600)  # Create Serial port object called arduinoSerialData
# time.sleep(2)  # wait for 2 seconds for the communication to get established

db = sqlite3.connect('server1.db')
sql = db.cursor()


def startup():
    sql.execute("""CREATE TABLE IF NOT EXISTS users (
         id  INTEGER PRIMARY KEY AUTOINCREMENT, 
         login TEXT,
         password TEXT,
         id_version INT,
         FOREIGN KEY(id_version) REFERENCES version(id)
    )""")

    sql.execute("""CREATE TABLE IF NOT EXISTS version (
             id  INTEGER PRIMARY KEY AUTOINCREMENT, 
             name TEXT
        )""")

    sql.execute("""CREATE TABLE IF NOT EXISTS func (
                 id  INTEGER PRIMARY KEY AUTOINCREMENT, 
                 name_func TEXT
            )""")

    sql.execute("""CREATE TABLE IF NOT EXISTS versions_func (
                 func_id INT,
                 version_id INT,
                 FOREIGN KEY(version_id) REFERENCES version(id),
                 FOREIGN KEY(func_id) REFERENCES func(id)
            )""")
    db.commit()


    #for value in sql.execute("SELECT * FROM datch"):
     #   print(value)

def servis():
    sql.execute(f"INSERT INTO version(id, name) VALUES (?, ?)", (1, 'one'))
    sql.execute(f"INSERT INTO version(id, name) VALUES (?, ?)", (2, 'two'))
    sql.execute(f"INSERT INTO version(id, name) VALUES (?, ?)", (3, 'three'))
    db.commit()


def func():
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (1, 'down'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (2, 'high'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (3, 'left'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (4, 'right'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (5, 'click'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (6, 'center'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (7, 'Play/Pause'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (8, 'Vdown'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (9, 'Vup'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (10, 'language'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (11, 'Rewind'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (12, 'Forward'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (13, 'Win+d'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (14, 'ctrl+z'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (15, 'click_r'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (16, 'Sdown'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (17, 'Sup'))
    sql.execute(f"INSERT INTO func(id, name_func) VALUES (?, ?)", (18, 'ctrl+alt+delete'))
    db.commit()


def sers_func():
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (7, 1))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (8, 1))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (9, 1))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (11, 1))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (12, 1))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (1, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (2, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (3, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (4, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (5, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (6, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (10, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (13, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (14, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (15, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (16, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (17, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (18, 2))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (1, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (2, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (3, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (4, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (5, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (6, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (7, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (8, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (9, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (10, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (11, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (12, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (13, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (14, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (15, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (16, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (17, 3))
    sql.execute(f"INSERT INTO versions_func (func_id, version_id) VALUES (?, ?)", (18, 3))
    db.commit()


