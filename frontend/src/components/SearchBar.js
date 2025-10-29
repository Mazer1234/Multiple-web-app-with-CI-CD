import React, { useState } from "react";
import { movieAPI } from "../services/api";
import './SearchBar.css';

const SearchBar = ({ onFilterChange}) => {
    const [search, setSearch] = useState('');
    const [genre, setGenre] = useState('');
    const [genres, setGenres] = useState([]);

    React.useEffect(() => {
        movieAPI.getGenres().then(responce => {
            setGenres(responce.data);
        });
    }, []);

    const handleSearchChange = (e) => {
        setSearch(e.target.value);
        onFilterChange({ search, genre: e.target.value });
    };

    return (
        <div className="search-bar">
            <input 
                type="text"
                placeholder="Search movies..."
                value={search}
                onChange={handleSearchChange}
            />
            <select value={genre} onChange={handleSearchChange}>
                <option value=''>All Genres</option>
                {genres.map(g => (
                    <option key={g} value={g}>{g}</option>
                ))}
            </select>
        </div>
    );
};

export default SearchBar;