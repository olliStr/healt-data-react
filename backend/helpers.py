import requests
from sqlalchemy.orm import Session
from models import Countries, Genders, LifeExpectancy, ObesityPrevalence, HypertensionPrevalence, DeathProbability


def fetch_and_store_data(db: Session, Table, url: str, store_data):
    
    # Überprüfen, ob die Tabelle bereits existiert
    if does_table_exist(db=db, Table=Table):
        data = fetch_data(url=url)
        
        if data:
            store_data(db, data)
            print("Daten erfolgreich abgerufen und gespeichert.")
        else:
            print("Fehler beim Abrufen der Daten.")
    
    else:
        print("Daten sind bereits vorhanden.")

        

# Daten aus der Api abfragen
def fetch_data(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['value']
    else:
        print(f'Fehler beim Abrufen der Daten: {response.status_code}')
        return None

## Daten aus der Api in der DB speichern 

# Länder
def store_country_data(db: Session, data: list):
    for item in data:
        entry = Countries(
            code=item['Code'],
            title=item['Title']
        )
        db.add(entry)
    db.commit()

# Geschlechter
def store_gender_data(db: Session, data: list):
    for item in data:
        entry = Genders(
            code=item['Code'],
            title=item['Title']
        )
        db.add(entry)
    db.commit()

# Lebenserwartung in Jahren
def store_life_expectancy_data(db: Session, data: list):
    for item in data:
        if item['SpatialDimType'] == 'COUNTRY': # Nur die Daten mit den Ländern
            entry = LifeExpectancy(
                country=item['SpatialDim'],
                year=item['TimeDim'],
                sex=item['Dim1'],
                value=float(item['NumericValue'])
            )
            db.add(entry)
    db.commit()

# Prävalenz Übergewicht
def store_obesity_prevalence_data(db: Session, data: list):
    for item in data:
        if item['SpatialDimType'] == 'COUNTRY': # Nur die Daten mit den Ländern
            entry = ObesityPrevalence(
                country=item['SpatialDim'],
                year=item['TimeDim'],
                sex=item['Dim1'],
                value=float(item['NumericValue'])
            )
            db.add(entry)
    db.commit()

# Prävalenz Bluthochdruck Mellitus
def store_hypertension_prevalence_data(db: Session, data: list):
    for item in data:
        if item['SpatialDimType'] == 'COUNTRY': # Nur die Daten mit den Ländern
            entry = HypertensionPrevalence(
                country=item['SpatialDim'],
                year=item['TimeDim'],
                sex=item['Dim1'],
                value=float(item['NumericValue'])
            )
            db.add(entry)
    db.commit()

# Sterbewahrscheinlichkeit bei Volkskrankheiten
def store_death_probability_data(db: Session, data: list):
    for item in data:
        if item['SpatialDimType'] == 'COUNTRY': # Nur die Daten mit den Ländern
            entry = DeathProbability(
                country=item['SpatialDim'],
                year=item['TimeDim'],
                sex=item['Dim1'],
                value=float(item['NumericValue'])
            )
            db.add(entry)
    db.commit()

# Überprüfen, ob es eine Tabelle bereits gibt (neues Anlegen von Tabellen)
def does_table_exist(db: Session, Table):
    return db.query(Table).first() is None