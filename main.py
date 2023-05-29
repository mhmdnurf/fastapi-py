from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from sqlalchemy.orm import sessionmaker
from models import Base, User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine

app = FastAPI()
db_url = "mysql+mysqlconnector://root:crack_@34.101.145.22/crack-db"
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

bearer = HTTPBearer()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@app.get("/")
def dashboard(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return {"message": "Anda telah terautentikasi"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Autentikasi gagal")

@app.post("/register")
def register(nama_lengkap: str, username: str, password: str, alamat: str):
    session = SessionLocal()
    user = User(nama_lengkap=nama_lengkap, username=username, password=password, alamat=alamat)
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
        # Generate JWT token
        token = jwt.encode({"username": username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3001)