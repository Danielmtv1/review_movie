from typing import List
from fastapi import APIRouter, Depends, HTTPException
from project.data_base import User, Movie, UserReview
from project.schemas import (
    ReviewRequestMovie,
    ReviewResponseModel,
    ReviewRequestPutModel,

)
from common import get_current_user
from ..routers.movies import create_movie

router = APIRouter(prefix="/reviews", tags=["Reviews"])


def _create_movie_if_not_exist(title: str) -> None:
    if not Movie.select().where(Movie.title == title).exists():
        try:
            create_movie(title)
        except:
            raise HTTPException(status_code=409, detail="movie not found")


@router.post("", response_model=ReviewResponseModel,)
async def create_review(
    review_request: ReviewRequestMovie, user: User = Depends(get_current_user)
):
    _create_movie_if_not_exist(review_request.title)

    movie = Movie.get(title=review_request.title)
    user_review = UserReview.create(
        user_id=user.id,
        movie_id=movie.id,
        reviews=review_request.reviews,
        score=review_request.score,
    )
    return user_review


@router.get("", response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit)
    return [review for review in reviews]


@router.get("/{review_id}", response_model=ReviewResponseModel)
async def get_review(review_id: int):
    user_review = UserReview.get_or_none(UserReview.id == review_id)
    if not user_review:
        raise HTTPException(status_code=404, detail="review not found")
    return user_review


@router.put("/{review_id}", response_model=ReviewResponseModel)
async def update_review(
    review_id: int,
    review_request: ReviewRequestPutModel,
    user: User = Depends(get_current_user),
):
    user_review = UserReview.get_or_none(UserReview.id == review_id)
    if not user_review:
        raise HTTPException(status_code=404, detail="review not found")
    if user_review.user_id != user.id:
        raise HTTPException(status_code=404, detail="you are not owner")

    user_review.reviews = review_request.review
    user_review.score = review_request.score

    user_review.save()
    return user_review


@router.delete("/{review_id}", response_model=ReviewResponseModel)
async def delete_review(review_id: int, user: User = Depends(get_current_user)):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review.user_id != user.id:
        raise HTTPException(status_code=404, detail='you are not owner')
    user_review.delete_instance()
    return user_review
