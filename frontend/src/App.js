import React, { useState, useEffect} from 'react';
import MovieList from './components/MovieList';
import SearchBar from './components/SearchBar';
import './App.css';
import { movieAPI } from './services/api';

function App() {
  const [movies, setMovies] = useState([]);
  const [filters, setFilters] = useState({});

  useEffect(() => {
    loadMovies();
  }, [filters]);

  const loadMovies = async () => {
    try {
      const responce = await movieAPI.getMovies(filters);
      setMovies(responce.data);
    }catch (error) {
      console.error('Error loading Movies: ', error);
    }
  };

  return (
    <div className='App'>
      <header className='App-header'>
        <h1> Movie DataBase</h1>
        <SearchBar onFilterChange={setFilters} />
      </header>
      <main>
        <MovieList movies={movies} onRatingAdded={loadMovies}/>
      </main>

    </div>
  );
}

export default App;
