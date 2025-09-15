import React, { useState, useEffect, useCallback } from 'react';
import { checkYahooStatus, getYahooAuthUrl } from '../services/api';

const SettingsPage = () => {
    const [yahooLinked, setYahooLinked] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchStatus = useCallback(async () => {
        try {
            const response = await checkYahooStatus();
            setYahooLinked(response.data.is_linked);
        } catch (err) {
            setError('Failed to fetch Yahoo account status.');
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchStatus();
    }, [fetchStatus]);

    const handleLinkYahoo = async () => {
        setError('');
        try {
            const response = await getYahooAuthUrl();

            window.location.href = response.data.authorization_url;
        } catch (err) {
            setError('Could not start the Yahoo linking process. Please try again.');
        }
    };

    const renderStatus = () => {
        if (isLoading) return <p>Loading account status...</p>;
        if (error) return <p style={{ color: 'red' }}>{error}</p>;
        if (yahooLinked) {
            return <p style={{ color: 'green' }}>✓ Yahoo Account Linked Successfully</p>;
        }
        return <button onClick={handleLinkYahoo}>Link Yahoo Fantasy Account</button>;
    };

    return (
        <div>
            <h2>Account Settings</h2>
            <h3>Integrations</h3>
            {renderStatus()}
        </div>
    );
};

export default SettingsPage;