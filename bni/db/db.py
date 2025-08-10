from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bni.model.data_model import Base

# Example: SQLite (you can replace with MySQL/PostgreSQL)
engine = create_engine("sqlite:///bni.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
