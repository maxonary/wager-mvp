import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import BetForm from './components/BetForm';
import Leaderboard from './components/Leaderboard';
import './App.css';
import './styles.css';

function App() {
  const [betAmount, setBetAmount] = useState(50);

  const handleBetAmountChange = (amount) => {
    setBetAmount(amount);
  };

  return (
    <Router>
      <div className="App">
        <div className="container">
          <h1>Wager</h1>
          <Routes>
            <Route path="/" element={<BetForm betAmount={betAmount} onBetAmountChange={handleBetAmountChange} />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
