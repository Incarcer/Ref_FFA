import React, { useState, useEffect, createContext, useContext } from 'react';
import { Routes, Route, Link } from 'react-router-dom';

import HomePage from './pages/HomePage';
import LeaguePage from './pages/LeaguePage';
import WaiverWirePage from './pages/WaiverWirePage';
import TradeAnalyzerPage from './pages/TradeAnalyzerPage';
import { fetchCurrentUser } from './services/api';

const AuthContext = createContext(null);
export const useAuth = () => useContext(AuthContext);

function App() {
  const [user, setUser] = useState(null);
  const [loadingAuth, setLoadingAuth] = useState(true);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const userData = await fetchCurrentUser();
        setUser(userData);
      } catch (error) {
        setUser(null);
      } finally {
        setLoadingAuth(false);
      }
    };

    checkAuthStatus();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, loadingAuth }}>
      <div className="bg-gray-900 text-white min-h-screen">
        <header className="p-4 bg-gray-950 border-b border-gray-800 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Yahoo Fantasy Football Analyst</h1>
          <nav className="flex gap-6 items-center">
            <Link to="/" className="text-gray-300 hover:text-white transition-colors">Home</Link>
            <Link to="/leagues" className="text-gray-300 hover:text-white transition-colors">Leagues</Link>
            <Link to="/waiver-wire" className="text-gray-300 hover:text-white transition-colors">Waiver Wire</Link>
            <Link to="/trade-analyzer" className="text-gray-300 hover:text-white transition-colors">Trade Analyzer</Link>
          </nav>
        </header>
        <main className="p-4 md:p-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/leagues" element={<LeaguePage />} />
            <Route path="/waiver-wire" element={<WaiverWirePage />} />
            <Route path="/trade-analyzer" element={<TradeAnalyzerPage />} />
          </Routes>
        </main>
      </div>
    </AuthContext.Provider>
  );
}

export default App;
