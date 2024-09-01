import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './SignUp.css'; // We'll create this CSS file for custom styles

function SignUp() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userTag, setUserTag] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/api/v1/signup`, {
        email,
        password,
        userTag
      });
      if (response.data.success) {
        localStorage.setItem('token', response.data.token);
        navigate('/betform');
      } else {
        setError(response.data.message || 'Signup failed. Please try again.');
      }
    } catch (error) {
      setError(error.response?.data?.message || 'An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="form-input"
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="form-input"
          />
        </div>
        <div className="form-group">
          <label htmlFor="userTag">User Tag:</label>
          <input
            type="text"
            id="userTag"
            value={userTag}
            onChange={(e) => setUserTag(e.target.value)}
            required
            className="form-input"
          />
        </div>
        {error && <p className="error-message">{error}</p>}
        <button type="submit" disabled={isLoading} className="submit-button">
          {isLoading ? 'Signing Up...' : 'Sign Up'}
        </button>
      </form>
      <p className="signin-link">
        Already have an account? <Link to="/signin">Sign In</Link>
      </p>
    </div>
  );
}

export default SignUp;