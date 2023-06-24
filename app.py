from fastapi import FastAPI, Request, Response, HTTPException
import uvicorn
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from models.schemas import UserBase, UserUpdate

# Models

# Create Base from sqlalchemy
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    photo = Column(String, nullable=True)
    hobbies = relationship('Hobby', backref='user')

class Hobby(Base):
    __tablename__ = 'hobby'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String)

engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

@app.get('/')
async def index():
    # get all User left join hobby
    users = session.query(User).all()
    for item in users:
        print(item.username, item.photo, item.hobbies)
    return {"message": users}

@app.post('/user')
async def create_user(response: Response, user: UserBase):
    # Insert user to database
    new_user = User(username=user.username, password=user.password, photo=user.photo)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created", "user": new_user}


@app.put('/user')
async def update_user(user: UserUpdate):
    # update user with user.id
    user_id = user.id
    user_to_update = session.query(User).filter_by(id=user_id).first()
    user_to_update.password = user.password
    user_to_update.photo = user.photo
    session.commit()
    session.refresh(user_to_update)
    return {"message": "User updated", "user": user_to_update}

@app.delete('/user')
async def delete_user(user_id: int):
    # Check if that user is having any hobby
    user_to_delete = session.query(User).filter_by(id=user_id).first()
    if user_to_delete.hobbies:
        raise HTTPException(status_code=400, detail="User has hobbies")
    
    # Delete user
    session.delete(user_to_delete)
    session.commit()
    return {'message':"User Deleted"}


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # Run the app using the Uvicorn server. We've set reload=True so that
    # any changes to our code will automatically be reloaded.
    uvicorn.run(app, port=5000)