import React, { useState } from "react";
import './RatingForm';

const RatingForm = ({ onSubmit }) => {
    const [rating, setRating] = useState(5);
    const [review, setReview] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('📝 Form data:', { rating, review });
        onSubmit({ rating: parseFloat(rating), review });
    };

    return (
        <form className="rating-form" onSubmit={handleSubmit}>
            <div className="form-group">
                <label>Rating (1-10):</label>
                <input
                    type="number"
                    min="1"
                    max="10"
                    step="0.1"
                    value={rating}
                    onChange={(e) => setRating(parseFloat(e.target.value) || 5)}
                    required
                />
            </div>

            <div className="form-group">
                <label>Review (optional):</label>
                <textarea
                    value={review}
                    onChange={(e) => setReview(e.target.value)}
                    placeholder="Your thoughts about the movie..."
                    rows="3"
                />
            </div>

            <button type="submit">Submit Rating</button>
        </form>
    );
};

export default RatingForm;