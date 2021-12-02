from typing import NoReturn, Text
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.params import Body, Depends
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.selectable import ReturnsRows 
from starlette import status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

import psycopg2

models.Base.metadata.create_all(bind=engine)

api = FastAPI()

try:
    connection = psycopg2.connect(host='hostname', database='name', user='username', password='password', cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print("Database connection is successfull!")
except Exception as error:
    print("Connection error")
    print('Error: ', error)

@api.get('/user/{username}', response_model=schemas.User)
def get_individual_user(username: str, db: Session = Depends(get_db)):
    get_individual_user = db.query(models.User).filter(models.User.username == username).first()
    if not get_individual_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with {username}.")
    return get_individual_user

@api.get('/users')
def test(db: Session = Depends(get_db)):
    get_users = db.query(models.User).all()
    return get_users

@api.post('/create_account')
def create_account(user: schemas.CreateUserAccount, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@api.put('/update_account/{username}')
def update_account(username: str, modify_user: schemas.UpdateUserAccount, db: Session = Depends(get_db)):
    post = db.query(models.User).filter(models.User.username == username)
    user = post.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail=f"Not updated")
    post.update(modify_user.dict(), synchronize_session=False)
    db.commit()
    return "updated successfully"

@api.delete('/delete_account/{username}')
def delete_account(username: str, db: Session = Depends(get_db)):
    delete_user = db.query(models.User).filter(models.User.username == username)
    if delete_user.first() == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No user exist with {username}.")
    delete_user.delete(synchronize_session=False)
    db.commit()
    return f"{username}, your account is successfully deleted."
