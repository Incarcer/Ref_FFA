import React, { useState, useEffect, useMemo } from 'react';
import { fetchAllPlayers, analyzeTrade } from '../services/api';

const PlayerSearch = ({ onPlayerSelect, availablePlayers }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    if (searchTerm.length > 1) {
      const filtered = availablePlayers.filter(p => 
        p.full_name.toLowerCase().includes(searchTerm.toLowerCase())
      ).slice(0, 5);
      setSearchResults(filtered);
    } else {
      setSearchResults([]);
    }
  }, [searchTerm, availablePlayers]);

  const handleSelect = (player) => {
    onPlayerSelect(player);
    setSearchTerm('');
    setSearchResults([]);
  };

  return (
    <div className="relative">
      <input
        type="text"
        placeholder="Add player..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full bg-gray-700 text-white placeholder-gray-400 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      {searchResults.length > 0 && (
        <ul className="absolute z-10 w-full bg-gray-800 border border-gray-700 rounded-md mt-1 max-h-60 overflow-y-auto">
          {searchResults.map(player => (
            <li 
              key={player.player_id}
              onClick={() => handleSelect(player)}
              className="px-3 py-2 hover:bg-gray-700 cursor-pointer"
            >
              {player.full_name} <span className="text-gray-400 text-sm">({player.position})</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};


const PlayerTradeCard = ({ title, players, onAddPlayer, onRemovePlayer, availablePlayers }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-lg w-full">
      <h3 className="text-xl font-semibold mb-4 text-white">{title}</h3>
      <div className="space-y-4">
        <PlayerSearch onPlayerSelect={onAddPlayer} availablePlayers={availablePlayers} />
        <ul className="space-y-2 min-h-[60px]">
          {players.map(player => (
            <li key={player.player_id} className="bg-gray-900 p-3 rounded-md flex justify-between items-center animate-fade-in">
              <span>{player.full_name} <span className="text-gray-400 text-sm">({player.position})</span></span>
              <button onClick={() => onRemovePlayer(player)} className="text-red-500 hover:text-red-400">&times;</button>
            </li>
          ))}
          {players.length === 0 && <p className="text-gray-500 text-center py-4">No players added.</p>}
        </ul>
      </div>
    </div>
  );
};


const TradeAnalyzerPage = () => {
  const [allPlayers, setAllPlayers] = useState([]);
  const [teamGive, setTeamGive] = useState([]);
  const [teamReceive, setTeamReceive] = useState([]);
  
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPlayers = async () => {
      try {
        const players = await fetchAllPlayers();
        setAllPlayers(players || []); 
      } catch (err) {
        setError('Failed to load player data. Please try refreshing the page.');
        console.error(err);
      }
    };
    loadPlayers();
  }, []);

  const availablePlayers = useMemo(() => {
    const selectedIds = new Set([...teamGive.map(p => p.player_id), ...teamReceive.map(p => p.player_id)]);
    return allPlayers.filter(p => !selectedIds.has(p.player_id));
  }, [allPlayers, teamGive, teamReceive]);

  const handleAddPlayer = (team, setTeam) => (player) => {
    setTeam([...team, player]);
  };

  const handleRemovePlayer = (team, setTeam) => (player) => {
    setTeam(team.filter(p => p.player_id !== player.player_id));
  };

  const handleAnalyzeTrade = async () => {
    if (teamGive.length === 0 || teamReceive.length === 0) {
      setError('Please add players to both sides of the trade.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    const tradeData = {
      team_a_players: teamGive.map(p => p.player_id),
      team_b_players: teamReceive.map(p => p.player_id),
    };

    try {
      const result = await analyzeTrade(tradeData);
      setAnalysisResult(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'An unexpected error occurred during analysis.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const renderAnalysis = () => {
    if (isLoading) {
      return <p className="text-center py-8 text-blue-400">Analyzing trade...</p>;
    }
    if (error && !analysisResult) {
      return <p className="text-center py-8 text-red-500">{error}</p>;
    }
    if (!analysisResult) {
      return (
        <div className="text-center py-8 text-gray-500">
          <p>Analysis of the trade will appear here.</p>
          <p className="mt-2 text-sm">Input players above and click "Analyze Trade" to see the results.</p>
        </div>
      );
    }

    const { team_a_value, team_b_value, conclusion } = analysisResult;
    return (
      <div className="space-y-4 text-center animate-fade-in">
        <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-700 p-4 rounded-lg">
                <p className="text-gray-400">"You Give" Value</p>
                <p className="text-2xl font-bold text-white">{team_a_value.toFixed(2)}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg">
                <p className="text-gray-400">"You Receive" Value</p>
                <p className="text-2xl font-bold text-white">{team_b_value.toFixed(2)}</p>
            </div>
        </div>
        <div className="bg-gray-900 p-4 rounded-lg">
            <p className="text-lg text-white font-semibold">Conclusion</p>
            <p className="text-blue-300 mt-2">{conclusion}</p>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-white">Trade Analyzer</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <PlayerTradeCard 
          title="You Give" 
          players={teamGive}
          onAddPlayer={handleAddPlayer(teamGive, setTeamGive)}
          onRemovePlayer={handleRemovePlayer(teamGive, setTeamGive)}
          availablePlayers={availablePlayers}
        />
        <PlayerTradeCard 
          title="You Receive" 
          players={teamReceive}
          onAddPlayer={handleAddPlayer(teamReceive, setTeamReceive)}
          onRemovePlayer={handleRemovePlayer(teamReceive, setTeamReceive)}
          availablePlayers={availablePlayers}
        />
      </div>

      <div className="text-center">
        <button 
          onClick={handleAnalyzeTrade}
          disabled={isLoading || allPlayers.length === 0}
          className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-lg text-lg transition-colors disabled:bg-gray-500 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Analyzing...' : 'Analyze Trade'}
        </button>
      </div>

      <div className="bg-gray-800 p-6 rounded-lg min-h-[200px]">
        <h2 className="text-2xl font-bold mb-4 text-white">Analysis Results</h2>
        {renderAnalysis()}
      </div>
    </div>
  );
};

export default TradeAnalyzerPage;
