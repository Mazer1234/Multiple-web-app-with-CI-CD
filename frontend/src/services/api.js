import axios from 'axios';

const API_BASE_URL = "/api";

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const movieAPI = {
    getMovies: (filters = {}) => api.get('/movies', { params: filters}),
    getMovie: (id) => api.get(`/movies/${id}`),
    addRating: (ratingData) => api.post("/ratings", ratingData),
    getRecommendations: () => api.get('/recommendations'),
    getStats: () => api.get('/stats'),
    getGenres: () => api.get('/genres')
};

