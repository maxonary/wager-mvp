import React, { useState } from 'react';

function BetForm({ betAmount, onBetAmountChange }) {
  const [player1Tag, setPlayer1Tag] = useState('#');
  const [player2Tag, setPlayer2Tag] = useState('#');
  const [error, setError] = useState('');

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
      setError('');
      // Submit form logic here
    }
  };

  const closeModal = () => {
    setError('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input-group">
        <div className="input-wrapper">
          <label htmlFor="player1">Player 1 Tag:</label>
          <input 
            type="text" 
            id="player1" 
            name="player1" 
            value={player1Tag} 
            onChange={(e) => handleTagChange(setPlayer1Tag, e.target.value)} 
          />
        </div>
        <div className="input-wrapper">
          <label htmlFor="player2">Player 2 Tag:</label>
          <input 
            type="text" 
            id="player2" 
            name="player2" 
            value={player2Tag} 
            onChange={(e) => handleTagChange(setPlayer2Tag, e.target.value)} 
          />
        </div>
      </div>
      <button type="submit">Place Bet</button>

      {error && (
        <div className="modal">
          <div className="modal-content">
            <p>{error}</p>
            <button onClick={closeModal}>OK</button>
          </div>
        </div>
      )}
    </form>
  );
}

export default BetForm;
