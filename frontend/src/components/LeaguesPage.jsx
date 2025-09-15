import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { fetchYahooLeagues } from '../services/api';

const LeaguesPage = () => {
    const [leagues, setLeagues] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const getLeagues = useCallback(async () => {
        setIsLoading(true);
        setError('');
        try {
            const response = await fetchYahooLeagues();
            setLeagues(response.data.leagues || []);
        } catch (err) {
            if (err.response?.status === 401) {
                setError('Your Yahoo account is not linked.');
            } else {
                setError('An error occurred while fetching your leagues.');
            }
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {

        getLeagues();
    }, [getLeagues]);

    if (isLoading) return <div>Loading your leagues...</div>;

    if (error) {
        return (
            <div>
                <p style={{ color: 'red' }}>{error}</p>
                <p>Go to <Link to="/settings">Account Settings</Link> to link your account.</p>
            </div>
        );
    }

    return (
        <div>
            <h2>Your Yahoo Fantasy Leagues</h2>
            {leagues.length > 0 ? (
                <table>
                    <thead>
                        <tr>
                            <th>League Name</th>
                            <th>Season</th>
                        </tr>
                    </thead>
                    <tbody>
                        {leagues.map((league) => (
                            <tr key={league.league_key}>
                                <td><a href={league.url} target="_blank" rel="noopener noreferrer">{league.name}</a></td>
                                <td>{league.season}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No fantasy football leagues found for your linked Yahoo account.</p>
            )}
        </div>
    );
};

export default LeaguesPage;