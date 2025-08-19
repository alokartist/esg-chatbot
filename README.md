# ESG Data Chatbot

## Overview
Chat interface that lets users query steel manufacturing ESG data using natural language. Backend uses FastAPI and OpenAI to translate queries to SQL and return tabular results.

## Repo structure## 📂 Project Structure  

```plaintext
esg-chatbot/
├─ backend/                     
│  ├─ app.py                    # Main FastAPI app
│  ├─ utils.py                  # Utility functions (DB connection, helpers, etc.)
│  ├─ requirements.txt          # Python dependencies
│  ├─ .env.example              # Example environment variables
│
├─ frontend/                    
│  ├─ package.json              # Frontend dependencies
│  ├─ public/
│  │   └─ index.html            # Root HTML file
│  └─ src/
│      ├─ index.js              # Entry point for React
│      └─ App.jsx               # Main React component
│
├─ scripts/                     
│  ├─ import_csv_to_sqlite.py   # Load CSV data into SQLite DB
│  └─ normalize_esg.py          # Normalize/clean ESG data
│
├─ data/                        
│  └─ Steel_Manufacturing_ESG_data.csv   # Place your dataset here
│
├─ docs/                        
│  └─ ER_summary.txt            # Entity-Relationship summary
│
├─ .gitignore                   # Ignore unnecessary files
└─ README.md                    # Project documentation


## Setup (local)
1. Clone repo.
2. Place `Steel_Manufacturing_ESG_data.csv` in `data/`.
3. Create virtual env:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt

