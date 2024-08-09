import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles.css'; // Import the updated CSS file
import axios from 'axios';

function AnotherPage() {
  const [data, setData] = useState([]);

  function getData() {
    axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/v1/leaderboard`)
      .then((resp) => {
        const leaderboard = resp.data.leaderboard;
        // Sort the leaderboard by balance in descending order
        const sortedLeaderboard = leaderboard.sort((a, b) => b.balance - a.balance);
        setData(sortedLeaderboard);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }

  useEffect(() => {
    getData();
  }, []);

  return (
    <div className="leaderboard-container">
      <h2>Leaderboard</h2>
      <table className="leaderboard-table">
        <thead>
          <tr>
            <th>Player Name</th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          {data.map((player, index) => (
            <tr key={index}>
              <td>{player.username ? player.username : 'Anonymous'}</td>
              <td>${player.balance}</td>
            </tr>
          ))}
        </tbody>
      </table>
      
      {/* Button to go back to BetForm */}
      <Link to="/">
        <button className="back-button">Start a new a bet</button>
      </Link>
    </div>
  );
}

export default AnotherPage;
