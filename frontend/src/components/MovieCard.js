import React, { useState } from "react";
import { movieAPI } from "../services/api";
import RatingForm from './RatingForm';
import './MovieCard.css';

const MovieCard = ({ movie, onRatingAdded }) => {
    const [showRatingForm, setShowRatingForm] = useState(false);

    const handleAddRating = async (ratingData) => {
        try {
            await movieAPI.addRating({
                movie_id: Number(movie.id),
                rating: Number(ratingData.rating),
                review: ratingData.review || null
            });
            setShowRatingForm(false);
            onRatingAdded(); // Уведомляем род. компонент
        } catch (error) {
            console.error('❌ Full error:', error);
            console.error('📝 Error response:', error.response);
            console.error('🔍 Error data:', JSON.stringify(error.response?.data, null, 2));
            alert(`Failed to add rating: ${JSON.stringify(error.response?.data)}`);
        }
    };

    return (
        <div className="movie-card">
            <div className="movie-header">
                <h3>{movie.title} ({movie.year})</h3>
                <div className="movie-rating">
                    {movie.imdb_rating}/10
                    {movie.user_rating && (
                        <span className="user-rating">{movie.user_rating}/10</span>
                    )}
                </div>
            </div>

            <div className="movie-details">
                <p><strong>Director:</strong> {movie.director}</p>
                <p><strong>Genre:</strong> {movie.genre}</p>
                <p><strong>Duration:</strong> {movie.duration} min</p>
                {movie.description && (
                    <p className="movie-description">{movie.description}</p>
                )}
            </div>

            <button
                className="rate-button"
                onClick={() => setShowRatingForm(!showRatingForm)}
            >
                {showRatingForm ? 'Cancel' : 'Rate Movie'}
            </button>

            {showRatingForm && (
                <RatingForm onSubmit={handleAddRating} />
            )}
        </div>
    );
};

export default MovieCard;