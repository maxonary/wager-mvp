import React, { useEffect, useState } from 'react';
import '../styles.css'; // Import the updated CSS file
import axios from 'axios';

function AnotherPage() {
  const [data, setData] = useState([]);

  function getData() {
    axios.get('https://backend-service-fuf2ajnimq-wl.a.run.app/api/v1/leaderboard')
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
    </div>
  );
}

export default AnotherPage;