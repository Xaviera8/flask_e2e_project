from flask import Flask, render_template, url_for, redirect, session, request
from datetime import datetime  
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from dotenv import load_dotenv
import os
from db_functions import update_or_create_user
from sqlalchemy import create_engine, text, engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sentry_sdk import capture_exception

load_dotenv()

import sentry_sdk

# This will initalize the Sentry SDK with your specific configuration
sentry_sdk.init(
    dsn="https://03b73b565605f5019972700e04e309f5@o4506409273458688.ingest.sentry.io/4506409279684608",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

app = Flask(__name__)
app.secret_key = os.urandom(12)
oauth = OAuth(app)

db_url = os.getenv('db_url')

engine = create_engine(db_url)
Base = declarative_base()

class Weight(Base):
    __tablename__ = 'weight'
    record_date = Column(DateTime, primary_key=True)
    weight = Column(Integer)

def show_table():
        # Establish a database connection
    with engine.connect() as connection:
        # Execute an SQL query to fetch data (replace this with your query)
        query1 = text('SELECT * FROM weight order by record_date desc;')
        result1 = connection.execute(query1)
        # Fetch all rows of data
        user_weight = result1.fetchall()
        return user_weight


@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/google/')
def google():
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

    # Redirect to google_auth function
    ###note, if running locally on a non-google shell, do not need to override redirect_uri
    ### and can just use url_for as below
    redirect_uri = url_for('google_auth', _external=True)
    print('REDIRECT URL: ', redirect_uri)
    session['nonce'] = generate_token()
    ##, note: if running in google shell, need to override redirect_uri 
    ## to the external web address of the shell, e.g.,
    redirect_uri = 'https://5000-cs-538798890225-default.cs-us-east1-vpcf.cloudshell.dev/google/auth/'
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    update_or_create_user(user)
    print(" Google User ", user)
    return redirect('/dashboard')

@app.route('/dashboard/')
def dashboard():
    user = session.get('user')
    if user:
        return render_template('index.html', user=user)
    else:
        return redirect('/')

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/weight')
def weight():
    return render_template('weight.html')


@app.route('/weight_results')
def weight_results():
    user_weight = show_table()
    return render_template('weight_results.html', data1=user_weight)

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    date_value = request.form.get('date')
    weight_value = request.form.get('weight')

    # Convert to a datetime object
    date_value = datetime.strptime(date_value, '%Y-%m-%d')

    # Create a new Weight instance with the form data
    new_value = Weight(record_date=date_value, weight=weight_value)

    # Create a session and add the new_value instance to the session
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.add(new_value)
        # Commit the changes to the database
        session.commit()
        # Close the session
        session.close()
        # Redirect to a success page or another route
        return redirect(url_for('weight_results'))
    except Exception as e:
        capture_exception(e)
        return redirect(url_for('error'))




@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(
        debug=True, 
        port=5000
    )