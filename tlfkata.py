# telefonkatalog_mariadb.py

import mysql.connector  # Importing mysql.connector for MariaDB interaction

# Establishing a connection to the MariaDB database
conn = mysql.connector.connect(
    host="localhost",  # Replace with your MariaDB host, e.g., 'localhost'
    user="your_username",  # Replace with your MariaDB username
    password="your_password",  # Replace with your MariaDB password
    database="telefonkatalog"  # Database name
)

cursor = conn.cursor()  # Creating a cursor object to interact with the database

# Create table if it does not exist (similar to SQLite)
cursor.execute('''CREATE TABLE IF NOT EXISTS personer (
                fornavn VARCHAR(255),
                etternavn VARCHAR(255),
                telefonnummer VARCHAR(255)
            )''')

conn.commit()  # Save changes to the database


def visAllePersoner():
    cursor.execute("SELECT * FROM personer")
    resultater = cursor.fetchall()
    if not resultater:
        print("Det er ingen registrerte personer i katalogen")
        input("Trykk en tast for å gå tilbake til menyen")
        printMeny()
    else:
        print("*****************************************"
              "*****************************************")
        for personer in resultater:
            print("* Fornavn: {:15s} Etternavn: {:15s} Telfonnummer:{:8s}"
                  .format(personer[0], personer[1], personer[2]))
        print("*****************************************"
              "*****************************************")
        input("Trykk en tast for å gå tilbake til menyen")
        printMeny()


# Function to add a person to the database
def legg_til_person_i_db(fornavn, etternavn, telefonnummer):
    cursor.execute("INSERT INTO personer (fornavn, etternavn, telefonnummer) VALUES (%s, %s, %s)",
              (fornavn, etternavn, telefonnummer))
    conn.commit()


# Function to delete a person from the database based on first name, last name, and phone number
def slett_person_fra_db(fornavn, etternavn, telefonnummer):
    cursor.execute("DELETE FROM personer WHERE fornavn=%s AND etternavn=%s AND telefonnummer=%s",
              (fornavn, etternavn, telefonnummer))
    conn.commit()


def printMeny():
    print("------------------- Telefonkatalog -------------------")
    print("| 1. Legg til ny person                              |")
    print("| 2. Søk opp person eller telefonnummer              |")
    print("| 3. Vis alle personer                               |")
    print("| 4. Slett en person                                 |")
    print("| 5. Avslutt                                         |")
    print("------------------------------------------------------")
    menyvalg = input("Skriv inn tall for å velge fra menyen: ")
    utfoerMenyvalg(menyvalg)


def utfoerMenyvalg(valgtTall):
    if valgtTall == "1":
        registrerPerson()
    elif valgtTall == "2":
        sokPerson()
        printMeny()
    elif valgtTall == "3":
        visAllePersoner()
    elif valgtTall == "4":
        slettPerson()
    elif valgtTall == "5":
        bekreftelse = input("Er du sikker på at du vil avslutte? J/N ")
        if (bekreftelse == "J" or bekreftelse == "j"):
            conn.close()
            exit()
    else:
        nyttForsoek = input("Ugyldig valg. Velg et tall mellom 1-5: ")
        utfoerMenyvalg(nyttForsoek)


def registrerPerson():
    fornavn = input("Skriv inn fornavn: ")
    etternavn = input("Skriv inn etternavn: ")
    telefonnummer = input("Skriv inn telefonnummer: ")

    legg_til_person_i_db(fornavn, etternavn, telefonnummer)  # Add the new person to the database

    print("{0} {1} er registrert med telefonnummer {2}"
          .format(fornavn, etternavn, telefonnummer))
    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()


def slettPerson():
    fornavn = input("Skriv inn fornavn: ")
    etternavn = input("Skriv inn etternavn: ")
    telefonnummer = input("Skriv inn telefonnummer: ")

    slett_person_fra_db(fornavn, etternavn, telefonnummer)  # Delete the person from the database

    print("{0} {1} er slettet fra katalogen".format(fornavn, etternavn))
    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()


def sokPerson():
    print("1. Søk på fornavn")
    print("2. Søk på etternavn")
    print("3. Søk på telefonnummer")
    print("4. Tilbake til hovedmeny")
    sokefelt = input("Velg ønsket søk 1-3, eller 4 for å gå tilbake: ")
    if sokefelt == "1":
        navn = input("Fornavn: ")
        finnPerson("fornavn", navn)
    elif sokefelt == "2":
        navn = input("Etternavn: ")
        finnPerson("etternavn", navn)
    elif sokefelt == "3":
        tlfnummer = input("Telefonnummer: ")
        finnPerson("telefonnummer", tlfnummer)
    elif sokefelt == "4":
        printMeny()
    else:
        print("Ugyldig valg. Velg et tall mellom 1-4: ")
        sokPerson()


def finnPerson(typeSok, sokeTekst):
    query = f"SELECT * FROM personer WHERE {typeSok}=%s"
    cursor.execute(query, (sokeTekst,))
    resultater = cursor.fetchall()

    if not resultater:
        print("Finner ingen personer")
    else:
        for personer in resultater:
            print("{0} {1} har telefonnummer {2}".format(personer[0], personer[1], personer[2]))


printMeny()  # Starter programmet ved å skrive menyen første gang
