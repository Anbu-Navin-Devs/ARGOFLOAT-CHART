# 🌊 FloatChart – ARGO Ocean Intelligence Suite

A comprehensive toolkit for exploring ARGO float oceanographic data using AI-powered natural language queries.

| Application | Type | Purpose |
|-------------|------|---------|
| **ARGO_CHATBOT** | 🌐 Web App | Natural language query interface with maps & charts |
| **DATA_GENERATOR** | 🖥️ Desktop App | ETL pipeline for fetching ARGO data into PostgreSQL |

---

## 📋 Table of Contents

1. [Complete Setup Guide (Beginners)](#-complete-setup-guide-for-beginners)
2. [Project Structure](#-project-structure)
3. [Quick Start (Experienced Users)](#-quick-start)
4. [Features](#-features)
5. [Configuration](#️-configuration)
6. [Troubleshooting](#-troubleshooting)

---

## 🎓 Complete Setup Guide (For Beginners)

Follow these steps **in order** to get everything running from scratch.

### Step 1: Install Prerequisites

#### 1.1 Install Python (3.10 or higher)

1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
2. **IMPORTANT**: Check ✅ "Add Python to PATH" during installation
3. Verify installation:
   ```cmd
   python --version
   ```
   Should show: `Python 3.10.x` or higher

#### 1.2 Install PostgreSQL

1. Download from [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
2. Run the installer and remember:
   - **Password** you set for `postgres` user (you'll need this!)
   - **Port**: Keep default `5432`
3. When prompted, include "pgAdmin 4" (GUI tool)
4. After installation, **restart your computer**

#### 1.3 Install VS Code (Recommended)

1. Download from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install recommended extensions:
   - Python
   - SQLTools
   - SQLTools PostgreSQL

---

### Step 2: Setup PostgreSQL Database

#### 2.1 Using pgAdmin (GUI Method - Easier)

1. Open **pgAdmin 4** from Start Menu
2. Click on "Servers" → Right-click → "Register" → "Server"
3. Enter:
   - Name: `Local`
   - Host: `localhost`
   - Port: `5432`
   - Username: `postgres`
   - Password: (what you set during installation)
4. Click "Save"

5. **Create the database:**
   - Right-click on "Databases" → "Create" → "Database"
   - Name: `argo_db`
   - Click "Save"

6. **Create the table:**
   - Click on `argo_db` → "Tools" → "Query Tool"
   - Paste this SQL and click ▶️ Run:

```sql
-- Create the main data table
CREATE TABLE argo_data (
    id SERIAL PRIMARY KEY,
    float_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    pressure DOUBLE PRECISION,
    temperature DOUBLE PRECISION,
    salinity DOUBLE PRECISION,
    dissolved_oxygen DOUBLE PRECISION,
    chlorophyll DOUBLE PRECISION
);

-- Create indexes for fast queries
CREATE INDEX idx_argo_float_id ON argo_data(float_id);
CREATE INDEX idx_argo_timestamp ON argo_data(timestamp);
CREATE INDEX idx_argo_location ON argo_data(latitude, longitude);

-- Prevent duplicate data
CREATE UNIQUE INDEX idx_argo_unique ON argo_data(float_id, timestamp, pressure);
```

#### 2.2 Using Command Line (Alternative)

```cmd
# Open command prompt and run:
psql -U postgres

# Enter your password when prompted, then:
CREATE DATABASE argo_db;
\c argo_db

# Paste the SQL above, then:
\q
```

---

### Step 3: Get Your FREE AI API Key

You need **ONE** of these (Gemini is recommended - completely FREE):

#### Option A: Google Gemini API (🌟 RECOMMENDED - FREE)

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)
5. ✅ **FREE**: 60 requests per minute, no credit card needed!

#### Option B: Groq API (Alternative - Also FREE)

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up / Sign in
3. Click **"Create API Key"**
4. Copy the key (starts with `gsk_...`)
5. ✅ **FREE**: Very fast inference

---

### Step 4: Download & Configure the Project

#### 4.1 Clone or Download the Project

```cmd
# Option 1: Clone with Git
git clone <repository-url>
cd ARGOFLOAT-CHART

# Option 2: Download ZIP and extract to a folder
```

#### 4.2 Create Virtual Environment

```cmd
# Navigate to project folder
cd "E:\VS CODE\ARGOFLOAT-CHART"

# Create virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate

# You should see (.venv) at the start of your command prompt
```

#### 4.3 Configure Environment Variables

1. Copy the template file:
   ```cmd
   copy .env.example .env
   ```

2. Open `.env` in VS Code or Notepad and update these values:

```env
# DATABASE - Update password!
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD_HERE@localhost:5432/argo_db

# AI API KEY - Use ONE of these:

# If using Gemini (recommended):
GOOGLE_API_KEY=AIza_YOUR_KEY_HERE
GEMINI_MODEL=gemini-1.5-flash

# OR if using Groq:
GROQ_API_KEY=gsk_YOUR_KEY_HERE
GROQ_MODEL_NAME=llama-3.3-70b-versatile
```

**Example for Gemini:**
```env
DATABASE_URL=postgresql+psycopg2://postgres:mypassword123@localhost:5432/argo_db
GOOGLE_API_KEY=AIzaSyABC123xyz...
GEMINI_MODEL=gemini-1.5-flash
```

---

### Step 5: Get Ocean Data (DATA_GENERATOR)

Now let's fetch real ARGO float data from the ocean!

```cmd
# Make sure virtual environment is active
# (you should see (.venv) in your prompt)

# Install dependencies
cd DATA_GENERATOR
pip install -r requirements.txt

# Run the Data Generator GUI
python gui.py
```

**In the GUI:**
1. Click **"Update Latest Data"** button
2. Wait for the progress bar to complete
3. Check "Activity Log" for status messages
4. The database snapshot will show how many records were added

**What's happening?**
- Fetches data from [Ifremer ERDDAP](https://erddap.ifremer.fr/) server
- Downloads ARGO float profiles from the Indian Ocean region
- Transforms NetCDF data and loads into PostgreSQL

---

### Step 6: Run the Web Application

Now for the fun part - the AI chatbot!

```cmd
# Go back to chatbot folder
cd ../ARGO_CHATBOT

# Install dependencies
pip install -r requirements.txt

# Start the web server
python app.py
```

You should see:
```
🌊 FloatChat server starting...
📊 Running on http://127.0.0.1:5000
```

**Open your browser:** [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### Step 7: Start Asking Questions!

Try these example queries:
- "Show me all ARGO floats in the Arabian Sea"
- "What is the average temperature in Bay of Bengal?"
- "Show trajectory of float 2902115"
- "What are the nearest floats to Chennai?"
- "Compare temperature and salinity trends"

---

## 📁 Project Structure

```
ARGOFLOAT-CHART/
├── .env                   # Your config (create from .env.example)
├── .env.example           # Template file
├── README.md              # This guide
│
├── ARGO_CHATBOT/          # 🌐 Web Application
│   ├── app.py             # Flask server
│   ├── brain.py           # AI/NLP processing
│   ├── sql_builder.py     # Query generation
│   ├── database_utils.py  # DB connections
│   └── static/            # Frontend files
│       ├── index.html
│       ├── css/styles.css
│       └── js/app.js
│
└── DATA_GENERATOR/        # 🖥️ Desktop App
    ├── gui.py             # Tkinter GUI
    ├── config.py          # Settings
    └── pipeline/          # ETL modules
        ├── netcdf_fetcher.py
        ├── netcdf_transformer.py
        ├── db_loader.py
        └── state_manager.py
```

---

## 🚀 Quick Start

For experienced users who already have PostgreSQL and Python:

```bash
# Clone and setup
git clone <repo-url>
cd ARGOFLOAT-CHART
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Configure
cp .env.example .env
# Edit .env with your DATABASE_URL and GOOGLE_API_KEY

# Get data
cd DATA_GENERATOR
pip install -r requirements.txt
python gui.py  # Click "Update Latest Data"

# Run chatbot
cd ../ARGO_CHATBOT
pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:5000
```

---

## ✨ Features

### ARGO_CHATBOT (Web App)
- 💬 **Natural Language Queries** - Ask in plain English
- 🗺️ **Interactive Map** - Leaflet.js with float markers
- 📊 **Dynamic Charts** - Temperature, salinity trends
- 📋 **Data Tables** - Browse and filter results
- ⬇️ **CSV Export** - Download your data
- 📜 **Query History** - Saved locally

### DATA_GENERATOR (Desktop App)
- ⬇️ **One-Click Updates** - Fetch latest ARGO profiles
- 📊 **Database Stats** - View record counts
- 🔄 **Incremental Updates** - Only new data since last run
- 📋 **Activity Log** - Track progress

---

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `GOOGLE_API_KEY` | ✅* | Gemini API key (FREE) |
| `GEMINI_MODEL` | ❌ | Model name (default: gemini-1.5-flash) |
| `GROQ_API_KEY` | ✅* | Groq API key (alternative) |
| `GROQ_MODEL_NAME` | ❌ | Model name (default: llama-3.3-70b-versatile) |

*Need at least ONE of the API keys

### AI Provider Comparison

| Provider | Cost | Speed | Limit |
|----------|------|-------|-------|
| **Google Gemini** | 🟢 FREE | Fast | 60 req/min |
| **Groq** | 🟢 FREE | Very Fast | ~30 req/min |

---

## 🐛 Troubleshooting

### "Could not connect to database"
- ✅ Check PostgreSQL is running (look for "postgresql-x64-16" in Services)
- ✅ Verify password in `.env` matches your PostgreSQL password
- ✅ Ensure database `argo_db` exists

### "No AI provider configured"
- ✅ Check `.env` has either `GOOGLE_API_KEY` or `GROQ_API_KEY`
- ✅ Make sure there are no extra spaces in the API key

### "No data found"
- ✅ Run DATA_GENERATOR first to populate the database
- ✅ Check data exists: In pgAdmin, run `SELECT COUNT(*) FROM argo_data;`

### Port 5000 already in use
```cmd
# Find what's using the port
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID_NUMBER> /F
```

### Module not found errors
```cmd
# Make sure you're in the virtual environment
.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📚 Learn More

- **ARGO Program**: [argo.ucsd.edu](https://argo.ucsd.edu/) - Global ocean observation
- **ERDDAP Data**: [erddap.ifremer.fr](https://erddap.ifremer.fr/) - Data source
- **Google AI Studio**: [aistudio.google.com](https://aistudio.google.com/) - Get API keys
- **PostgreSQL Docs**: [postgresql.org/docs](https://www.postgresql.org/docs/)

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

---

Made with 💙 for Ocean Science 🌊
