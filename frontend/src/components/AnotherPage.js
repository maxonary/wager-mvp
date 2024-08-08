import React from 'react';
import '../styles.css'; // Import the updated CSS file

const players = [
  { name: 'Player1', userId: '123456789', winnings: '$100' },
  { name: 'Player2', userId: '987654321', winnings: '$200' },
  { name: 'Player3', userId: '192837465', winnings: '$150' },
  // Add more players as needed
];

function AnotherPage() {
  return (
    <div className="leaderboard-container">
      <h2>Leaderboard</h2>
      <table className="leaderboard-table">
        <thead>
          <tr>
            <th>Player Name</th>
            <th>User ID</th>
            <th>Winnings</th>
          </tr>
        </thead>
        <tbody>
          {players.map((player, index) => (
            <tr key={index}>
              <td>{player.name}</td>
              <td>{player.userId}</td>
              <td>{player.winnings}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AnotherPage;