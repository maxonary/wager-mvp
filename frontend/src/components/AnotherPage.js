import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles.css'; // Import the updated CSS file
import axios from 'axios';
import { copyToClipboard } from '../utils/clipboardUtils';

function AnotherPage() {
  const [data, setData] = useState([]);
  const navigate = useNavigate(); // Use useNavigate instead of useHistory

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

  const handleStartNewBet = () => {
    // Clear the token from local storage
    localStorage.removeItem('currentMatch');

    // Redirect to BetForm page
    navigate('/'); // Use navigate instead of history.push
  };

  return (
    <div className="leaderboard-container">
      <h2>Leaderboard</h2>
      <table className="leaderboard-table">
        <thead>
          <tr>
            <th>Player Name
              <br/>
              (Click to copy user tag)
            </th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          {data.map((player, index) => (
            <tr key={index}>
              <td onClick={() => copyToClipboard(player.userTag)}>
                <strong>{player.username ? player.username : 'Anonymous'}</strong>
                <br />
                {player.userTag} 
              </td>
              <td>
                <strong>${player.balance}</strong>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {/* Button to go back to BetForm */}
      <button className="back-button" onClick={handleStartNewBet}>
        Start a new bet
      </button>
    </div>
  );
}

export default AnotherPage;
