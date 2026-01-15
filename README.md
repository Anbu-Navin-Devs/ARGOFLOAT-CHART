# 🌊 FloatChart – AI-Powered Ocean Intelligence Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-purple?style=for-the-badge&logo=supabase)
![LangChain](https://img.shields.io/badge/LangChain-AI-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An AI-powered web application for querying and visualizing ARGO float oceanographic data using natural language.**

[🌐 Live Demo](https://argofloat-chart.onrender.com) • [📖 Documentation](#-features) • [🚀 Quick Start](#-quick-start)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Live Demo](#-live-demo)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Sample Queries](#-sample-queries)
- [API Reference](#-api-reference)
- [Data Coverage](#-data-coverage)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌐 Overview

**FloatChart** is an intelligent oceanographic data platform that allows users to query over **1.5 million ARGO float records** using natural language. The system leverages AI (LLM) to interpret user questions, generate SQL queries, and present results through interactive visualizations.

### What are ARGO Floats?
ARGO floats are autonomous profiling instruments that drift with ocean currents, diving to depths of 2000m and measuring temperature, salinity, and pressure. Over 4,000 floats are currently deployed worldwide, providing critical data for climate research and oceanography.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **Natural Language Queries** | Ask questions in plain English - no SQL knowledge required |
| 🗺️ **Interactive Map Explorer** | Click anywhere on the ocean to find nearby floats |
| 📊 **Dynamic Visualizations** | Temperature, salinity, and depth charts with multiple view options |
| 📈 **Float Trajectories** | Track float movement paths over time |
| 🔍 **Proximity Search** | Find floats near any coastal city or coordinates |
| 📋 **Data Tables** | Browse, filter, and export query results |
| ⬇️ **CSV Export** | Download data for offline analysis |
| 🌡️ **Real-time Stats** | Temperature, salinity averages, and float counts |

---

## 🌐 Live Demo

**🔗 [https://argofloat-chart.onrender.com](https://argofloat-chart.onrender.com)**

### Database Statistics
| Metric | Value |
|--------|-------|
| **Total Records** | 1,513,324+ |
| **Date Range** | January 2020 - June 2026 |
| **Coverage** | Global (Pacific, Atlantic, Indian Ocean, Mediterranean, Caribbean) |
| **Metrics** | Temperature, Salinity, Pressure, Dissolved Oxygen |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core programming language |
| **Flask 3.0** | Web framework |
| **LangChain** | AI/LLM orchestration |
| **Groq (LLaMA 3.3-70B)** | Fast LLM inference |
| **Google Gemini** | Fallback LLM provider |
| **SQLAlchemy** | Database ORM |
| **Supabase PostgreSQL** | Cloud database |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5/CSS3** | Modern responsive design |
| **JavaScript (ES6+)** | Interactive functionality |
| **Leaflet.js** | Interactive maps |
| **Chart.js** | Data visualizations |

### Deployment
| Service | Purpose |
|---------|---------|
| **Render** | Cloud hosting platform |
| **Gunicorn** | WSGI server |
| **GitHub** | Version control |

---

## 📁 Project Structure

```
ARGOFLOAT-CHART/
│
├── 📂 ARGO_CHATBOT/              # Main Web Application
│   ├── app.py                    # Flask server & API routes
│   ├── brain.py                  # AI/NLP processing with LangChain
│   ├── sql_builder.py            # Dynamic SQL query generation
│   ├── database_utils.py         # Database connection utilities
│   ├── requirements.txt          # Python dependencies
│   ├── Procfile                  # Render deployment config
│   │
│   └── 📂 static/                # Frontend Assets
│       ├── index.html            # Main chat interface
│       ├── map.html              # Interactive map explorer
│       ├── 📂 css/
│       │   └── styles.css        # Global styles (glassmorphism)
│       └── 📂 js/
│           └── app.js            # Frontend JavaScript
│
├── 📂 DATA_GENERATOR/            # Data Management (Optional)
│   ├── gui.py                    # Desktop GUI for data updates
│   ├── config.py                 # Configuration settings
│   └── update_manager.py         # Data synchronization
│
├── README.md                     # Project documentation
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Anbu-2006/ARGOFLOAT-CHART.git
cd ARGOFLOAT-CHART

# 2. Navigate to the chatbot directory
cd ARGO_CHATBOT

# 3. Create virtual environment
python -m venv .venv

# 4. Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the application
python app.py
```

### Environment Variables

Create a `.env` file in the `ARGO_CHATBOT` folder:

```env
# Database (Required)
DATABASE_URL=postgresql://user:password@host:5432/database

# LLM Provider (At least one required)
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key

# Optional Settings
GROQ_MODEL_NAME=llama-3.3-70b-versatile
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

---

## 💬 Sample Queries

### 📍 Location-Based Queries
```
• "Find 5 nearest floats to Chennai"
• "Show floats in Bay of Bengal"
• "Floats near Mumbai"
• "Data from Arabian Sea"
• "Floats around Kollam"
```

### 🌡️ Data Analysis
```
• "Average temperature in Indian Ocean"
• "Maximum salinity in Pacific Ocean"
• "Temperature trends in 2024"
• "Compare temperature and salinity"
```

### 🔢 Specific Float Queries
```
• "Show data for float 2902115"
• "Trajectory of float 5907083"
• "All records from float 2700917"
```

### 📊 Statistical Queries
```
• "How many floats are in the database?"
• "Count floats in Mediterranean Sea"
• "Average temperature this year"
```

### Supported Locations

| Category | Locations |
|----------|-----------|
| **Indian Ocean** | Arabian Sea, Bay of Bengal, Andaman Sea, Laccadive Sea, Red Sea, Persian Gulf |
| **Pacific Ocean** | South China Sea, Philippine Sea, Coral Sea, Tasman Sea |
| **Atlantic Ocean** | Caribbean Sea, Gulf of Mexico, Mediterranean Sea, North Sea |
| **Indian Cities** | Chennai, Mumbai, Kollam, Kochi, Goa, Kolkata, Vizag, Mangalore, Tuticorin, Pondicherry, Trivandrum, Surat, Kandla, Paradip, Port Blair |
| **International** | Singapore, Tokyo, Sydney, Cape Town, Miami, Maldives, Mauritius, Sri Lanka |

---

## 📡 API Reference

### Base URL
```
https://argofloat-chart.onrender.com/api
```

### Endpoints

#### `GET /api/status`
Check server and database status.

**Response:**
```json
{
  "status": "online",
  "database": "connected",
  "records": 1513324,
  "timestamp": "2026-01-16T12:00:00Z"
}
```

#### `POST /api/query`
Process a natural language query.

**Request:**
```json
{
  "query": "Find 5 nearest floats to Chennai"
}
```

**Response:**
```json
{
  "success": true,
  "query_type": "Proximity",
  "sql": "SELECT ... FROM argo_data ...",
  "data": [...],
  "summary": "Found 5 floats near Chennai...",
  "chart_type": "map"
}
```

---

## 🗺️ Data Coverage

### Geographic Distribution

| Region | Records | Coverage |
|--------|---------|----------|
| Indian Ocean | 400,000+ | Full coverage |
| Pacific Ocean | 450,000+ | Extensive coverage |
| Atlantic Ocean | 350,000+ | Good coverage |
| Mediterranean | 150,000+ | Complete coverage |
| Southern Ocean | 100,000+ | Antarctic waters |
| Caribbean Sea | 50,000+ | Regional coverage |

### Temporal Coverage
- **Start Date:** January 2020
- **End Date:** June 2026
- **Total Span:** 6+ years of oceanographic data

### Data Schema

| Field | Type | Description |
|-------|------|-------------|
| `float_id` | Integer | Unique ARGO float identifier |
| `timestamp` | DateTime | Observation date/time (UTC) |
| `latitude` | Float | Geographic latitude (-90 to 90) |
| `longitude` | Float | Geographic longitude (-180 to 180) |
| `temperature` | Float | Water temperature in Celsius |
| `salinity` | Float | Salinity in PSU |
| `pressure` | Float | Depth pressure in dbar |
| `dissolved_oxygen` | Float | Oxygen concentration (μmol/kg) |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add comments for complex logic
- Update documentation as needed

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[ARGO Program](https://argo.ucsd.edu/)** - Global ocean observation network
- **[ERDDAP](https://coastwatch.pfeg.noaa.gov/erddap/)** - Oceanographic data distribution
- **[Groq](https://groq.com/)** - Fast LLM inference
- **[Supabase](https://supabase.com/)** - Managed PostgreSQL hosting
- **[Render](https://render.com/)** - Cloud deployment platform
- **[LangChain](https://langchain.com/)** - LLM application framework

---

## 📞 Contact

| | |
|---|---|
| **Developer** | Anbu |
| **GitHub** | [@Anbu-2006](https://github.com/Anbu-2006) |
| **Project** | [ARGOFLOAT-CHART](https://github.com/Anbu-2006/ARGOFLOAT-CHART) |

---

<div align="center">

### 🌊 Made with ❤️ for Ocean Research

**⭐ Star this repo if you find it helpful!**

</div>
