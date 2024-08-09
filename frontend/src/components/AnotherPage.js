import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles.css'; // Import the updated CSS file
import axios from 'axios';

function AnotherPage() {
  const [data, setData] = useState([]);
  const [isDataFetched, setIsDataFetched] = useState(false);

  function getData() {
    axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/v1/leaderboard`)
      .then((resp) => {
        const leaderboard = resp.data.leaderboard;
        // Sort the leaderboard by balance in descending order
        const sortedLeaderboard = leaderboard.sort((a, b) => b.balance - a.balance);
        setData(sortedLeaderboard);
        setIsDataFetched(true); // Set data fetched state to true
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }

  useEffect(() => {
    getData();
  }, []);

  function resetPage() {
    setIsDataFetched(false); // Reset data fetched state
    setData([]); // Clear the data
    getData(); // Re-fetch data
  }

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
          {data.length > 0 ? (
            data.map((player, index) => (
              <tr key={index}>
                <td>{player.username ? player.username : 'Anonymous'}</td>
                <td>${player.balance}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="2">No data available</td>
            </tr>
          )}
        </tbody>
      </table>

      {/* Button to go back to BetForm */}
      <Link to="/">
        <button className="back-button">Start a new bet</button>
      </Link>

      {/* Button to refresh data */}
      {isDataFetched && (
        <button className="refresh-button" onClick={resetPage}>
          Refresh Data
        </button>
      )}
    </div>
  );
}

export default AnotherPage;
