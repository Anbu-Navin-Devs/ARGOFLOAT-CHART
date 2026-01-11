# 🌊 FloatChart – ARGO Ocean Intelligence Suite

A comprehensive toolkit for exploring ARGO float oceanographic data. This repository combines two applications:

| Application | Type | Purpose |
|-------------|------|---------|
| **ARGO_CHATBOT** | 🌐 Web App | Natural language query interface with maps & charts |
| **DATA_GENERATOR** | 🖥️ Desktop App | ETL pipeline for fetching ARGO data into PostgreSQL |

---

## 📁 Project Structure

```
ARGOFLOAT-CHART/
├── .env.example           # Environment template (copy to .env)
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
├── README.md              # This file
│
├── ARGO_CHATBOT/          # 🌐 Web Application
│   ├── app.py             # Flask server (main entry point)
│   ├── brain.py           # NLP & SQL generation
│   ├── sql_builder.py     # Query construction
│   ├── database_utils.py  # Database utilities
│   ├── requirements.txt   # Python dependencies
│   ├── README.md          # Detailed documentation
│   └── static/
│       ├── index.html     # Web frontend
│       ├── css/styles.css # Styling
│       └── js/app.js      # JavaScript
│
└── DATA_GENERATOR/        # 🖥️ Desktop Application
    ├── gui.py             # Tkinter GUI (main entry point)
    ├── config.py          # Configuration settings
    ├── env_utils.py       # Environment loading
    ├── update_manager.py  # Update orchestration
    ├── requirements.txt   # Python dependencies
    └── pipeline/
        ├── netcdf_fetcher.py    # ERDDAP data fetcher
        ├── netcdf_transformer.py # Data transformation
        ├── db_loader.py         # PostgreSQL loader
        └── state_manager.py     # Checkpoint tracking
```

---

## 🚀 Quick Start

### Step 1: Clone & Setup Environment

```bash
git clone <repository-url>
cd ARGOFLOAT-CHART

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate
```

### Step 2: Configure Environment Variables

```bash
# Copy the template
cp .env.example .env

# Edit .env with your values:
# - DATABASE_URL: Your PostgreSQL connection string
# - GROQ_API_KEY: Your Groq API key (for chatbot)
```

### Step 3: Setup Database

Create a PostgreSQL database and table:

```sql
CREATE DATABASE argo_db;

\c argo_db

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

-- Create indexes for performance
CREATE INDEX idx_argo_float_id ON argo_data(float_id);
CREATE INDEX idx_argo_timestamp ON argo_data(timestamp);
CREATE INDEX idx_argo_location ON argo_data(latitude, longitude);

-- Unique constraint to prevent duplicates
CREATE UNIQUE INDEX idx_argo_unique ON argo_data(float_id, timestamp, pressure);
```

### Step 4: Populate Data (DATA_GENERATOR)

```bash
cd DATA_GENERATOR
pip install -r requirements.txt

# Run the GUI
python -m DATA_GENERATOR.gui
```

Click **"Update Latest Data"** to fetch ARGO float data from ERDDAP.

### Step 5: Run the Web Application (ARGO_CHATBOT)

```bash
cd ARGO_CHATBOT
pip install -r requirements.txt

# Start the web server
python app.py
```

Open your browser: **http://127.0.0.1:5000**

---

## 🌐 ARGO_CHATBOT (Web Application)

A modern web interface for querying ocean data using natural language.

### Features
- 💬 **Natural Language Queries** - Ask questions in plain English
- 🗺️ **Interactive Map** - Leaflet.js with dark theme
- 📊 **Dynamic Charts** - Chart.js visualizations
- 📋 **Data Tables** - Browse and export results
- 📜 **Query History** - Saved in browser localStorage
- ⬇️ **CSV Export** - Download query results

### Example Queries
- "What are the nearest ARGO floats to Chennai?"
- "Show temperature trends in the Arabian Sea"
- "What is the average salinity in Bay of Bengal?"
- "Show trajectory of float 2902115"

### Tech Stack
- **Backend**: Flask, SQLAlchemy, LangChain + Groq
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Map**: Leaflet.js
- **Charts**: Chart.js

---

## 🖥️ DATA_GENERATOR (Desktop Application)

A Tkinter GUI for managing the ARGO data pipeline.

### Features
- ⬇️ **One-Click Updates** - Fetch latest ARGO profiles from ERDDAP
- 📊 **Database Snapshot** - View current data statistics
- 📋 **Activity Log** - Track pipeline progress
- 🔄 **Incremental Updates** - Only fetches new data since last run

### Data Source
- **ERDDAP**: Ifremer ARGO BGC synthetic profiles
- **Region**: Indian Ocean (50°E-100°E, 20°S-25°N)
- **Parameters**: Temperature, Salinity, Dissolved Oxygen, Chlorophyll

---

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `GROQ_API_KEY` | ✅ (Chatbot) | Groq API key for NLP |
| `GROQ_MODEL_NAME` | ❌ | LLM model (default: llama-3.3-70b-versatile) |
| `SHOW_INTENT_JSON` | ❌ | Debug mode (0 or 1) |

### Supported Locations (Chatbot)

| Location | Coordinates |
|----------|-------------|
| Arabian Sea | 5°N-25°N, 50°E-75°E |
| Bay of Bengal | 5°N-22°N, 80°E-95°E |
| Andaman Sea | 5°N-15°N, 92°E-98°E |
| Chennai | 12.5°N-13.5°N, 80°E-80.5°E |
| Mumbai | 18.5°N-19.5°N, 72.5°E-73°E |
| Sri Lanka | 5°N-10°N, 79°E-82°E |
| Equator | 2°S-2°N |

---

## 🐛 Troubleshooting

### Database Connection Failed
- Ensure PostgreSQL is running
- Verify `DATABASE_URL` in `.env` file
- Check that `argo_data` table exists

### No Data in Chatbot
- Run DATA_GENERATOR first to populate the database
- Check database has records: `SELECT COUNT(*) FROM argo_data;`

### Groq API Errors
- Verify `GROQ_API_KEY` in `.env` file
- Check API key at [console.groq.com](https://console.groq.com)

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- [ARGO Program](https://argo.ucsd.edu/) - Global ocean observation network
- [Ifremer ERDDAP](https://erddap.ifremer.fr/) - ARGO data access
- [Groq](https://groq.com/) - Fast LLM inference
- [Leaflet](https://leafletjs.com/) - Interactive maps
- [Chart.js](https://www.chartjs.org/) - Data visualization

---

Made with 💙 for Ocean Science
