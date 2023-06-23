from fastapi import FastAPI, Request
import uvicorn
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Models

# Create Base from sqlalchemy
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    photo = Column(String, nullable=True)

engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

@app.get('/')
async def index():
    # get all User
    users = session.query(User).all()
    return {"message": users}

@app.post('/user')
async def create_user(request: Request):
    # Create User
    data = await request.json()
    if "username" not in data:
        return {"message": "username is required"},400
    print(data)
    return {"message": "User created"}

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # Run the app using the Uvicorn server. We've set reload=True so that
    # any changes to our code will automatically be reloaded.
    uvicorn.run(app, port=5000)