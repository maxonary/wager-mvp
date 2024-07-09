import React, { useState } from 'react';
import BetForm from './components/BetForm';
import Leaderboard from './components/Leaderboard';
import './App.css';

function App() {
  const [betAmount, setBetAmount] = useState(50);

  const handleBetAmountChange = (amount) => {
    setBetAmount(amount);
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Clash Royale</h1>
        <BetForm betAmount={betAmount} onBetAmountChange={handleBetAmountChange} />
        <Leaderboard betAmount={betAmount} />
      </div>
    </div>
  );
}

export default App;
