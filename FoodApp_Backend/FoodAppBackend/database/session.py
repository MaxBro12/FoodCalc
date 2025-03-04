from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session():
    engine = create_engine('sqlite:///food_app.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def close_session(session):
    session.close()
