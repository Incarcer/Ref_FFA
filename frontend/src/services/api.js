import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1', // Proxied by Vite to the backend
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchCurrentUser = async () => {
  try {
    const response = await apiClient.get('/users/me');
    return response.data;
  } catch (error) {

    throw error;
  }
};

export const fetchLeagues = async () => {
  try {
    const response = await apiClient.get('/leagues');
    return response.data;
  } catch (error) {
    console.error('Error fetching leagues:', error);
    throw error;
  }
};

export const getWaiverWire = async (leagueKey) => {
  try {
    const response = await apiClient.get(`/leagues/${leagueKey}/waiver-wire`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching waiver wire for league ${leagueKey}:`, error);
    throw error;
  }
};

export const fetchAllPlayers = async () => {
    try {
        const response = await apiClient.get('/players');
        return response.data;
    } catch (error) {
        console.error('Error fetching players:', error);
        throw error;
    }
};

export const analyzeTrade = async (tradeData) => {
    try {
        const response = await apiClient.post('/trades/analyze', tradeData);
        return response.data;
    } catch (error) {
        console.error('Error analyzing trade:', error);
        throw error;
    }
};
