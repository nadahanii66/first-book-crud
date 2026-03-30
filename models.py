from sqlalchemy import BOOLEAN, Column, ForeignKey, Integer, String
from database import Base
class Books(Base):
    __tablename__ = "books"
    id     = Column(Integer, primary_key=True, index=True)
    title  = Column(String(50), index=True, unique=True)
    author = Column(String(100), index=True)