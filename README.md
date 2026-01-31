# 🌊 FloatChart

**AI-Powered Ocean Data Intelligence** - Chat with 46 million ARGO float records using natural language.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🤖 **AI Chat** - Ask questions about ocean data in natural language
- 🗺️ **Interactive Map** - Explore float positions worldwide
- 📊 **Dashboard** - Visualize temperature, salinity trends
- ⬇️ **Data Manager** - Download ARGO data from ERDDAP servers

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/floatchart.git
cd floatchart

# Run setup
python local_setup.py

# Edit credentials
# ARGO_CHATBOT/.env

# Start the chat app
cd ARGO_CHATBOT
python app.py
# → Opens at http://localhost:5000
```

## 📂 Project Structure

```
FloatChart/
├── ARGO_CHATBOT/          # Chat Application
│   ├── app.py             # Flask server
│   ├── brain.py           # AI query logic
│   ├── sql_builder.py     # SQL generation
│   └── static/            # Web UI (HTML, CSS, JS)
│
├── DATA_GENERATOR/        # Data Management
│   ├── app.py             # Web-based data manager
│   ├── data_manager.py    # Data fetch API
│   ├── database_utils.py  # Database operations
│   ├── bulk_fetch.py      # CLI bulk fetcher
│   └── static/            # Data manager UI
│
├── requirements.txt       # Python dependencies
├── local_setup.py         # One-click setup
└── .env.example           # Configuration template
```

## 🔧 Configuration

Create `ARGO_CHATBOT/.env`:

```env
# Database (CockroachDB - Free 10GB at cockroachlabs.cloud)
DATABASE_URL=postgresql://user:pass@host:26257/database?sslmode=verify-full

# AI Provider (Groq - Free at console.groq.com)
GROQ_API_KEY=your_api_key_here
```

## 📥 Getting Data

### Option 1: Web Interface
```bash
cd DATA_GENERATOR
python app.py
# → Opens at http://localhost:5001
```

### Option 2: Command Line
```bash
cd DATA_GENERATOR
python bulk_fetch.py --fetch-all          # All data from 2002
python bulk_fetch.py --fetch-year 2024    # Specific year
python bulk_fetch.py --stats              # Database stats
```

## 🖥️ Running the Apps

### Chat App (Main Interface)
```bash
cd ARGO_CHATBOT
python app.py
```
- **http://localhost:5000** - Chat Interface
- **http://localhost:5000/map** - Interactive Map
- **http://localhost:5000/dashboard** - Analytics

### Data Manager
```bash
cd DATA_GENERATOR
python app.py
```
- **http://localhost:5001** - Data Management UI

## 💬 Example Queries

- "What's the average temperature in Bay of Bengal?"
- "Show me floats near Chennai from 2024"
- "Compare salinity between Arabian Sea and Indian Ocean"
- "How many floats are active this month?"

## 🔗 Resources

- [ARGO Program](https://argo.ucsd.edu) - Global ocean observation
- [CockroachDB](https://cockroachlabs.cloud) - Free 10GB database
- [Groq](https://console.groq.com) - Free AI API
- [ERDDAP](https://erddap.ifremer.fr) - ARGO data source

## 📄 License

MIT License - feel free to use and modify!
