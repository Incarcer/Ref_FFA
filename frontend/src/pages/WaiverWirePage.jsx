import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getWaiverWire } from '../services/api';

const WaiverWirePage = () => {
  const { leagueKey } = useParams();
  const [availablePlayers, setAvailablePlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWaiverData = async () => {
      if (!leagueKey) {
        setLoading(false);
        setError("League key is not available in the URL.");
        return;
      }
      try {
        setLoading(true);
        const data = await getWaiverWire(leagueKey);
        setAvailablePlayers(data || []);
        setError(null);
      } catch (err) {
        setError('Failed to fetch waiver wire data. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchWaiverData();
  }, [leagueKey]);

  const renderTableBody = () => {
    if (loading) {
      return (
        <tr>
          <td colSpan="5" className="text-center py-8 text-gray-400">Loading available players...</td>
        </tr>
      );
    }

    if (error) {
      return (
        <tr>
          <td colSpan="5" className="text-center py-8 text-red-500">{error}</td>
        </tr>
      );
    }

    if (!availablePlayers || availablePlayers.length === 0) {
      return (
        <tr>
          <td colSpan="5" className="text-center py-8 text-gray-400">No players available on the waiver wire.</td>
        </tr>
      );
    }

    return availablePlayers.map((player) => (
      <tr key={player.id} className="border-b border-gray-700 hover:bg-gray-700/50">
        <th scope="row" className="px-6 py-4 font-medium text-white whitespace-nowrap">
          {player.name}
        </th>
        <td className="px-6 py-4">{player.position}</td>
        <td className="px-6 py-4">{player.team}</td>
        <td className="px-6 py-4 text-green-400">5-10%</td>
        <td className="px-6 py-4">
          <button className="font-medium text-blue-500 hover:underline">Add to Watchlist</button>
        </td>
      </tr>
    ));
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">Waiver Wire Assistant</h1>
      
      <div className="bg-gray-800 p-4 rounded-lg flex flex-wrap gap-4 items-center">
        <input 
          type="text" 
          placeholder="Search player..." 
          className="bg-gray-700 text-white placeholder-gray-400 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <select className="bg-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="">All Positions</option>
          <option value="QB">QB</option>
          <option value="RB">RB</option>
          <option value="WR">WR</option>
          <option value="TE">TE</option>
          <option value="K">K</option>
          <option value="DEF">DEF</option>
        </select>
        <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition-colors">
          Apply Filters
        </button>
      </div>

      <div className="overflow-x-auto bg-gray-800 rounded-lg">
        <table className="min-w-full text-sm text-left text-gray-300">
          <thead className="bg-gray-900 text-xs text-gray-400 uppercase">
            <tr>
              <th scope="col" className="px-6 py-3">Player</th>
              <th scope="col" className="px-6 py-3">Position</th>
              <th scope="col" className="px-6 py-3">Team</th>
              <th scope="col" className="px-6 py-3">Recommended FAAB %</th>
              <th scope="col" className="px-6 py-3">Action</th>
            </tr>
          </thead>
          <tbody>
            {renderTableBody()}
          </tbody>
        </table>
      </div>
      <p className="text-gray-500 italic">This page will help users find the best available players on the waiver wire based on their team's needs.</p>
    </div>
  );
};

export default WaiverWirePage;
