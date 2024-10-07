from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class Countries(Base):
    __tablename__ = "countries"

    code = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)

class Genders(Base):
    __tablename__ ="genders"

    code = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)

class LifeExpectancy(Base):
    __tablename__ = "life_expectancy"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), ForeignKey('countries.code'))
    year = Column(Integer, nullable=False)
    sex = Column(String(50), ForeignKey('genders.code'))
    value = Column(Float, nullable=False)

class ObesityPrevalence(Base):
    __tablename__ = "obesity_prevalence"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), ForeignKey('countries.code'))
    year = Column(Integer, nullable=False)
    sex = Column(String(50), ForeignKey('genders.code'))
    value = Column(Float, nullable=False)

class HypertensionPrevalence(Base):
    __tablename__ = "hypertension_prevalence"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), ForeignKey('countries.code'))
    year = Column(Integer, nullable=False)
    sex = Column(String(50), ForeignKey('genders.code'))
    value = Column(Float, nullable=False)

class DeathProbability(Base):
    __tablename__ = "death_probability"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), ForeignKey('countries.code'))
    year = Column(Integer, nullable=False)
    sex = Column(String(50), ForeignKey('genders.code'))
    value = Column(Float, nullable=False)