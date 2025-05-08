# MovieDB Assistant — Natural Language Movie Database Interface

## Overview
MovieDB Assistant allows users to query a movie database using natural language.
It translates user input into SQL (MySQL) or NoSQL (MongoDB) queries through Llama 2 or OpenAI and displays results via a clean React frontend.

---

## Assumptions
- Python 3.8+ already installed
- Node.js and npm already installed
- MySQL Server and MongoDB Server already installed and running
- Required Python libraries already available (Flask, pymongo, pymysql, etc.)

---

## Project Structure

project/
├── backend/




│ ├── app.py




│ ├── config.py <-- Configure your MySQL/Mongo credentials here




│ ├── handlers/




│ ├── requirements.txt




│ ├── utils/




├── frontend/




│ ├── src/




│ ├── public/




├── README.md




└── flow_diagram.png

yaml
Copy
Edit

---

## Environment Setup

Create a `.env` file inside `/backend/`:

```bash
OPENAI_API_KEY=your_openai_api_key_here
Important:

All personal API keys have been removed from the repository for security purposes.

Configure your SQL password in config.py inside backend.

Example in config.py:

python
Copy
Edit
mysql_password = "your_password_here"
How to Run
1. Start Docker
bash
Copy
Edit
docker-compose up -d
2. Open Two Terminals
Terminal 1: Backend (Flask)
bash
Copy
Edit
cd backend/
source env/bin/activate
python app.py
Flask server will be available at: http://127.0.0.1:5000/

Terminal 2: Frontend (React)
bash
Copy
Edit
cd frontend/
npm install  # Only needed the first time
npm start
React frontend will open at: http://localhost:3000/



