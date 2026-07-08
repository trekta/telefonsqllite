import sqlite3, os

def db_anlegen():
    e = input("Die DB wird gelöscht, sind Sie sicher? (j/n)")
    if e != "j": return
    try:
        os.remove("schule.db")
    except: 
        print("Datenbank war nicht vorhanden")
    db = sqlite3.connect("schule.db") # Erzeugt oder Öffnet eine Datenbankdatei und das Datenbankobjekt db
    cursor = db.cursor() # Erzeugt ein Cursor-Objekt

    sql = """CREATE TABLE IF NOT EXISTS schueler (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        alterj INTEGER, 
        klasse TEXT)"""
    cursor.execute(sql)  # SQL ausführen

    db.close()  # DB geschlossen
    print("Datenbank und Tabelle angelegt!")

def schueler_eingeben():
    db = sqlite3.connect("schule.db") # Erzeugt oder Öffnet eine Datenbankdatei und das Datenbankobjekt db
    cursor = db.cursor() # Erzeugt ein Cursor-Objekt
    while True:
        n=input("Name>")
        if n=="": break
        a=int(input("Alter>"))
        k=input("Klasse>")
        sql = "INSERT INTO schueler (name, alterj, klasse) VALUES (?,?,?)" # Nur Platzhalter
        cursor.execute(sql,[n,a,k]) # Ausführen / Platzhalter mit Variablen füllen gegen SQL-Injection
        db.commit()  # Datentransfer bestätigen (Transaktion beenden)
        print("Daten eingefügt")

    db.close()
    print("Programm beendet")

def schueler_ausgeben():
    db = sqlite3.connect("schule.db") # Erzeugt oder Öffnet eine Datenbankdatei und das Datenbankobjekt db
    cursor = db.cursor() # Erzeugt ein Cursor-Objekt
    sql = "SELECT * FROM schueler ORDER BY name"
    cursor.execute(sql)
    print("\nID Name             Alter  Klasse")
    print("---------------------------------")
    for ds in cursor:
        print(f"{ds[0]:2} {ds[1]:16} {ds[2]:3}    {ds[3]:8}")
    db.close()

def schueler_suchen():
    db = sqlite3.connect("schule.db") # Erzeugt oder Öffnet eine Datenbankdatei und das Datenbankobjekt db
    cursor = db.cursor() # Erzeugt ein Cursor-Objekt
    s = input("Welchen Schüler suchen>")
    s = "%"+s+"%"  # Automatisch den Joker davor- und dinterhängen
    
    sql = "SELECT * FROM schueler WHERE name LIKE ? ORDER BY name"
    cursor.execute(sql,[s])

    print("\nID Name             Alter  Klasse")
    print("---------------------------------")
    for ds in cursor:
        print(f"{ds[0]:2} {ds[1]:16} {ds[2]:3}    {ds[3]:8}")
    db.close()

def schueler_loeschen():
    db = sqlite3.connect("schule.db") # Erzeugt oder Öffnet eine Datenbankdatei und das Datenbankobjekt db
    cursor = db.cursor() # Erzeugt ein Cursor-Objekt
    e = int(input("Welche ID löschen>"))
    sql = "DELETE FROM schueler WHERE id = ?"
    cursor.execute(sql, [e])
    db.commit()
    db.close()

while True:
    print("\nHauptmenü Schüler")
    print("------------------")
    print("1. Datenbank neu anlegen")
    print("2. Schüler eingeben")
    print("3. Schüler ausgeben")
    print("4. Schüler suchen")
    print("5. Schüler löschen nach ID")
    print("9. Programm beenden")
    e=int(input("Wählen Sie eine Funktion>"))
    if e==9: break
    elif e==1: db_anlegen()
    elif e==2: schueler_eingeben()
    elif e==3: schueler_ausgeben()
    elif e==4: schueler_suchen()
    elif e==5:
        schueler_ausgeben()
        schueler_loeschen()