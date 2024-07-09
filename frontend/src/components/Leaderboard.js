import React from 'react';

function Leaderboard({ betAmount }) {
  const initialWallet = 100;
  const currentWallet = initialWallet - betAmount;

  return (
    <div className="leaderboard">
      <h2 className="leaderboard-title">Your Wallet</h2>
      <ul>
        <li> Updated Amount: ${currentWallet}</li>
      </ul>
    </div>
  );
}

export default Leaderboard;
