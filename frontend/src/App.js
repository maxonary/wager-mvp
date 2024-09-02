import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
  Link,
} from "react-router-dom";
import BetForm from "./components/BetForm";
import DonationButton from "./components/DonationButton";
import Wallet from "./components/Wallet";
import Leaderboard from "./components/Leaderboard";
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
          <nav>
            <ul className="nav-links">
              <li><Link to="/betform">Bet</Link></li>
              <li><Link to="/leaderboard">Leaderboard</Link></li>
              <li><Link to="/wallet">Wallet</Link></li>
              <li><Link to="/donate">Top up account</Link></li>
            </ul>
          </nav>
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
                <BetForm
                  betAmount={betAmount}
                  onBetAmountChange={handleBetAmountChange}
                />
              }
            />
            <Route path="/leaderboard" element={<Leaderboard />} />
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
            <Route path="/donate" element={<DonationButton />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;