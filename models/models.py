from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String
from sqlalchemy import Column

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(BIGINT)
    is_available = Column(Boolean, default=True)
    seller_email = Column(String)
    deleted = Column(Boolean, default=False)
    created_by = Column(String),
