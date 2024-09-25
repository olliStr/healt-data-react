from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL-Verbindungs-URL (passe Benutzername, Passwort, und Datenbank an)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://health_user:password@localhost/health_data"

# Datenbank-Engine erstellen
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionFactory für die Datenbankverbindungen
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