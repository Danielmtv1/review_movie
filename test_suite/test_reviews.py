from fastapi.testclient import TestClient
from main import app
from project.data_base import User, Movie, UserReview
import json

client = TestClient(app)


def test_create_review():
    user = User.create(username="test_user", password="test_password")
    movie = Movie.create(title="test_movie")
    data = {
        "title": movie.title,
        "reviews": "Test review",
        "score": 4,
    }
    response = client.post(
        "/reviews",
        json=data,
        headers={"Authorization": f"Bearer {user.generate_jwt()}"},
    )
    assert response.status_code == 200
    review_response = json.loads(response.content)
    assert review_response["reviews"] == data["reviews"]
    assert review_response["score"] == data["score"]
    assert review_response["user_id"] == user.id
    assert review_response["movie_id"] == movie.id


def test_get_reviews():
    review_1 = UserReview.create(
        user_id=1, movie_id=1, reviews="review 1", score=5)
    review_2 = UserReview.create(
        user_id=2, movie_id=2, reviews="review 2", score=4)
    response = client.get("/reviews")
    assert response.status_code == 200
    reviews_response = json.loads(response.content)
    assert len(reviews_response) == 2
    assert reviews_response[0]["reviews"] == review_1.reviews
    assert reviews_response[0]["score"] == review_1.score
    assert reviews_response[1]["reviews"] == review_2.reviews
    assert reviews_response[1]["score"] == review_2.score


def test_get_review():
    review = UserReview.create(
        user_id=1, movie_id=1, reviews="review 1", score=5)
    response = client.get(f"/reviews/{review.id}")
    assert response.status_code == 200
    review_response = json.loads(response.content)
    assert review_response["reviews"] == review.reviews
    assert review_response["score"] == review.score
    assert review_response["user_id"] == review.user_id
    assert review_response["movie_id"] == review.movie_id
