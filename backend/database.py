from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Variablen aus der .env laden
load_dotenv()

# MySQL-Verbindungs-URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Datenbank-Engine erstellen
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session für die Datenbankverbindungen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basis-Klasse für die Modelle
Base = declarative_base()

# Datenbank-Session für jede Anfrage erstellen und schließen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()