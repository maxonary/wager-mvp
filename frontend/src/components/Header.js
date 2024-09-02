import React from 'react';
import { useNavigate } from 'react-router-dom';

function Header({ user, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/signin');
  };

  return (
    <header className="app-header">
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