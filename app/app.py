from flask import Flask, render_template, request, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
from dotenv import load_dotenv
from pandas import read_sql
from sqlalchemy import create_engine, text
from db_functions import update_or_create_user
import logging

load_dotenv()  

GCPURL = os.getenv("GCPURL")

engine = create_engine(GCPURL,
    connect_args={'ssl': {'ssl-mode':'preferred'}},
)    

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

logging.basicConfig(
    level=logging.DEBUG,
    filename="logs/app.log",
    filemode="w",
    format='%(levelname)s - %(name)s - %(message)s'
)

app = Flask(__name__)   

app.secret_key = os.urandom(12)
oauth = OAuth(app)

@app.route('/')
def mainpage():
    try:
        logging.debug("success! You have reached the home page!")
        return render_template('base.html')
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "please try again"    


@app.route('/google/')
def google():
    try:
        logging.debug("success! You have accessed the Google webpage!")
        CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
        oauth.register(
            name='google',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        redirect_uri = url_for('google_auth', _external=True)
        print('REDIRECT URL: ', redirect_uri)
        session['nonce'] = generate_token()
        redirect_uri = 'https://5000-cs-95785c58-446f-40ea-8544-2b7d3521503b.cs-us-east1-pkhd.cloudshell.dev/google/auth/'
        return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "please try again"  

@app.route('/google/auth/')
def google_auth():
    try:
        logging.debug("success! Google authorization page has been accessed")
        token = oauth.google.authorize_access_token()
        user = oauth.google.parse_id_token(token, nonce=session['nonce'])
        session['user'] = user
        update_or_create_user(user)
        print(" Google User ", user)
        return redirect('/dashboard')
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "please try again"    


@app.route('/dashboard/')
def dashboard():
    try:
        logging.debug("success! Dashboard page has been accessed")
        user = session.get('user')
        if user:
            return render_template('dashboard.html', user=user)
        else:
            return redirect('/')
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "please try again"    


@app.route('/logout')
def logout():
    try:
        logging.debug("successfully logged out.")
        session.pop('user', None)
        return redirect('/')
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "please try again"       



@app.route('/patients')
def patients():
    try:
        logging.debug("success! Patients page has been accessed")
        id = request.args.get('id')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        date_of_birth = request.args.get('date_of_birth')
        contact_number = request.args.get('contact_number')
        email = request.args.get('email')
        address = request.args.get('address')
    # Establish a database connection
        with engine.connect() as connection:
            if first_name:
                query1 = text('SELECT * FROM patients WHERE first_name = :first_name')
                result1 = connection.execute(query1, {"first_name": first_name})
            elif last_name:
                query1 = text('SELECT * FROM patients WHERE last_name = :last_name')
                result1 = connection.execute(query1, {"last_name": last_name})
            elif id:
                query1 = text('SELECT * FROM patients WHERE id = :id')
                result1 = connection.execute(query1, {"id": id})
            elif date_of_birth:
                query1 = text('SELECT * FROM patients WHERE date_of_birth = :date_of_birth')
                result1 = connection.execute(query1, {"date_of_birth": date_of_birth})
            elif contact_number:
                query1 = text('SELECT * FROM patients WHERE contact_number = :contact_number')
                result1 = connection.execute(query1, {"contact_number": contact_number})
            elif email:
                query1 = text('SELECT * FROM patients WHERE email = :email')
                result1 = connection.execute(query1, {"email": email})
            elif address:
                query1 = text('SELECT * FROM patients WHERE address = :address')
                result1 = connection.execute(query1, {"address": address})
            else:
                query1 = text('SELECT * FROM patients')
                result1 = connection.execute(query1)   

        # Fetch all rows of data
            patientdata = result1.fetchall()

        return render_template('patients.html', data1=patientdata)
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"     
    


@app.route('/prostate')
def patientprostate():
    try:
        logging.debug("success! Patient prostate data page has been accessed")
        id = request.args.get('id')
        patient_id = request.args.get('patient_id')
        psa = request.args.get('psa')
        prostate_volume = request.args.get('prostate_volume')
        exodx = request.args.get('exodx')
        mri = request.args.get('mri') 
        decipher = request.args.get('decipher') 
     # Establish a database connection
        with engine.connect() as connection:
            if id:
                query2 = text('SELECT * FROM prostate_data WHERE id = :id')
                result2 = connection.execute(query2, {"id": id})
            elif patient_id:
                query2 = text('SELECT * FROM prostate_data WHERE patient_id = :patient_id')
                result2 = connection.execute(query2, {"patient_id": patient_id})
            elif psa:
                query2 = text('SELECT * FROM prostate_data WHERE psa = :psa')
                result2 = connection.execute(query2, {"psa": psa})
            elif prostate_volume:
                query2 = text('SELECT * FROM prostate_data WHERE prostate_volume = :prostate_volume')
                result2 = connection.execute(query2, {"prostate_volume": prostate_volume})
            elif exodx:
                query2 = text('SELECT * FROM prostate_data WHERE exodx = :exodx')
                result2 = connection.execute(query2, {"exodx": exodx})
            elif mri:
                query2 = text('SELECT * FROM prostate_data WHERE mri = :mri')
                result2 = connection.execute(query2, {"mri": mri})
            elif decipher:
                query2 = text('SELECT * FROM prostate_data WHERE decipher = :decipher')
                result2 = connection.execute(query2, {"decipher": decipher})
            else:
                query2 = text('SELECT * FROM prostate_data')
                result2 = connection.execute(query2)   

        # Fetch all rows of data
            prostatedata = result2.fetchall()

        return render_template('prostate.html', data2=prostatedata)
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"       


@app.route('/encounter')
def patientencounter():
    try:
        logging.debug("success! Patient Encounter page has been accessed")
        id = request.args.get('id')
        patient_id = request.args.get('patient_id')
        family_history = request.args.get('family_history')
        luts = request.args.get('luts')
        dre = request.args.get('dre')
        treatment = request.args.get('treatment')
        # Establish a database connection
        with engine.connect() as connection:
            if id:
                query3 = text('SELECT * FROM patient_encounter WHERE id = :id')
                result3 = connection.execute(query3, {"id": id})
            elif patient_id:
                query3 = text('SELECT * FROM patient_encounter WHERE patient_id = :patient_id')
                result3 = connection.execute(query3, {"patient_id": patient_id})
            elif family_history:
                query3 = text('SELECT * FROM patient_encounter WHERE family_history = :family_history')
                result3 = connection.execute(query3, {"family_history": family_history})
            elif luts:
                query3 = text('SELECT * FROM patient_encounter WHERE luts = :luts')
                result3 = connection.execute(query3, {"luts": luts})
            elif dre:
                query3 = text('SELECT * FROM patient_encounter WHERE dre = :dre')
                result3 = connection.execute(query3, {"dre": dre})
            elif treatment:
                query3 = text('SELECT * FROM patient_encounter WHERE treatment = :treatment')
                result3 = connection.execute(query3, {"treatment": treatment})
            else:
                query3 = text('SELECT * FROM patient_encounter')
                result3 = connection.execute(query3)   

        # Fetch all rows of data
            encounterdata = result3.fetchall()

        return render_template('encounter.html', data3=encounterdata)
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"       

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
