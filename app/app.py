import os
from dotenv import load_dotenv
from pandas import read_sql
from sqlalchemy import create_engine, inspect
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/steps')
def index():
    return render_template('steps.html')


@app.route('/food')
def index():
    return render_template('food.html')

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )