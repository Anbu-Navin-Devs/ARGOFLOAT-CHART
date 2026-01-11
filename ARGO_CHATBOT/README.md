# 🌊 FloatChat - Ocean Intelligence Web Application

A modern web-based application for querying and visualizing ARGO float oceanographic data using natural language processing.

![FloatChat Screenshot](docs/screenshot.png)

## ✨ Features

- **Natural Language Queries**: Ask questions about ocean data in plain English
- **Interactive Map**: Visualize float locations and trajectories on a dark-themed Leaflet map
- **Dynamic Charts**: View data as time series, profiles, or trajectory plots using Chart.js
- **Data Table**: Browse and export query results
- **Query History**: Keep track of your recent queries
- **Period Filtering**: Filter data by year and month
- **Export to CSV**: Download query results for further analysis
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8+** installed on your system
2. **PostgreSQL** database with ARGO float data
3. **Groq API Key** for natural language processing

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ARGOFLOAT-CHART
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   cd ARGO_CHATBOT
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   
   Create a `.env` file in the `ARGO_CHATBOT` folder:
   ```env
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/argo_db
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL_NAME=llama-3.3-70b-versatile
   ```

### Database Setup

The application expects a PostgreSQL database with an `argo_data` table containing:

```sql
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
    chlorophyll DOUBLE PRECISION,
    nitrate DOUBLE PRECISION,
    ph DOUBLE PRECISION
);

-- Create indexes for better performance
CREATE INDEX idx_argo_float_id ON argo_data(float_id);
CREATE INDEX idx_argo_timestamp ON argo_data(timestamp);
CREATE INDEX idx_argo_location ON argo_data(latitude, longitude);
```

If you need to populate the database, you can use the `DATA_GENERATOR` module included in this project. It can fetch data from ARGO data centers and load it into your PostgreSQL database.

### Running the Application

1. **Start the web server**:
   ```bash
   cd ARGO_CHATBOT
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. **Start asking questions!** Examples:
   - "What are the nearest ARGO floats to Chennai?"
   - "Show temperature trends in the Arabian Sea"
   - "What is the average salinity in Bay of Bengal?"
   - "Show trajectory of float 2902115"
   - "Compare BGC parameters in the Arabian Sea for the last 6 months"

## 📁 Project Structure

```
ARGO_CHATBOT/
├── app.py                 # Flask web server & API endpoints (main entry)
├── brain.py               # Natural language processing & SQL generation
├── sql_builder.py         # Query construction logic
├── database_utils.py      # Database connection utilities
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── README.md              # This documentation
└── static/
    ├── index.html         # Main web application
    ├── css/
    │   └── styles.css     # Application styles
    └── js/
        └── app.js         # Frontend JavaScript
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve the web application |
| `/api/status` | GET | Check API and database status |
| `/api/query` | GET | Process natural language queries |
| `/api/locations` | GET | Get supported geographic locations |
| `/api/available_periods` | GET | Get available years and months |
| `/api/nearest_floats` | GET | Find nearest floats to coordinates |
| `/api/float_profile/<id>` | GET | Get depth profile for a float |
| `/api/float_trajectory/<id>` | GET | Get trajectory path for a float |
| `/api/statistics` | GET | Get dataset statistics |

### Query Endpoint Parameters

```
GET /api/query?question=<your question>&year=<optional>&month=<optional>
```

## 🗺️ Supported Locations

The application recognizes these predefined regions:
- Arabian Sea
- Bay of Bengal
- Equator
- Andaman Sea
- Chennai
- Mumbai
- Sri Lanka

You can also specify coordinates directly in your query.

## 🎨 Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **LangChain + Groq** - Natural language processing
- **PostgreSQL** - Database

### Frontend
- **HTML5/CSS3** - Modern, responsive layout
- **JavaScript (ES6+)** - Interactive functionality
- **Leaflet.js** - Interactive maps
- **Chart.js** - Data visualization
- **Inter Font** - Typography

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `GROQ_API_KEY` | Groq API key for LLM | Required |
| `GROQ_MODEL_NAME` | LLM model to use | `llama-3.3-70b-versatile` |
| `SHOW_INTENT_JSON` | Show debug intent info | `0` |

### Customizing the Server

You can customize the server settings in `app.py`:

```python
start_api_server(
    host="127.0.0.1",  # Change to "0.0.0.0" for external access
    port=5000,          # Change port if needed
    debug=True          # Set to False in production
)
```

## 📊 Query Types

The application supports various query types:

1. **Proximity**: "What are the nearest floats to Chennai?"
2. **Time-Series**: "Show temperature trends in the Arabian Sea"
3. **Statistic**: "What is the average salinity in Bay of Bengal?"
4. **Profile**: "Show depth profile for float 2902115"
5. **Trajectory**: "Show trajectory of float 2902115"
6. **Scatter**: "Compare temperature vs salinity"
7. **General**: Any other oceanographic question

## 🐛 Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env` file
- Ensure the `argo_data` table exists

### API Key Issues
- Verify `GROQ_API_KEY` in `.env` file
- Check API key validity at [console.groq.com](https://console.groq.com)

### Empty Results
- Check if data exists for the queried location/time
- Try broader queries first
- Use the period selectors to filter available data

### Port Already in Use
```bash
# Find and kill the process using port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- [ARGO Program](https://argo.ucsd.edu/) for oceanographic float data
- [Groq](https://groq.com/) for LLM inference
- [Leaflet](https://leafletjs.com/) for interactive maps
- [Chart.js](https://www.chartjs.org/) for data visualization

---

Made with 💙 for Ocean Science
