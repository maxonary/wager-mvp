import React, { useEffect, useState } from 'react';
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

  const openClashRoyaleApp = (userTag) => {
    if (/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream) {
      // iOS device
      window.location.replace(`clashroyale://?addFriend=${userTag}`);
      setTimeout(() => {
        window.location.replace("https://apps.apple.com/app/clash-royale/id1053012308");
      }, 10000);
    } else if (/Android/.test(navigator.userAgent)) {
      // Android device
      window.location.replace(`intent://addfriend/#Intent;scheme=clashroyale;package=com.supercell.clashroyale;end`);
      setTimeout(() => {
        window.location.replace("https://play.google.com/store/apps/details?id=com.supercell.clashroyale");
      }, 10000);
    } else {
      alert('Please open this link on a mobile device with Clash Royale installed.');
    }
  };

  return (
    <div className="leaderboard-container">
      <h2>Leaderboard</h2>
      <table className="leaderboard-table">
        <thead>
          <tr>
            <th>Player Name</th>
            <th>User Tag</th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          {data.map((player, index) => (
            <tr key={index}>
              <td>{player.username ? player.username : 'Anonymous'}</td>
              <td 
                className="user-tag" 
                onClick={() => openClashRoyaleApp(player.userTag)}
                style={{ cursor: 'pointer', color: 'blue', textDecoration: 'underline' }}
              >
                {player.userTag}
              </td>
              <td>${player.balance}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AnotherPage;