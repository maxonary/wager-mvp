## Setting up and running the project
### Backend
1. Create a virtual environment in the backend folder ```python3 -m venv venv```
2. Activate the virtual environment ```source venv/bin/activate```
3. Install the required packages ```pip install -r requirements.txt```
4. Copy the .env.example file to .env ```cp .env.example .env``` and fill in the required fields
5. Run the server ```uvicorn app.main:app --reload``` 

### Frontend
1. Install the required packages ```npm install```
2. Copy the .env.example file to .env ```cp .env.example .env``` and fill in the required fields
3. Run the server ```npm start```

### Docker 
1. Make sure the environment variables are set in the .env file in the root of the project
2. Run ```docker-compose build``` to build the images
3. Run ```docker-compose up``` to start the containers