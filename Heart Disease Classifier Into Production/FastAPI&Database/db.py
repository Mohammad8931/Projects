from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/heart_disease_database"

Base = declarative_base()

class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True, index=True)
    thalach = Column(Float)
    cp = Column(Float)
    ca = Column(Float)
    thal = Column(Float)
    result = Column(String)
    prediction_date = Column(DateTime, default=datetime.now)
    prediction_source = Column(String)

class Feature(Base):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    value = Column(String)
    prediction_id = Column(Integer, ForeignKey('predictions.id'))

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
