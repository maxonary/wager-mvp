import React, { useState } from 'react';
import axios from 'axios';

function BetForm() {
    const [player1, setPlayer1] = useState('');
    const [player2, setPlayer2] = useState('');
    const [amount, setAmount] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('/api/v1/bets/', {
                player1_tag: player1,
                player2_tag: player2,
                bet_amount: parseFloat(amount),
            });
            console.log(response.data);
        } catch (error) {
            console.error('Error placing bet:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Player 1 Tag:</label>
                <input type="text" value={player1} onChange={(e) => setPlayer1(e.target.value)} required />
            </div>
            <div>
                <label>Player 2 Tag:</label>
                <input type="text" value={player2} onChange={(e) => setPlayer2(e.target.value)} required />
            </div>
            <div>
                <label>Bet Amount:</label>
                <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} required />
            </div>
            <button type="submit">Place Bet</button>
        </form>
    );
}

export default BetForm;
