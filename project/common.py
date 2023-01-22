import jwt
from fastapi import Depends, HTTPException, status
from project.data_base import User
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from local_settings import SECRET_KEY1
# import os

# SECRET_KEY = os.environ.get("SECRET_KEY")

# def create_access_token(user, days: int = 7):
#    data = {
#        "user_id": user.id,
#        "user_name": user.user_name,
#        "exp": datetime.utcnow() + timedelta(days=days),
#    }
#    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

SECRET_KEY = SECRET_KEY1

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")

# this function create and encode token jwt


def create_access_token(user, days: int = 7):
    data = {
        "user_id": user.id,
        "user_name": user.user_name,
        "exp": datetime.utcnow() + timedelta(days=days),
    }
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


# this function decode token jwt


def decode_access_token(token):

    try:
        return jwt.decode(token, SECRET_KEY, algorithms="HS256")

    except Exception as err:
        return None


# this function decode token an dreturn  the user and id


def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    data = decode_access_token(token)
    print(data)
    if data:
        return User.select().where(User.id == data["user_id"]).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not valid ",
            headers={"WWWW.AUTENTICATE": "Beraer"},
        )
