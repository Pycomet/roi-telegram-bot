from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

engine = create_engine("sqlite:///database.db", echo=True)
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
    date_joined = Column(String)
    address = Column(String)
    transaction = relationship("Transaction", backref="owner")

    def __repr__(self):
        return "<User(id='%d', name='%s')>" % (self.id, self.first_name)


class Transaction(Base):
    """
    SqlAlchemy ORM Transaction Model
    """
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    date_created = Column(String(50))
    user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship("User", back_populates="transaction")

    def __repr__(self):
        return "<Tansaction(id='%s')>" % (self.id)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


session = Session()


session.close()