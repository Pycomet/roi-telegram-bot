from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

engine = create_engine("sqlite:///database.db", echo=True)
# Change encho to false before deploying

class User(Base):
    """
    SqlAlchemy ORM for Bot Application
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    btc_balance = Column(Integer)
    xrp_balance = Column(Integer)
    date_joined = Column(String)
    address = Column(String)

    def __repr__(self):
        return "<User(id='%d', name='%s')>" % (self.id, self.first_name)


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


session = Session()


session.close()