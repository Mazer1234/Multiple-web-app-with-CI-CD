from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

# Жанры
class Genre(str, Enum):
    ACTION = "action"
    COMEDY = "comedy"
    DRAMA = "drama"
    HORROR = "horror"
    SCIFI = "sci-fi"
    ROMANCE = "romance"
    THRILLER = "thriller"
    FANTASY = "fantasy"

# Базовые модели
class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200) # ... означает обязательное поле
    year: int = Field(..., ge=1900, le=2030)
    genre: Genre
    director: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    duration: int = Field(..., ge=1, le=500) # в минутах
    imdb_rating: float = Field(..., ge=0, le=10)

# Для создания (только данные)
class MovieCreate(MovieBase):
    pass

# Для ответа добавляем id
class Movie(MovieBase):
    id: int
    user_rating: Optional[float] = None # Optional означает что может быть либо float либо None
    total_ratings: int = 0

    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    movie_id: int
    rating: float = Field(..., ge=1, le=10)
    review: Optional[str] = None

class Rating(RatingCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class SearchFilters(BaseModel):
    genre: Optional[Genre] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    min_rating: Optional[float] = None
    director: Optional[str] = None

class RecommendationResponce(BaseModel):
    movie: Movie
    reason: str
    match_score: float
