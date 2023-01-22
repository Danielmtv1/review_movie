from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from project.data_base import User, Movie, UserReview
from project.data_base import database as connection
from .routers import user_router, review_router, movie_router
from project.common import create_access_token
import logging


tags_metadata = [
    {
        "name": "Reviews",
        "description": "End Points Reviews",
    },
    {
        "name": "Users",
        "description": "End points for Users",
    },
    {
        "name": "Movies",
        "description": "End points for Movies"
    }
]


app = FastAPI(

    title="Proyecto para reseñar peliculas",
    description=" Es un proyecto para reseñar peliculas ",
    version="1",
    contact={
            "name": "Jaime Daniel Cabrera",
            "email": "danielmtv6@gmail.com"
    },
    openapi_tags=tags_metadata,
)


api_v1 = APIRouter(prefix="/api/v1")


api_v1.include_router(user_router)
api_v1.include_router(review_router)
api_v1.include_router(movie_router)


@api_v1.post("/auth")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(form_data.username, form_data.password)

    if user:
        logging.info("user ok")
        return {
            "access_token": create_access_token(user),
            "token:type": "Bearer"
        }
    else:
        logging.exception("user unauthorized")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="USERNAME OR PASSWORD FAIL",
            headers={"WWWW.AUTENTICATE": "Beraer"},
        )


app.include_router(api_v1)


@app.on_event("startup")
def startup():
    if connection.is_closed():
        connection.connect
        print("connecting...")
    connection.create_tables(
        [
            User,
            Movie,
            UserReview,
        ]
    )


@app.on_event("shutdown")
def shutdown():
    if not connection.is_closed():
        connection.close()
        print("closing")
