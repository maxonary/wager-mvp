import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import 'font-awesome/css/font-awesome.min.css'; // Import Font Awesome CSS
import '../styles.css'; // Import the updated CSS file
import axios from 'axios';

function BetForm({ betAmount, onBetAmountChange }) {
  const [player1Tag, setPlayer1Tag] = useState('#');
  const [player2Tag, setPlayer2Tag] = useState('#');
  const [rangeValue, setRangeValue] = useState(1); // Updated initial state to 1
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [matchID, setMatchID] = useState(null);
  const [result, setResult] = useState(null);

  const handleSliderChange = (event) => {
    onBetAmountChange(parseInt(event.target.value, 10));
    setRangeValue(event.target.value);
  };

  const handleTagChange = (setter, value) => {
    const formattedValue = value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase(); // Remove non-alphanumeric characters and convert to uppercase
    setter(`#${formattedValue}`);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if ((player1Tag.length < 7 || player1Tag.length > 10) || (player2Tag.length < 7 || player2Tag.length > 10)) {
      setError('Your gamertag must be between 7 and 10 characters long');
    } else {
      const body = {
        userTag1: player1Tag,
        userTag2: player2Tag,
        betAmount: parseInt(rangeValue),
      };
      axios
        .post(`${process.env.REACT_APP_BACKEND_URL}/api/v1/match`, body)
        .then((response) => {
          setError('');
          setIsSubmitting(true);
          setIsCompleted(false);

          setTimeout(() => {
            setIsSubmitting(false);
            setIsCompleted(true);
            setMatchID(response.data.matchID); // Save match ID
          }, 2000); // Simulate a 2-second delay
        })
        .catch((error) => {
          setError('Failed to start bet. Please try again.');
        });
    }
  };

  const handleFetchResult = () => {
    if (!matchID) return;
    setIsSubmitting(true);
  
    // Prepare the request body
    const requestBody = {
      matchID: matchID,
    };
  
    axios
      .post(`${process.env.REACT_APP_BACKEND_URL}/api/v1/match/result`, requestBody) // Send matchID as body
      .then((response) => {
        setIsSubmitting(false);
        setResult(response.data);
      })
      .catch((error) => {
        setIsSubmitting(false);
        setError('Failed to fetch result. Please try again.');
      });
  };
  

  const closeModal = () => {
    setError('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input-group">
        <div className="input-wrapper">
          <label htmlFor="player1">User Tag:</label>
          <input
            type="text"
            id="player1"
            name="player1"
            value={player1Tag}
            onChange={(e) => handleTagChange(setPlayer1Tag, e.target.value)}
          />
        </div>
        <div className="input-wrapper">
          <label htmlFor="player2">Opponent Tag:</label>
          <input
            type="text"
            id="player2"
            name="player2"
            value={player2Tag}
            onChange={(e) => handleTagChange(setPlayer2Tag, e.target.value)}
          />
        </div>
      </div>

      {!isCompleted ? (
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'center' }}>
          <p>Bet Amount:</p>
          <input
            type="range"
            className="range-slider"
            min={1} // Updated minimum value to 1
            max={10}
            onChange={handleSliderChange}
            style={{ width: '50%', margin: '0px 5px' }}
            value={rangeValue}
          />
          <p>{rangeValue}</p>
        </div>
      ) : (
        <p>You're Wagering ${rangeValue} - let the game begin!</p>
      )}

      {!isCompleted ? (
        <button type="submit" disabled={isSubmitting} style={{ marginRight: '10px' }}>
          {isSubmitting ? <i className="fa fa-spinner fa-spin"></i> : 'Start Bet'}
        </button>
      ) : (
        <button type="button" onClick={handleFetchResult} disabled={isSubmitting}>
          {isSubmitting ? <i className="fa fa-spinner fa-spin"></i> : 'Fetch Result'}
        </button>
      )}

      {result && (
        <div className="result">
          <p>Winner: {result.winnerUserName} (New Balance: {result.winnerNewBalance})</p>
          <p>Loser: {result.loserUserName} (New Balance: {result.loserNewBalance})</p>
        </div>
      )}

      {error && (
        <div className="modal">
          <div className="modal-content">
            <p>{error}</p>
            <button onClick={closeModal}>OK</button>
          </div>
        </div>
      )}

      {/* Link to leaderboard Page */}
      <Link to="/leaderboard">
        <button type="button">Leaderboard</button>
      </Link>
    </form>
  );
}

export default BetForm;
