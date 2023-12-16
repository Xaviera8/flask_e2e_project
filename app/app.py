from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
from pandas import read_sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, engine
import pandas as pd


 # Load environment variables from .env file
load_dotenv() 

# Database connection settings from environment variables
db_url = os.getenv('db_url')

gcp_engine = db_url
engine = create_engine(gcp_engine)



app = Flask(__name__)


def show_table():
        # Establish a database connection
    with engine.connect() as connection:
        # Execute an SQL query to fetch data (replace this with your query)
        query1 = text('SELECT * FROM test')
        result1 = connection.execute(query1)
        # Fetch all rows of data
        patientdata = result1.fetchall()
        return patientdata


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/weight')
def weight():
    return render_template('weight.html')


@app.route('/weight_results')
def weight_results():
    patientdata = show_table()
    return render_template('weight_results.html', data1=patientdata)

@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        # Extract form data
        id_value = request.form.get('id')
        weight_value = request.form.get('weight')

        # Execute SQL INSERT statement
        with engine.connect() as connection:
            query_insert = text('INSERT INTO test (id, weight) VALUES (:id, :weight)')
            connection.execute(query_insert, {"id": id_value, "weight": weight_value})

        # Redirect to the /food route to see the updated data
        return redirect(url_for('food'))
    else:
        # Handle other HTTP methods if needed
        return redirect(url_for('food'))


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )

