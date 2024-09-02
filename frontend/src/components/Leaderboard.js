import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../styles.css";
import axios from "axios";
import { copyToClipboard } from "../utils/clipboardUtils";

function LeaderBoard() {
  const [data, setData] = useState([]);

  function getData() {
    axios
      .get(`${process.env.REACT_APP_BACKEND_URL}/api/v1/leaderboard`)
      .then((resp) => {
        const leaderboard = resp.data.leaderboard;
        const sortedLeaderboard = leaderboard.sort(
          (a, b) => b.balance - a.balance
        );
        setData(sortedLeaderboard);
      })
      .catch((error) => {
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
            <th>Player Name (Click to copy user tag)</th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          {data.map((player, index) => (
            <tr key={index}>
              <td onClick={() => copyToClipboard(player.userTag)}>
                <strong>
                  {player.username ? player.username : "Anonymous"}
                </strong>
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
      <Link to="/betform">
        <button className="back-button">Start a new bet</button>
      </Link>
    </div>
  );
}

export default LeaderBoard;
