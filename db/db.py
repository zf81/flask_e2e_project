"""

pip install sqlalchemy alembic mysql-connector-python
pip install pymysql

"""

## Part 1 - Define SQLAlchemy models for patients and their preferences:

from sqlalchemy import create_engine, inspect, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

GCPURL = os.getenv("GCPURL")

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    contact_number = Column(String(100))
    email = Column(String(100))
    address = Column(String(200))

    prostate = relationship('Prostate', back_populates='patient')
    encounter = relationship('Encounter', back_populates='patient2')

class Prostate(Base):
    __tablename__ = 'prostate_data'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    psa = Column(String(200), nullable=False)
    prostate_volume = Column(String(200))
    exodx = Column(String(200))
    mri = Column(String(100))  
    decipher = Column(String(100))  
    
    patient = relationship('Patient', back_populates='prostate')

class Encounter(Base):
    __tablename__ = 'patient_encounter'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    family_history = Column(String(100), nullable=False)
    luts = Column(String(100))
    dre = Column(String(100))
    treatment = Column(String(100))

    patient2 = relationship('Patient', back_populates='encounter')

### Part 2 - initial sqlalchemy-engine to connect to db:


engine = create_engine(GCPURL,
    connect_args={'ssl': {'ssl-mode':'preferred'}},
)    


## Test connection

inspector = inspect(engine)
inspector.get_table_names()


### Part 3 - create the tables using sqlalchemy models, with no raw SQL required:

Base.metadata.create_all(engine)
