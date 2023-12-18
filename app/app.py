from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
from pandas import read_sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import matplotlib

import sentry_sdk

# This will initalize the Sentry SDK with your specific configuration
sentry_sdk.init(
    dsn="https://03b73b565605f5019972700e04e309f5@o4506409273458688.ingest.sentry.io/4506409279684608",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
 # Load environment variables from .env file
load_dotenv() 

# Database connection settings from environment variables
db_url = os.getenv('db_url')


engine = create_engine(db_url)

Base = declarative_base()

# Define the Test class corresponding to the 'test' table
class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)

# Create the 'test' table if it doesn't exist
Base.metadata.create_all(engine)



app = Flask(__name__)


def show_table():
        # Establish a database connection
    with engine.connect() as connection:
        # Execute an SQL query to fetch data (replace this with your query)
        query1 = text('SELECT * FROM test')
        result1 = connection.execute(query1)
        # Fetch all rows of data
        user_weight = result1.fetchall()
        return user_weight




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/weight')
def weight():
    return render_template('weight.html')


@app.route('/weight_results')
def weight_results():
    user_weight = show_table()
    return render_template('weight_results.html', data1=user_weight)

@app.route('/add_data', methods=['POST'])
def add_data():
    id_value = request.form.get('id')
    weight_value = request.form.get('weight')
    # Create a new Test instance with the form data
    new_value = Test(id=id_value, weight=weight_value)

    # Create a session and add the new_test instance to the session
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
        raise Exception (f'something went wrong:{e}')
        return render_template(url_for('weight_error'))

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )




