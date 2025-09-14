import React, { useState, useEffect } from 'react';
import { useAuth } from '../App';
import { fetchLeagues } from '../services/api';

const LeaguePage = () => {
  const { user } = useAuth();
  const [leagues, setLeagues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (user) {
      const loadLeagues = async () => {
        try {
          setLoading(true);
          const data = await fetchLeagues();
          setLeagues(data.leagues || []);
          setError(null);
        } catch (err) {
          console.error('Failed to fetch leagues:', err);
          setError('Failed to load league data. Your session may have expired. Please try logging in again.');
          setLeagues([]);
        } finally {
          setLoading(false);
        }
      };
      loadLeagues();
    } else {
      setLoading(false);
      setLeagues([]);
    }
  }, [user]);

  if (loading) {
    return (
      <div className="text-center p-8">
        <p className="text-lg">Loading leagues...</p>
      </div>
    );
  }

  if (!user) {
    return (
        <div className="p-8 bg-gray-800 rounded-lg shadow-lg text-center">
            <h1 className="text-2xl font-bold mb-4">Leagues</h1>
            <p className="text-gray-400">Please log in to view your fantasy leagues.</p>
        </div>
    );
  }

  if (error) {
    return <div className="p-8 bg-red-900/50 border border-red-700 rounded-lg shadow-lg text-center text-red-300">{error}</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">My Fantasy Leagues</h1>
      {leagues.length > 0 ? (
        <div className="space-y-8">
          {leagues.map(league => (
            <div key={league.league_key} className="bg-gray-800 p-6 rounded-lg shadow-lg transition-all hover:bg-gray-700/50">
              <h2 className="text-2xl font-semibold mb-4 text-white">{league.name}</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-xl font-medium mb-3 border-b border-gray-700 pb-2 text-blue-400">Standings</h3>
                  <p className="text-gray-400 italic">Standings data will be displayed here.</p>
                </div>
                <div>
                  <h3 className="text-xl font-medium mb-3 border-b border-gray-700 pb-2 text-blue-400">Team Rosters</h3>
                  <p className="text-gray-400 italic">Team roster details will be displayed here.</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-8 bg-gray-800 rounded-lg shadow-lg text-center">
            <p className="text-gray-400">No fantasy football leagues found for your account.</p>
        </div>
      )}
    </div>
  );
};

export default LeaguePage;
