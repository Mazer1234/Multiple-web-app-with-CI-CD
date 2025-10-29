import React from 'react';
import MovieCard from './MovieCard';
import './MovieList.css';

const MovieList = ({ movies, onRatingAdded }) => {
    if (movies.length === 0) {
        return <div className='no-movies'>No movies found. Try different filters</div>
    }

    return (
        <div className='movie-list'>
            {movies.map(movie => (
                <MovieCard
                    key={movie.id}
                    movie={movie}
                    onRatingAdded={onRatingAdded}
                />
            ))}
        </div>
    );
};

export default MovieList;