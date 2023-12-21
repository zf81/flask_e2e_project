import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from faker import Faker
from db.db import Patient, Preferences, Demographics
import random

# Load environment variables
load_dotenv()

# Database connection settings from environment variables
DB_AZURE = os.getenv("DB_AZURE")


# Create a database engine
engine = create_engine(DB_AZURE, echo=False)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

#create a faker instance 
fake = Faker()

#creating lists for patient urology data

psa = ['4.89', '72.32', '0.002', '3.67', '4.12', '7.34', '16.09', '2.01', '1.33', '13.996', '5.53']

Exodx = ['15.9', '7.84', '12', '29', '56', '2.34', '78', '8.12', '3.31', '1.99', '32.49', '14.11']

MRI = ['PIRADS-3', 'PIRADS-2', 'NEGATIVE', 'PIRADS-4', 'PIRADS-5', 'NEGATIVE', 'PIRADS-2', 'PIRADS-4', 'PIRADS-5', 'PIRADS-3', 'PIRADS-4']

prostate_volume_cc = ['45', '78', '23', '5', '15', '34', '49', '53', '38', '12', '102']

decipher = ['0', '1', '0.3', '0.67', '0.22']


#family history 
#GU symptoms
#digital rectal exam
###

treatment = ['surgery', 'radiation', 'HIFU', 'active surveillance', 'cryoablation', 'cyber knife']

family_history = ['mint', 'pickle', 'blueberry', 'chocolate', 'pine', 'orange', 'strawberry', 'wasabi', 'lemon', 'bacon', 'coffee', 'mint', 'mint', 'mint', 'fennel']

# Functions to generate fake data
def create_fake_patient():
    first_name = fake.first_name()
    last_name = fake.last_name()
    return Patient(
        first_name = first_name,
        last_name = last_name,
        date_of_birth = fake.date_of_birth(),
        contact_number = fake.phone_number(),
        email = f"{first_name}.{last_name}@{fake.domain_name()}",
        address = fake.address()
    )

def create_fake_preferences():
    return Preferences(

    patient_id = session.query(Patient).order_by(func.rand()).first().id,
    favorite_food = random.choice(foods),
    favorite_shows = random.choice(show),
    hobbies = random.choice(hobby),
    toothpaste_flavor = random.choice(flavor)
    )

def create_fake_demographics():
    return Demographics(
    patient_id = session.query(Patient).order_by(func.rand()).first().id,
    gender = random.choice(genders),
    language_spoken = random.choice(sample_languages),
    marital_status = random.choice(marital),
    nationality = fake.country(),
    occupation = fake.job()
    )

# Generate and insert fake data
for _ in range(20):
    fake_patient = create_fake_patient()
    session.add(fake_patient)
    

for _ in range(20):
    fake_preferences = create_fake_preferences()
    session.add(fake_preferences)

for _ in range(20):
    fake_demographics = create_fake_demographics()
    session.add(fake_demographics)

#commit
session.commit()

#close session 
session.close()