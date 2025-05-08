# MovieDB Assistant — Natural Language Movie Database Interface

# Overview

# MovieDB Assistant allows users to query a movie database using natural language.
It translates user input into SQL (MySQL) or NoSQL (MongoDB) queries through Llama 2 or OpenAI and displays results via a clean React frontend.
Full Setup Guide
Assumptions
Python 3.8+ already installed
Node.js and npm already installed
MySQL Server and MongoDB Server already installed and running
Required Python libraries already available (Flask, pymongo, pymysql, etc.)

 Project Structure
cpp
Copy
Edit
project/
├── backend/
│   ├── app.py
│   ├── config.py   <-- Configure your MySQL/Mongo credentials here
│   ├── handlers/
│   ├── requirements.txt/
│   ├── utils/
├── frontend/
│   ├── src/
│   ├── public/
├── README.md
└── flow_diagram.png

Create a .env file inside /backend/:

bash
Copy
Edit
OPENAI_API_KEY=your_openai_api_key_here
All personal API keys have been removed from the repository for security purposes.

How to Run

Start docker and run

docker-compose up -d


You will need two terminals open:

Backend (Flask)
bash
Copy
Edit
cd backend/
source env/bin/activate
python app.py
Backend Flask server will be available at:
http://127.0.0.1:5000/

Frontend 
bash
Copy
Edit
cd frontend/
npm start
Frontend will open automatically at:
http://localhost:3000/

