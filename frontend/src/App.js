// import React from 'react';
// import BetForm from './components/BetForm';
// import Leaderboard from './components/Leaderboard';
// import './App.css';

// function App() {
//     return (
//         <div>
//             <h1>Clash Royale Betting</h1>
//             <BetForm />
//             <Leaderboard />
//         </div>
//     );
// }

// export default App;
import React from 'react';
import BetForm from './components/BetForm';
import Leaderboard from './components/Leaderboard';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="container">
        <h1>Clash Royale Betting</h1>
        <BetForm />
        <Leaderboard />
      </div>
    </div>
  );
}

export default App;
