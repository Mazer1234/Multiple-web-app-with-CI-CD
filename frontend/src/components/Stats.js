import React, { useState, useEffect } from "react";
import { movieAPI } from "../services/api";
import './Stats.css';

const Stats = () => {
    const [stats, setStats] = useState(null);

    useEffect(() => {
        movieAPI.getStats().then(responce => {
            setStats(responce.data);
        });
    }, []);

    if (!stats) return null;

    return (
        <div className="stats">
            <h3>📊 Database Stats</h3>
            <p><strong>Total Movies:</strong> {stats.total_movies}</p>
            <p><strong>Total Ratings:</strong> {stats.total_ratings}</p>
            <p><strong>Genres:</strong> {Object.keys(stats.genre_distribution).join(', ')}</p>
        </div>
    );
};

export default Stats;