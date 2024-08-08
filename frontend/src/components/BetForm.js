import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import 'font-awesome/css/font-awesome.min.css'; // Import Font Awesome CSS
import '../styles.css'; // Import the updated CSS file
import axios from 'axios'

function BetForm({ betAmount, onBetAmountChange }) {
  const [player1Tag, setPlayer1Tag] = useState('#');
  const [player2Tag, setPlayer2Tag] = useState('#');
  const [rangeValue, setRangeValue] = useState(0)
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false); // Add this state

  const handleSliderChange = (event) => {
    onBetAmountChange(parseInt(event.target.value, 10));
  };

  const handleTagChange = (setter, value) => {
    const formattedValue = value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase(); // Remove non-alphanumeric characters and convert to uppercase
    setter(`#${formattedValue}`);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (player1Tag.length !== 10 || player2Tag.length !== 10) {
      setError('Your gamertag is 9 characters long');
    } else {
      const body = {
        "userTag1": player1Tag,
        "userTag2": player2Tag,
        "betAmount": parseInt(rangeValue)
      }
      axios.post('https://backend-service-fuf2ajnimq-wl.a.run.app/api/v1/match', body)
        .then((response) => {
          setError('');
          setIsSubmitting(true);
          setIsCompleted(false); // Reset completion status

          // Simulate an asynchronous operation like an API call
          setTimeout(() => {
            setIsSubmitting(false);
            setIsCompleted(true); // Mark as completed after the operation
          }, 2000); // Simulate a 2-second delay
        })
    }
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
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'center' }}>
        <p>Bet Amount:</p>
        <input type='range' className='range-slider' max={10} onChange={(e) => setRangeValue(e.target.value)} style={{ width: '50%',margin:'0px 5px' }} value={rangeValue} />
        <p>{rangeValue}</p>
      </div>
      <button type="submit" disabled={isSubmitting} style={{ marginRight: '10px' }}>
        {isSubmitting ? (
          <i className="fa fa-spinner fa-spin"></i>
        ) : isCompleted ? (
          <i className="fa fa-check"></i> // Display check mark when completed
        ) : (
          'Start Bet'
        )}
      </button>

      {isSubmitting && (
        <p className="in-progress-text">Match Id: 1X3eR4</p>
      )}

      {error && (
        <div className="modal">
          <div className="modal-content">
            <p>{error}</p>
            <button onClick={closeModal}>OK</button>
          </div>
        </div>
      )}

      {/* Link to Another Page */}
      <Link to="/anotherpage">
        <button type="button">Leaderboard</button>
      </Link>
    </form>
  );
}

export default BetForm;
