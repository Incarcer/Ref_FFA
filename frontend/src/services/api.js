import axios from 'axios';


const apiClient = axios.create({
    baseURL: '/api/v1',
    withCredentials: true, // Crucial for sending HttpOnly cookies
});


export const registerUser = (userData) => {

    return apiClient.post('/auth/register', userData);
};

export const loginUser = (credentials) => {

    const params = new URLSearchParams();
    params.append('username', credentials.email);
    params.append('password', credentials.password);
    return apiClient.post('/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
};

export const logoutUser = () => {
    return apiClient.post('/auth/logout');
};

export const getCurrentUser = () => {
    return apiClient.get('/auth/users/me');
};



export const getYahooAuthUrl = () => {
    return apiClient.get('/yahoo/auth');
};

export const checkYahooStatus = () => {
    return apiClient.get('/yahoo/status');
};

export const fetchYahooLeagues = () => {
    return apiClient.get('/yahoo/leagues');
};

export default apiClient;