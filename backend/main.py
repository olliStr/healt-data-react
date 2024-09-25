from fastapi import FastAPI, Depends, Query
from database import engine, SessionLocal, Base, get_db
import requests
from sqlalchemy.orm import Session
from models import LifeExpectancy
from fastapi.middleware.cors import CORSMiddleware

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
    return {"message": "Daten erfolgreich importiert"}

@app.get("/life-expectancy")
def get_life_expectancy(
    country: str,
    db: Session = Depends(get_db)
    ):
    # SQL Abfrage
    data = db.query(LifeExpectancy).filter(LifeExpectancy.country == country).order_by(LifeExpectancy.year).all()

    # Anpassung für das Frontend
    response_data = [{
        "country": entry.country,
        "year": entry.year,
        "sex": entry.sex,
        "value": entry.value
    } for entry in data]

    print(country)

    return response_data

# router für die Extraktion der einzelnen Länder (Dropdown im Frontend)
@app.get("/countries")
def get_countries(db: Session = Depends(get_db)):
    countries = db.query(LifeExpectancy.country).distinct().all()
    country_list = [c[0] for c in countries]
    country_list.sort()
    return country_list

def fetch_and_store_life_expectancy_data():
    response = requests.get("https://ghoapi.azureedge.net/api/WHOSIS_000001")
    
    if response.status_code == 200:
        data = response.json()['value']

        db: Session = SessionLocal()

        for item in data:
            entry = LifeExpectancy(
                country=item['SpatialDim'],
                year=item['TimeDim'],
                sex=item['Dim1'],
                value=float(item['NumericValue'])
            )
            db.add(entry)

        db.commit()
        db.close()
    else:
        print(f'Fehler beim Abrufen der Daten {response.status_code}')

