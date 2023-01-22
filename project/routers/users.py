from project.data_base import User
from project.schemas import UserRequestModel, UserResponseModel, ReviewResponseModel
from fastapi import HTTPException, APIRouter, Response, Depends
from fastapi.security import HTTPBasicCredentials
from typing import List
from project.common import get_current_user

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("", response_model=UserResponseModel)
def create_user(user: UserRequestModel):
    if User.select().where(User.user_name == user.user_name).exists():
        raise HTTPException(409, "username in use!! try again.")

    hash_password = User.create_password(user.password)

    user = User.create(user_name=user.user_name,
                       password=hash_password
                       )
    return user
# se serializa el peewee permitiendo que el user retorne un json de lo contrario
# deberiamos usar Userresponsemodel(username_id=userresponsemodel.user_name, id= userrespoinsemodel.id )


@router.post('/login', response_model=UserResponseModel)
def loginuser(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.user_name == credentials.username).first()

    if user is None:
        raise HTTPException(404, 'User not found')

    if user.password != User.create_password(credentials.password):
        raise HTTPException(404, "password error")

    response.set_cookie(key='user_id', value=user.id)  # TOKEN
    return user
 # endpoint de autenticacion  basiccredentials es un modelo de fast para evitar crear uno


"""
@router.get('/reviews')
async def get_reviews(user_id: int = Cookie(None)):  # leercoockie
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(404, 'user no found')

    return [user_review for user_review in user.reviews]
"""


@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user: User = Depends(get_current_user)):  # leertoken

    return [user_review for user_review in user.reviews]
