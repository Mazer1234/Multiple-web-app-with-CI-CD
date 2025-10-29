from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
import redis
import os
import json
from datetime import datetime

from .models import (
    Movie, MovieCreate, RatingCreate, Rating, User, UserCreate,
    SearchFilters, Genre, RecommendationResponce
)

# Конфигурация redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)
# Пока что данные будут хранится в виде массива потом заменю на бд
movies_db = []
ratings_db = []
users_db = []
next_movie_id = 1
next_rating_id = 1
next_user_id = 1


# Добавляем демо данные
def initialize_demo_data():
    global movies_db, next_movie_id

    demo_movies = [
        {
            "title": "Inception",
            "year": 2010,
            "genre": Genre.SCIFI,
            "director": "Christopher Nolan",
            "description": "A thief who steals corporate secrets through dream-sharing technology.",
            "duration": 148,
            "imdb_rating": 8.8
        },
        {
            "title": "The Shawshank Redemption",
            "year": 1994,
            "genre": Genre.DRAMA,
            "director": "Frank Darabont",
            "description": "Two imprisoned men bond over a number of years.",
            "duration": 142,
            "imdb_rating": 9.3
        },
        {
            "title": "The Dark Knight",
            "year": 2008,
            "genre": Genre.ACTION,
            "director": "Christopher Nolan",
            "description": "Batman faces the Joker, a criminal mastermind.",
            "duration": 152,
            "imdb_rating": 9.0
        },
        {
            "title": "Pulp Fiction",
            "year": 1994,
            "genre": Genre.THRILLER,
            "director": "Quentin Tarantino",
            "description": "The lives of two mob hitmen, a boxer, and a pair of diner bandits.",
            "duration": 154,
            "imdb_rating": 8.9
        }
    ]

    for movie_data in demo_movies:
        movie = Movie(
            id=next_movie_id,
            **movie_data
        )
        movies_db.append(movie)
        next_movie_id += 1

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Movie Database application...")
    initialize_demo_data()
    redis_client.set("total_movies", len(movies_db))
    yield
    print("Shutting down FastAPI application...")

app = FastAPI(
    title="Movie Database API",
    description="База данных фильмов с рекомендациями",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_movie_by_id(movie_id: int) -> Optional[Movie]:
    return next((m for m in movies_db if m.id == movie_id), None)

def calculate_movie_rating(movie_id: int):
    movie_ratings = [r.rating for r in ratings_db if r.movie_id == movie_id]
    if movie_ratings:
        return sum(movie_ratings) / len(movie_ratings), len(movie_ratings)
    return None, 0

@app.get("/")
async def root():
    return {
        "message": "🎬 Welcome to Movie Database API!",
        "version": "1.0.0",
        "total_movies": len(movies_db),
        "endpoints": [
            "GET /movies - Поиск фильмов",
            "GET /movies/{id} - Детали фильма",
            "POST /ratings - Добавить оценку",
            "GET /recommendations - Персональные рекомендации",
            "GET /genres - Список жанров"
        ]
    }

@app.get("/health")
async def health_check():
    try:
        redis_client.ping()
        redis_status = "healthy"
    except:
        redis_status = "unhealthy"

    return {
        "status": "healthy",
        "redis": redis_status,
        "total_movies": len(movies_db),
        "total_ratings": len(ratings_db),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/movies", response_model=List[Movie])
async def get_movies(
        genre: Optional[Genre] = None,
        min_year: Optional[int] = Query(None, ge=1900),
        max_year: Optional[int] = Query(None, le=2030),
        min_rating: Optional[float] = Query(None, ge=0, le=10),
        director: Optional[str] = None,
        search: Optional[str] = None
):
    '''Поиск и фильтрация фильмов'''
    filtered_movies = movies_db.copy()

    #применяем фильтры
    if genre:
        filtered_movies = [m for m in filtered_movies if m.genre == genre]
    if min_year:
        filtered_movies = [m for m in filtered_movies if m.year >= min_year]
    if max_year:
        filtered_movies = [m for m in filtered_movies if m.year <= max_year]
    if min_rating:
        filtered_movies = [m for m in filtered_movies if m.rating >= min_rating]
    if director:
        filtered_movies = [m for m in filtered_movies if director.lower() in m.director.lower()]
    if search:
        filtered_movies = [m for m in filtered_movies if search.lower() in m.title.lower()]

    # Добавляем пользовательские рейтинги
    for movie in filtered_movies:
        users_rating, total_ratings = calculate_movie_rating(movie.id)
        if users_rating:
            movie.user_rating = users_rating
            movie.total_ratings = total_ratings
    return filtered_movies

@app.get("/movies/{movie_id}", response_model=Movie)
async def get_movie(movie_id: int):
    """Получить детальную информацию о фильме"""
    movie = get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found") # raise - создание и выброс исключения

    # Добавляем рейтинги
    user_rating, total_ratings = calculate_movie_rating(movie_id)
    if user_rating:
        movie.user_rating = user_rating
        movie.total_ratings = total_ratings

    #Кэшируем просмотры в Redis
    redis_client.zincrby("movie_views", 1, movie_id)

    return movie

@app.post("/ratings", response_model=Rating)
async def create_rating(rating: RatingCreate):
    """Добавить оценку фильму"""
    global next_rating_id

    movie = get_movie_by_id(rating.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Создаем оценку
    new_rating = Rating(
        id = next_rating_id,
        user_id=1,
        **rating.dict(),
        created_at = datetime.utcnow()
    )

    ratings_db.append(new_rating)
    next_rating_id += 1

    # Обновляем кэш
    redis_client.incr("total_ratings")

    return new_rating

@app.get("/recommendations", response_model=List[RecommendationResponce])
async def get_recommendations():
    """Получить персональные рекомендации"""
    recommendations = []

    user_rated_movies = {r.movie_id for r in ratings_db}

    for movie in movies_db[:3]:
        if movie.id not in user_rated_movies:
            reason = "Popular movie you haven't rated yet"
            if movie.imdb_rating >= 8.5:
                reason = "Highly rated movie"
            elif movie.genre == Genre.ACTION:
                reason = "Based on your love for action movies"

            recommendations.append(
                RecommendationResponce(
                    movie=movie,
                    reason=reason,
                    match_score=min(movie.imdb_rating / 10, 0.05)
                )
            )

    return recommendations

@app.get("/genres")
async def get_genre():
    """Получить список всех жанров"""
    return [genre.value for genre in Genre]

@app.get("/stats")
async def get_stats():
    """Статистика базы данных"""
    popular_movies = redis_client.zrevrange("movie_views", 0, 2, withscores=True)

    return {
        "total_movies": len(movies_db),
        "total_ratings": len(ratings_db),
        "most_viewed_movies": [
            {"movie_id": int(mid), "views": int(views)}
            for mid, views in popular_movies
        ],
        "genre_distribution": {
            genre.value: len([m for m in movies_db if m.genre == genre])
            for genre in Genre
        }
    }