import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

function SignIn({ onAuthenticate, redirectTo }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/api/v1/signin`,
        {
          email,
          password,
        }
      );
      if (response.data.access_token) {
        localStorage.setItem("token", response.data.access_token);
        onAuthenticate(true);
        navigate(redirectTo || "/betform");
      } else {
        setError("Sign in failed. Please try again.");
      }
    } catch (error) {
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === "string") {
          setError(errorData);
        } else if (typeof errorData === "object") {
          setError(errorData.detail || JSON.stringify(errorData));
        } else {
          setError("An unexpected error occurred. Please try again.");
        }
      } else if (error.request) {
        setError("No response received from server. Please try again.");
      } else {
        setError("An error occurred. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="signin-container">
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
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
          />
        </div>
        {error && <p className="error-message">{error}</p>}
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Signing In..." : "Sign In"}
        </button>
      </form>
      <p>
        Don't have an account? <Link to="/signup">Sign Up</Link>
      </p>
    </div>
  );
}

export default SignIn;
