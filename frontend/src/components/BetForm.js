import React, { useState } from 'react';
import axios from 'axios';

const isDebug = process.env.REACT_APP_DEBUG === 'true';

function BetForm() {
    const [player1, setPlayer1] = useState('');
    const [player2, setPlayer2] = useState('');
    const [amount, setAmount] = useState('');
    const [betId, setBetId] = useState(null);
    const [winner, setWinner] = useState('');
    const [betStatus, setBetStatus] = useState('');
    const [betError, setBetError] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        setBetStatus('');
        setBetError('');
        try {
            const response = await axios.post('/api/v1/bets/', {
                player1_tag: player1,
                player2_tag: player2,
                bet_amount: parseFloat(amount),
            });
            if (isDebug) console.log('Bet placed:', response.data);
            setBetId(response.data.id);
            setBetStatus('Bet placed successfully!');
        } catch (error) {
            if (isDebug) console.error('Error placing bet:', error);
            setBetError('Error placing bet. Please try again.');
        }
    };

    const checkBetStatus = async () => {
        try {
            const response = await axios.get(`/api/v1/bets/${betId}`);
            if (response.data.winner_tag) {
                if (isDebug) console.log('Bet status:', response.data);
                setWinner(response.data.winner_tag);
                setBetStatus(`Winner: ${response.data.winner_tag}`);
            } else {
                setBetStatus('Bet is still ongoing. Please check again later.');
            }
        } catch (error) {
            if (isDebug) console.error('Error checking bet status:', error);
            setBetError('Error checking bet status. Please try again.');
        }
    };

    return (
        <div>
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
            {betId && <button onClick={checkBetStatus}>Check Bet Status</button>}
            {betStatus && <p>{betStatus}</p>}
            {betError && <p style={{ color: 'red' }}>{betError}</p>}
            {winner && <p>Winner: {winner}</p>}
        </div>
    );
}

export default BetForm;
