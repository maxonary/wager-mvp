# Backend Documentation
Built on FastAPI 

## Installation
1. Create a virtual environment ```python3 -m venv venv```
2. Activate the virtual environment ```source venv/bin/activate```
3. Install the dependencies ```pip install -r requirements.txt```
4. Copy the .env.example file to .env ```cp .env.example .env``` and fill in the required fields
    1. Go to https://developer.clashroyale.com/ and create a new API Key. Bare in mind to update it with your IP address

## Running the server
1. Run the server ```uvicorn app.main:app --reload```
2. Copy the URL from the terminal and paste it in your browser

## API Documentation
1. Go to the URL ```/docs``` to view the API documentation





Sample Response:
Leaderboard:
{
    "message": "Leaderboard fetched successfully",
    "leaderboard": [
        {
            "userTag": "#UG2UPCYYC",
            "balance": 20,
            "wins": 2
        },
        {
            "userTag": "#VQGV2RURJ",
            "balance": 5,
            "wins": 0
        },
        {
            "userTag": "#202UPGQ9LG",
            "balance": 5,
            "wins": 0
        }
    ]
}

Create match:
{
    "message": "Success",
    "matchID": "b0022eb3-b698-4298-833a-5a1455f8496a",
    "betAmount": 5
}

Create User:
{
    "message": "Success",
    "userID": "66afe88d3d21799a68dbc612",
    "balance": 10
}

GetMatchResult:
{
    "message": "Success",
    "matchID": "8b120575-84c2-485e-96b7-6ae1485b245e",
    "winnerUserTag": "#UG2UPCYYC",
    "betAmount": 5
    "winnerUserName": xxx,
    "winnerNewBalance": xxx,
    "loserUserName": xxx,
    "loserNewBalance": xxx
}

Erro Result:
{
    "detail": "This match result has already been processed."
}
