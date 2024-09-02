import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import BetForm from "./components/BetForm";
import Leaderboard from "./components/Leaderboard";
import AnotherPage from "./components/AnotherPage";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import "./App.css";
import "./styles.css";

function App() {
  const [betAmount, setBetAmount] = useState(50);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleBetAmountChange = (amount) => {
    setBetAmount(amount);
  };

  const handleAuthentication = (status) => {
    setIsAuthenticated(status);
  };

  return (
    <Router>
      <div className="App">
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
              path="/anotherpage"
              element={
                isAuthenticated ? (
                  <AnotherPage />
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
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
