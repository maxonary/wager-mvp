import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import BetForm from "./components/BetForm";
import Wallet from "./components/Wallet";
import Leaderboard from "./components/LeaderBoard";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import Header from "./components/Header";
import "./App.css";
import "./styles.css";

function App() {
  const [betAmount, setBetAmount] = useState(50);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");
    if (token && storedUser) {
      setIsAuthenticated(true);
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleBetAmountChange = (amount) => {
    setBetAmount(amount);
  };

  const handleAuthentication = (status, userData) => {
    setIsAuthenticated(status);
    if (status) {
      setUser(userData);
      localStorage.setItem("user", JSON.stringify(userData));
    } else {
      setUser(null);
      localStorage.removeItem("user");
      localStorage.removeItem("token");
    }
  };

  const handleLogout = () => {
    handleAuthentication(false);
  };

  return (
    <Router>
      <div className="App">
        <Header user={user} onLogout={handleLogout} />
        <div className="container">
          <h1>Wager</h1>
          <Routes>
            <Route path="/" element={<Navigate replace to="/signup" />} />
            <Route
              path="/signup"
              element={<SignUp onAuthenticate={handleAuthentication} />}
            />
            <Route
              path="/signin"
              element={
                <SignIn
                  onAuthenticate={handleAuthentication}
                  redirectTo="/betform"
                />
              }
            />
            <Route
              path="/betform"
              element={
                isAuthenticated ? (
                  <BetForm
                    betAmount={betAmount}
                    onBetAmountChange={handleBetAmountChange}
                  />
                ) : (
                  <Navigate replace to="/signin" />
                )
              }
            />
            <Route
              path="/leaderboard"
              element={
                isAuthenticated ? (
                  <Leaderboard />
                ) : (
                  <Navigate replace to="/signin" />
                )
              }
            />
            <Route
              path="/wallet"
              element={
                isAuthenticated ? (
                  <Wallet user={user} />
                ) : (
                  <Navigate replace to="/signin" />
                )
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
