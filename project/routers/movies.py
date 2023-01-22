from project.data_base import Movie
from project.schemas import MovieResponseApiModel, MovieResponsesApiModel
from fastapi import APIRouter, HTTPException
import requests

router = APIRouter(prefix="/movies", tags=["Movies"])

OMDB_API_KEY = '10bd0f51'
OMDB_API_URL = 'http://www.omdbapi.com/'


def get_movie_data(title: str):
    url = f"{OMDB_API_URL}?apikey={OMDB_API_KEY}&t={title}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=response.text)
    return response.json()


@router.get("", response_model=MovieResponsesApiModel)
async def get_movie(tittle: str):
    return get_movie_data(tittle)


@router.post("", response_model=MovieResponseApiModel)
def create_movie(title: str):
    movie_data = get_movie_data(title)

    if Movie.select().where(Movie.title == movie_data['Title']):
        raise HTTPException(status_code=409, detail="movie exist")
    else:
        movie_create = Movie.create(
            imdbID=movie_data['imdbID'],
            title=movie_data['Title'],
            year=movie_data['Year'],
            genre=movie_data['Genre'],
            director=movie_data['Director'],
            actors=movie_data['Actors'],
            plot=movie_data['Plot'],
            poster=movie_data['Poster'],
        )
        return movie_create
