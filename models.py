from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
import datetime

engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5431/flask_app')

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

class Advertisement(Base):

    __tablename__ = 'advertisements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descriprion = Column(String, nullable=False)
    created_date = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False, index=True)

Base.metadata.create_all()


