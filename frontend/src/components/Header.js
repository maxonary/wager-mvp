import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Header({ user, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/signin');
  };

  return (
    <header className="app-header">
      <nav>
        <ul>
          <li><Link to="/betform">Bet</Link></li>
          <li><Link to="/leaderboard">Leaderboard</Link></li>
          <li><Link to="/wallet">Wallet</Link></li>
        </ul>
      </nav>
      {user && (
        <div className="user-info">
          <span>{user.username}</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
    </header>
  );
}

export default Header;