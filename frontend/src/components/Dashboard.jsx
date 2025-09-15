import React from 'react';
import { useAuth } from '../App';

const Dashboard = () => {
    const { user } = useAuth();

    return (
        <div>
            <h1>Welcome, {user?.full_name || 'User'}!</h1>
            <p>This is your main dashboard. You can view your fantasy sports information here.</p>
        </div>
    );
};

export default Dashboard;