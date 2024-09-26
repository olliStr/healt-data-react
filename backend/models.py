from sqlalchemy import Column, Integer, String, Float
from database import Base

class LifeExpectancy(Base):
    __tablename__ = "life_expectancy"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    sex = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)

class Countries(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)

class ObesityPrevalence(Base):
    __tablename__ = "obesity_prevalence"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    sex = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)

class HypertensionPrevalence(Base):
    __tablename__ = "hypertension_prevalence"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    sex = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)

class DeathProbability(Base):
    __tablename__ = "death_probability"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    sex = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)