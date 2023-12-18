import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
from faker import Faker

# Load environment variables
load_dotenv()

# Database connection settings from environment variables
db_url = os.getenv('db_url')

# Connection string
conn_string = db_url

# Create a database engine
engine = create_engine(conn_string, echo=True)  # Set echo=True for SQL statement debugging
Base = declarative_base()

# Define the Test class corresponding to the 'test' table
class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)

# Create the 'test' table if it doesn't exist
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.commit()
# Close the session
session.close()

print("Done")
