import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Database connection settings from environment variables
db_url = os.getenv('db_url')

# Connection string
conn_string = db_url

# Create a database engine
engine = create_engine(conn_string, echo=True)  # Set echo=True for SQL statement debugging

# Use declarative_base from sqlalchemy.orm
Base = declarative_base()

# Define the Test class corresponding to the 'test' table
class Weight(Base):
    __tablename__ = 'weight'
    Date = Column(DateTime, primary_key=True)
    weight = Column(Integer)

# Create the 'weight' table if it doesn't exist
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Commit and close the session
session.commit()
session.close()

print("Done")
