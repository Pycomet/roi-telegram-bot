from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

from sqlalchemy import Column, Integer, String, ForeignKey

from config import *

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=False)
# Change encho to false before deploying

# user_transaction_association = Table('user_transactions', Base.metadata,
#     Column('user_id', Integer, ForeignKey('user.id')),
#     Column('transaction_id', Integer, ForeignKey('transaction.id'))
# )

class User(Base):
    """
    SqlAlchemy ORM User Model
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    btc_balance = Column(Integer)
    xrp_balance = Column(Integer)
    
    btc_address = Column(String)
    xrp_address = Column(String)

    btc_address_id = Column(String)
    xrp_address_id = Column(String)

    btc_investment = Column(Integer)
    xrp_investment = Column(Integer)

    date_joined = Column(String)
    transaction = relationship("Transaction", backref="owner")

    def __repr__(self):
        return "<User(id='%d', name='%s')>" % (self.id, self.first_name)


class Transaction(Base):
    """
    SqlAlchemy ORM Transaction Model
    """
    __tablename__ = 'transaction'

    id = Column(String, primary_key=True)
    currency = Column(String(3))
    amount = Column(Integer)
    title = Column(String)
    hash = Column(String)
    status = Column(String)
    date_created = Column(String(50))
    user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship("User", back_populates="transaction")

    def __repr__(self):
        return "<Tansaction(id='%s')>" % (self.id)

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine, autoflush=False)

session = Session()

# import pdb; pdb.set_trace()

session.close()

