import sqlite3

# 1. Erstellen Sie ein Python-Skript, das die entsprechenden Tabellen in SQLite anlegt:

def create_bank_db():
    db = sqlite3.connect("bank.db")
    cursor = db.cursor()
    sql_konto = """CREATE TABLE IF NOT EXISTS konto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inhaber TEXT NOT NULL,
        kontostand REAL NOT NULL DEFAULT 0);"""
    
    sql_überweisung = """CREATE TABLE IF NOT EXISTS ueberweisung (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quellkonto_id INTEGER NOT NULL,
        zielkonto_id INTEGER NOT NULL,
        betrag REAL NOT NULL CHECK (betrag > 0),
        zeitstempel TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (quellkonto_id)
        REFERENCES konto(id),
        FOREIGN KEY (zielkonto_id)
        REFERENCES konto(id)
        );
        """
    cursor.execute(sql_konto)
    cursor.execute(sql_überweisung)
    db.close()

# 2. Fügen Sie in einem zweiten Skript Datensätze per Benutzereingabe in die Tabellen ein.

def konto_erstellen(inhaber: str, konotostand: float):
    db = sqlite3.connect("bank.db")
    cursor = db.cursor()
    sql = """INSERT INTO konto (inhaber, kontostand) VALUES(?,?)
    """
    cursor.execute(sql,[inhaber, konotostand])
    db.commit()
    db.close()
    print(f"Konto für {inhaber} erstellt und {konotostand} als Kontostand gesetzt")


def überweiseung(q_name:str, z_name:str, betrag):
    """namen zu id auflösen
        q_konto verringen
        z_konto erhöhen
        überweisung schreiben"""
    db = sqlite3.connect("bank.db")
    cursor = db.cursor()
    try:
        sql_id_auflösen = "SELECT id FROM konto WHERE inhaber = ?"
        
        cursor.execute(sql_id_auflösen, [q_name])
        q_id_o = cursor.fetchone()
        if q_id_o is None:
            print(f"Sender '{q_name}' nicht gefunden! ABBRUCH!")
            return
        
        cursor.execute(sql_id_auflösen, [z_name])
        z_id_o = cursor.fetchone()
        if z_id_o is None:
            print(f"Empfänger '{z_name}' nicht gefunden! ABBRUCH!")
            return
        
        sql_q_verringern = "UPDATE konto SET kontostand = kontostand - ? WHERE id = ?"
        cursor.execute(sql_q_verringern, [betrag, q_id_o[0]])

        sql_z_erhöhen = "UPDATE konto SET kontostand = kontostand + ? WHERE id = ?"
        cursor.execute(sql_z_erhöhen, [betrag, z_id_o[0]])

        sql_überweisung = """INSERT INTO ueberweisung (quellkonto_id, zielkonto_id, betrag)
            VALUES(?,?,?)
            """
        cursor.execute(sql_überweisung, [q_id_o[0], z_id_o[0], betrag])
        db.commit()
    except:
        print("Da ist was schiefgelaufen")
    finally:
        db.close()

# 3. Ein dritte Skript soll eine Liste der Überweisungen ausgeben:

def ausgabe():
    db = sqlite3.connect("bank.db")
    cursor = db.cursor()
    sql = """SELECT u.id, qk.inhaber AS quelle, zk.inhaber AS ziel, u.betrag, DATE(u.zeitstempel)
        FROM ueberweisung u
        JOIN konto qk ON u.quellkonto_id = qk.id
        JOIN konto zk ON u.zielkonto_id = zk.id
    """
    cursor.execute(sql)
    for ds in cursor:
        print(f"{ds[0]:2} {ds[1]:2} {ds[2]:2} {ds[3]:10.2f} {ds[4]:10}")


while True:
    print("\nHauptmenü Bank")
    print("-"*15)
    print("1. Datenbank anlegen")
    print("2. Konto erstellen")
    print("3. Überweisung tätigen")
    print("4. Überweisungen anzeigen")
    print("9. Programm beenden")
    e=int(input("Wählen Sie eine Funktion >"))
    if e == 9:
        break
    elif e == 1:
        create_bank_db()
    elif e == 2:
        while True:
            n = input("Name > ")
            if n == "":
                break
            k = input("Kontostand > ")
            if k == '': k = 0
            k = float(k)
            konto_erstellen(n,k)
    
    elif e == 3:
        while True:
            z = input("Empfänger Name > ")
            if z == "":
                break
            q = input("Sender Name > ")
            b = float(input("Betrag > "))
            überweiseung(q,z,b)
    
    elif e == 4:
        ausgabe()