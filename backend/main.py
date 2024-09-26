from fastapi import FastAPI, Depends, Query
from database import engine, SessionLocal, Base, get_db
import requests
from sqlalchemy.orm import Session
from models import LifeExpectancy, Countries, ObesityPrevalence, HypertensionPrevalence, DeathProbability
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, case, inspect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Erlaube das Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello, HealthData!"}

@app.post("/import-data")
def import_data():
    db: Session = SessionLocal()

    fetch_and_store_data(
        db=db,
        Table=LifeExpectancy,
        url="https://ghoapi.azureedge.net/api/WHOSIS_000001",
        store_data=store_life_expectancy_data
    )

    fetch_and_store_data(
        db=db,
        Table=Countries,
        url="https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues",
        store_data=store_country_data
    )

    fetch_and_store_data(
        db=db,
        Table=ObesityPrevalence,
        url="https://ghoapi.azureedge.net/api/NCD_BMI_30C",
        store_data=store_obesity_prevalence_data
    )

    fetch_and_store_data(
        db=db,
        Table=HypertensionPrevalence,
        url="https://ghoapi.azureedge.net/api/NCD_HYP_TREATMENT_A",
        store_data=store_hypertension_prevalence_data
    )

    fetch_and_store_data(
        db=db,
        Table=DeathProbability,
        url="https://ghoapi.azureedge.net/api/NCDMORT3070",
        store_data=store_death_probability_data
    )

    db.close()
    return {"message": "Daten erfolgreich importiert"}

@app.get("/death-probability")
def get_death_probability(
    country: str,
    db: Session = Depends(get_db)
    ):

    # Abfrage für das gewünschte Land und Sortierung nach Jahr
    data = db.query(
        DeathProbability.year,
        func.max(case((DeathProbability.sex == 'SEX_FMLE', DeathProbability.value), else_=None)).label('female'),
        func.max(case((DeathProbability.sex == 'SEX_MLE', DeathProbability.value), else_=None)).label('male')
    ).filter(DeathProbability.country == country)\
     .group_by(DeathProbability.year)\
     .order_by(DeathProbability.year).all()

    # Anpassung für das Frontend
    response_data = [{
        "year": entry.year,
        "female": entry.female,
        "male": entry.male,
    } for entry in data]

    print(country)

    return response_data

@app.get("/hypertension-prevalence")
def get_hypertension_prevalence(
    country: str,
    db: Session = Depends(get_db)
    ):

    # Abfrage für das gewünschte Land und Sortierung nach Jahr
    data = db.query(
        HypertensionPrevalence.year,
        func.max(case((HypertensionPrevalence.sex == 'SEX_FMLE', HypertensionPrevalence.value), else_=None)).label('female'),
        func.max(case((HypertensionPrevalence.sex == 'SEX_MLE', HypertensionPrevalence.value), else_=None)).label('male')
    ).filter(HypertensionPrevalence.country == country)\
     .group_by(HypertensionPrevalence.year)\
     .order_by(HypertensionPrevalence.year).all()

    # Anpassung für das Frontend
    response_data = [{
        "year": entry.year,
        "female": entry.female,
        "male": entry.male,
    } for entry in data]

    print(country)

    return response_data

@app.get("/obesity-prevalence")
def get_obesity_prevalence(
    country: str,
    db: Session = Depends(get_db)
    ):

    # Abfrage für das gewünschte Land und Sortierung nach Jahr
    data = db.query(
        ObesityPrevalence.year,
        func.max(case((ObesityPrevalence.sex == 'SEX_FMLE', ObesityPrevalence.value), else_=None)).label('female'),
        func.max(case((ObesityPrevalence.sex == 'SEX_MLE', ObesityPrevalence.value), else_=None)).label('male')
    ).filter(ObesityPrevalence.country == country)\
     .group_by(ObesityPrevalence.year)\
     .order_by(ObesityPrevalence.year).all()

    # Anpassung für das Frontend
    response_data = [{
        "year": entry.year,
        "female": entry.female,
        "male": entry.male,
    } for entry in data]

    print(country)

    return response_data


@app.get("/life-expectancy")
def get_life_expectancy(
    country: str,
    db: Session = Depends(get_db)
    ):

    # Abfrage für das gewünschte Land und Sortierung nach Jahr
    data = db.query(
        LifeExpectancy.year,
        func.max(case((LifeExpectancy.sex == 'SEX_FMLE', LifeExpectancy.value), else_=None)).label('female'),
        func.max(case((LifeExpectancy.sex == 'SEX_MLE', LifeExpectancy.value), else_=None)).label('male')
    ).filter(LifeExpectancy.country == country)\
     .group_by(LifeExpectancy.year)\
     .order_by(LifeExpectancy.year).all()

    # Anpassung für das Frontend
    response_data = [{
        "year": entry.year,
        "female": entry.female,
        "male": entry.male,
    } for entry in data]

    print(country)

    return response_data

# router für die Extraktion der einzelnen Länder (Dropdown im Frontend)
@app.get("/countries")
def get_countries(db: Session = Depends(get_db)):
    countries = db.query(Countries.code, Countries.title).all()
    country_dict = {sub[0]: sub[1] for sub in countries}
    print(country_dict)
    return country_dict

### HELPERS ###

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

# Lebenserwartung in Jahren
def store_life_expectancy_data(db: Session, data: list):
    for item in data:
        entry = LifeExpectancy(
            country=item['SpatialDim'],
            year=item['TimeDim'],
            sex=item['Dim1'],
            value=float(item['NumericValue'])
        )
        db.add(entry)
    db.commit()

# Länder
def store_country_data(db: Session, data: list):
    for item in data:
        entry = Countries(
            code=item['Code'],
            title=item['Title']
        )
        db.add(entry)
    db.commit()

# Prävalenz Übergewicht
def store_obesity_prevalence_data(db: Session, data: list):
    for item in data:
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