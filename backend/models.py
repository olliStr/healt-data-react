from sqlalchemy import Column, Integer, String, Float
from database import Base

class LifeExpectancy(Base):
    __tablename__ = "life_expectancy"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    sex = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)