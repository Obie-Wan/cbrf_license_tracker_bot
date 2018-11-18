from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BankSanction(Base):
    __tablename__ = 'sanctions'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False)
    url = Column(String(256), unique=True, nullable=False)
    date = Column(Date(), nullable=False)

    def __repr__(self):
        return '%s' % self.name

