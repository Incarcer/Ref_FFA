import React, { createContext, useState, useEffect, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import { getCurrentUser, logoutUser } from './services/api';


import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import SettingsPage from './components/SettingsPage';
import LeaguesPage from './components/LeaguesPage';


const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const verifyUser = async () => {
            try {
                const response = await getCurrentUser();
                setUser(response.data);
            } catch (error) {
                setUser(null);
            } finally {
                setLoading(false);
            }
        };
        verifyUser();
    }, []);

    const login = (userData) => setUser(userData);

    const logout = async () => {
        await logoutUser();
        setUser(null);
    };

    const authValue = { user, loading, login, logout };

    return (
        <AuthContext.Provider value={authValue}>
            {!loading && children}
        </AuthContext.Provider>
    );
};


const PrivateRoute = ({ children }) => {
    const { user } = useAuth();
    if (!user) {
        return <Navigate to="/login" replace />;
    }
    return children;
};


function AppLayout() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    return (
        <>
            <nav style={{ padding: '1rem', background: '#f0f0f0', borderBottom: '1px solid #ccc' }}>
                <Link to="/">Home</Link> | {' '}
                {user ? (
                    <>
                        <Link to="/leagues">My Leagues</Link> | {' '}
                        <Link to="/settings">Settings</Link> | {' '}
                        <button onClick={handleLogout} style={{all: 'unset', cursor: 'pointer', color: 'blue', textDecoration: 'underline'}}>Logout ({user.email})</button>
                    </>
                ) : (
                    <>
                        <Link to="/login">Login</Link> | {' '}
                        <Link to="/register">Register</Link>
                    </>
                )}
            </nav>
            <hr />
            <main style={{ padding: '1rem' }}>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    
                    {/* Protected Routes */}
                    <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
                    <Route path="/settings" element={<PrivateRoute><SettingsPage /></PrivateRoute>} />
                    <Route path="/leagues" element={<PrivateRoute><LeaguesPage /></PrivateRoute>} />

                    {/* Fallback to home */}
                    <Route path="*" element={<Navigate to="/" />} />
                </Routes>
            </main>
        </>
    );
}


function App() {
    return (
        <Router>
            <AuthProvider>
                <AppLayout />
            </AuthProvider>
        </Router>
    );
}

export default App;