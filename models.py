from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nama_lengkap = Column(String(255))
    username = Column(String(50), unique=True)
    password = Column(String(100))
    alamat = Column(String  (255))

# class Image(Base):
#     __tablename__ = 'images'

#     id = Column(Integer, primary_key=True)
#     image = Column(String(100))
#     location = Column(String(100))
#     description = Column(String(100))
#     label = Column(String(100))
