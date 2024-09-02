import React, { useState, useEffect } from "react";
import axios from "axios";

function Wallet() {
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_BACKEND_URL}/api/v1/user/info`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        setUserData(response.data);
      } catch (err) {
        setError("Failed to fetch user data. Please try again later.");
        console.error("Error fetching user data:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (isLoading) {
    return <div>Loading user data...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!userData) {
    return <div className="error-message">No user data available.</div>;
  }

  return (
    <div className="wallet">
      <h2 className="wallet-title">Your Wallet</h2>
      <div className="wallet-balance">
        <p>Current Balance: ${userData.balance}</p>
      </div>
      <div className="wallet-info">
        <p>Username: {userData.username}</p>
        <p>User Tag: {userData.userTag}</p>
      </div>
    </div>
  );
}

export default Wallet;
