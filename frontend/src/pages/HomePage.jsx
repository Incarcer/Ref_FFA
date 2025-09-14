import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../App';

const HomePage = () => {
  const { user, loadingAuth } = useAuth();

  const handleLogin = () => {
    window.location.href = '/auth/yahoo';
  };

  if (loadingAuth) {
    return (
      <div className="text-center p-8">
        <p className="text-lg">Authenticating...</p>
      </div>
    );
  }

  if (user) {
    return (
      <div className="text-center p-8 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Welcome back, {user.name}!</h2>
        <p className="mb-6 text-gray-400">
          You are successfully logged in. Explore your leagues and gain an edge.
        </p>
        <div className="flex justify-center gap-4">
          <Link
            to="/leagues"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-transform transform hover:scale-105"
          >
            View My Leagues
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="text-center p-8 bg-gray-800 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">Welcome to the Yahoo Fantasy Football Analyst</h2>
      <p className="mb-6 text-gray-400">
        Gain a competitive edge in your fantasy league. Log in with your Yahoo account to analyze your leagues, get waiver wire recommendations, and evaluate trades.
      </p>
      <button
        onClick={handleLogin}
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-transform transform hover:scale-105"
      >
        Login with Yahoo
      </button>
    </div>
  );
};

export default HomePage;
