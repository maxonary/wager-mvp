// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// function Leaderboard() {
//     const [players, setPlayers] = useState([]);

//     useEffect(() => {
//         const fetchLeaderboard = async () => {
//             try {
//                 const response = await axios.get('/api/v1/leaderboard/');
//                 setPlayers(response.data);
//             } catch (error) {
//                 console.error('Error fetching leaderboard:', error);
//             }
//         };
//         fetchLeaderboard();
//     }, []);

//     return (
//         <div>
//             <h2>Leaderboard</h2>
//             <ul>
//                 {players.map((player) => (
//                     <li key={player.id}>
//                         {player.tag}: {player.points} points
//                     </li>
//                 ))}
//             </ul>
//         </div>
//     );
// }

// export default Leaderboard;

import React from 'react';

function Leaderboard() {
  return (
    <div className="leaderboard">
      <h2 className="leaderboard-title">Leaderboard</h2>
      <ul>
        {/* List items will be dynamically rendered here */}
      </ul>
    </div>
  );
}

export default Leaderboard;
