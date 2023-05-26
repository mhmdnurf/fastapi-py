from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from models import Base, User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine

db_url = "mysql+mysqlconnector://root:@localhost/fastapi-test"
engine = create_engine(db_url)

app = FastAPI()
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

@app.post("/register")
def register(username: str, password: str):
    session = SessionLocal()
    user = User(username=username, password=password)
    session.add(user)
    try:
        session.commit()
        return {"message": "User registered successfully"}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        session.close()

@app.post("/login")
def login(username: str, password: str):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    if user and user.password == password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")
