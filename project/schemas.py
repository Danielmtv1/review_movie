from typing import Any
from pydantic import BaseModel, validator
from peewee import ModelSelect
from pydantic.utils import GetterDict
from fastapi import HTTPException
# esta clase convierte un objeto en diccionario estudiarla mejor
# esto se denomina serializar si usaramos sqlalchemy no sirve solo para
# peewee ok


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
# --------------------USER-------------------#


class UserRequestModel(BaseModel):
    user_name: str
    password: str

    @validator('user_name')
    def username_validator(cls, user_name):
        if len(user_name) < 3 or len(user_name) > 50:
            raise ValueError(
                "la longitud debe encontrarse entre 3 y 50 caracteres.")
        return user_name


class UserResponseModel(ResponseModel):
    id: int | None
    user_name: str | None  # antes tocaba usar OPTIONAL

# -------------------Movie------------------#


class MovieResponseModel(ResponseModel):
    id: int
    title: str
# -------------------Review------------------#


class Review_Validator():
    @validator('score')
    def score_validator(cls, score):

        if score < 0 or score > 5:
            raise HTTPException(409,
                                "the score range is an integer between 0 and 5")
        return score


# response model se encarga de serializar el objeto en json


class ReviewRequestPutModel(BaseModel, Review_Validator):
    review: str
    score: int


class MovieResponseApiModel(ResponseModel):
    imdbID: str | None
    title: str
    year: str | None
    genre: str | None
    director: str | None
    actors: str | None
    plot: str | None
    poster: str | None


class MovieResponsesApiModel(ResponseModel):

    Title: str
    Year: str | None
    Genre: str | None
    Director: str | None
    Actors: str | None
    Plot: str | None
    Poster: str | None
    imdbID: str | None


class ReviewResponseModel(ResponseModel):

    movie: MovieResponseApiModel  # objeto relacionado cool
    reviews: str
    score: int

    @validator('score')
    def score_validator(cls, score):

        if score < 0 or score > 5:
            raise HTTPException(409,
                                "the score range is an integer between 0 and 5")
        return score


class ReviewRequestMovie(BaseModel, Review_Validator):

    title: str
    reviews: str
    score: int
