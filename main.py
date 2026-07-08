import sqlite3, os

def db_anlegen(dbname: str):
    dbnamefull = dbname + ".db"
    try:
        os.remove(dbnamefull)
        print(f'Datenbank "{dbnamefull}" gelöscht!')
    except FileNotFoundError:
        print("Datenbank nicht gefunden!")
    db = sqlite3.connect(dbnamefull)
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS telefon (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        telefonnummer TEXT)"""
    cursor.execute(sql)
    db.close()
    print(f'Datenbank "{dbnamefull}" und Tabelle "telefon" erstellt!')

def db_insert(dbname: str, tname: str, ttelefon: str):
    dbnamefull = dbname + ".db"
    db = sqlite3.connect(dbnamefull)
    cursor = db.cursor()
    sql = "INSERT INTO telefon (name, telefonnummer) VALUES (?, ?)"
    cursor.execute(sql, [tname, ttelefon])
    db.commit()
    print(f'Daten eingefügt')
    db.close

def db_show_table(dbname: str, sortby: str):
    dbnamefull = dbname + ".db"
    db = sqlite3.connect(dbnamefull)
    cursor = db.cursor()
    sql = f"SELECT * FROM telefon ORDER BY {sortby}"
    cursor.execute(sql)
    print("|" + "-" * 3 + "|" + "-" * 15 + "|" + "-" * 21 + "|")
    
    for i in cursor:
        print(f"|{i[0]:2} | {i[1]:13} | {i[2]:20}|")
    print("|" + "-" * 3 + "|" + "-" * 15 + "|" + "-" * 21 + "|")

def db_delete_entry(dbname: str, id_to_delete: int):
    dbnamefull = dbname + ".db"
    db = sqlite3.connect(dbnamefull)
    cursor = db.cursor()
    sql = "DELETE FROM telefon WHERE id = ?"
    cursor.execute(sql, [id_to_delete])
    db.commit()
    db.close()


def db_menu():
    dname = input("Datenbanknamen eingeben > ")
    while True:
        print("Hauptmenu")
        print("1. Datenbank und Telefon-Tabelle erstellen/resetten")
        print("2. Eintrag hinzufügen")
        print("3. Tabelle anzeigen")
        print("4. Eintrag Löschen")
        print("5. Datenbank wechseln")
        print("9. Beenden")
        e=int(input("Wählen Sie eine Funktion > "))
        if e==9: break
        elif e==1:
            db_anlegen(dname)
        elif e==2:
            while True:
                n=input("Name (Kein Input um zuück ins Hauptmenü zu gelangen) > ")
                if n=="": break
                t=int(input("Telefonnummer > "))
                db_insert(dname, n, t)
        elif e==3:
            db_show_table(dname, "name")
        elif e==4:
            db_show_table(dname, "id")
            while True:
                i = input("Zu löschende id eingeben (Kein Input um zuück ins Hauptmenü zu gelangen) > ")
                if i == "":
                    break
                i = int(i)
                db_delete_entry(dname, i)
        elif e==5:
            dname = input("Datenbanknamen eingeben > ")

db_menu()