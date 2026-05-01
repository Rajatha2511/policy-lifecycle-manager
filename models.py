from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///policy.db", echo=False)
Session = sessionmaker(bind=engine)

class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ai_result = Column(Text, nullable=True)  # this is where we attach the AI result

Base.metadata.create_all(engine)  # creates the table

