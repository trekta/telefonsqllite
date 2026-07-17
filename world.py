from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = "world"
)

cursor = db.cursor()

def run_print_sql(sql_statement):
    cursor.execute(sql_statement)
    liste = cursor.fetchall()
    for ds in liste:
        print(*ds)


# übungen world db

sql_a = """SELECT Name, LifeExpectancy
    FROM country
    ORDER BY LifeExpectancy DESC
    LIMIT 10"""

sql_b = """SELECT Name, Population
    FROM city
    ORDER BY Population DESC
    LIMIT 10"""

sql_c = """SELECT Name, GNP, GovernmentForm
    FROM country
    ORDER BY GNP DESC
    LIMIT 10"""

sql_d = """SELECT Name, Population / SurfaceArea AS Bevölkerungsdichte
    FROM country
    ORDER BY Bevölkerungsdichte DESC
    LIMIT 5"""

sql_e = """SELECT Name, cl.Language
    FROM (select Code, Name, Population FROM country ORDER BY Population DESC LIMIT 5) as c
    LEFT JOIN countrylanguage cl ON c.Code = cl.CountryCode"""

sql_f = """SELECT AVG(Population)
    FROM (SELECT Name, Population, LifeExpectancy FROM country WHERE Population IS NOT NULL AND Population != 0 AND LifeExpectancy IS NOT NULL ORDER BY LifeExpectancy ASC LIMIT 5 ) as c
    """

sql_g = """SELECT AVG(Population)
    FROM (SELECT Name, Population, LifeExpectancy FROM country ORDER BY LifeExpectancy DESC LIMIT 5 ) as c
    """

sql_h = """SELECT c.Name, c.Population
    FROM city c
    JOIN country co ON co.Code = c.CountryCode
    WHERE co.Name = %s
    ORDER BY c.Population DESC"""

queries = {
    "a": sql_a,
    "b": sql_b,
    "c": sql_c,
    "d": sql_d,
    "e": sql_e,
    "f": sql_f,
    "g": sql_g,
}


def menü():
    while True:
        print("Aufgabe ausführen (a-h)")
        e = input("Aufgabe > ")
        if e == "h":
            l = input("Land? >")
            if l == "":
                break
            else:
                cursor.execute(sql_h, [l])
                liste = cursor.fetchall()
                for ds in liste:
                    print(*ds)
        elif e not in queries:
            break
        else:
            run_print_sql(queries[e])


menü()

db.close()