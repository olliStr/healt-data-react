from fastapi import FastAPI, Depends, Query
from database import engine, SessionLocal, Base, get_db
import requests
from sqlalchemy.orm import Session
from models import LifeExpectancy, Countries
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
    fetch_and_store_life_expectancy_data()
    fetch_and_store_country_data()
    return {"message": "Daten erfolgreich importiert"}

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

def fetch_and_store_country_data():
    db: Session = SessionLocal()


    first_country = db.query(Countries).first()
    print("Ergebnis der ersten Abfrage:", (first_country is not None))

    # Überprüfen, ob die Tabelle bereits existiert
    if db.query(Countries).first() is None:
        response = requests.get("https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues")

        if response.status_code == 200:
            data = response.json()['value']

            for item in data:
                entry = Countries(
                    code=item['Code'],
                    title=item['Title']
                )
                db.add(entry)
            
            db.commit()
        else:
            print(f'Fehler beim Abrufen der Daten {response.status_code}')
    else:
        print("Tabelle ist bereits vorhanden.")
    
    db.close()

def fetch_and_store_life_expectancy_data():
    
    db: Session = SessionLocal()

    # Überprüfen, ob die Tabelle bereits existiert
    if db.query(LifeExpectancy).first() is None:
        response = requests.get("https://ghoapi.azureedge.net/api/WHOSIS_000001")
        
        if response.status_code == 200:
            data = response.json()['value']

            for item in data:
                entry = LifeExpectancy(
                    country=item['SpatialDim'],
                    year=item['TimeDim'],
                    sex=item['Dim1'],
                    value=float(item['NumericValue'])
                )
                db.add(entry)

            db.commit()
        else:
            print(f'Fehler beim Abrufen der Daten {response.status_code}')
    else:
        print("Tabelle ist bereits vorhanden.")

    db.close()



