# 🌍 Global Seismic Trends: Data-Driven Earthquake Insights

## 📋 Project Overview

This project analyzes global earthquake data to identify seismic patterns, trends, and risk zones using data-driven approaches. The system retrieves earthquake data from the USGS API, processes it using Python, stores it in MySQL, and presents insights through interactive visualizations.

---

## 🎯 Problem Statement

Analyze and interpret global earthquake data to:
- Identify seismic patterns and trends
- Detect high-risk zones
- Support disaster management strategies
- Enable informed decision-making for governments, insurers, and researchers

---

## 🚀 Business Use Cases

1. **Risk Assessment**: Enable governments and insurers to assess earthquake risks in different regions
2. **Disaster Management**: Plan and optimize disaster response strategies
3. **Urban Safety**: Support data-driven policies for infrastructure resilience
4. **Research**: Provide comprehensive data for seismological research
5. **Emergency Response**: Facilitate effective emergency preparedness

---

## 🛠️ Skills & Technologies

### Technical Skills
- **Python**: Data retrieval, cleaning, and analysis
- **Regular Expressions (Regex)**: Text parsing and data extraction
- **SQL**: Complex queries and database management
- **MySQL**: Relational database design and optimization
- **Streamlit**: Interactive dashboard development
- **Data Visualization**: Plotly, Matplotlib, Seaborn

### Domain Knowledge
- Disaster Management
- Geoscience
- Seismology
- Data Analytics

---

## 📊 Dataset Description

### Data Source
- **API**: USGS Earthquake API
- **URL**: https://earthquake.usgs.gov/fdsnws/event/1/query
- **Time Range**: Last 5 years (2021-2025)
- **Minimum Magnitude**: 3.0

### Features (26 Core + Derived)

#### Core Features
1. **id**: Unique earthquake identifier
2. **time**: Earthquake timestamp
3. **updated**: Last update timestamp
4. **latitude**: Epicenter latitude
5. **longitude**: Epicenter longitude
6. **depth_km**: Earthquake depth
7. **mag**: Magnitude value
8. **magType**: Magnitude measurement type
9. **place**: Location description
10. **status**: Review status (reviewed/automatic)
11. **tsunami**: Tsunami indicator
12. **sig**: Significance metric
13. **net**: Reporting network
14. **nst**: Number of reporting stations
15. **dmin**: Distance to nearest station
16. **rms**: Root mean square residual
17. **gap**: Azimuthal gap
18. **magError**: Magnitude uncertainty
19. **depthError**: Depth uncertainty
20. **magNst**: Stations for magnitude
21. **locationSource**: Location reporting agency
22. **magSource**: Magnitude reporting agency
23. **types**: Data types available
24. **ids**: Associated IDs
25. **sources**: Reporting sources
26. **type**: Event type

#### Derived Features
- **country**: Extracted from place
- **region**: Extracted from place
- **distance_km**: Distance from location
- **year, month, day, hour**: Time components
- **day_of_week, day_name, month_name**: Calendar info
- **quarter**: Fiscal quarter
- **depth_category**: shallow/intermediate/deep
- **magnitude_category**: light/moderate/strong/major/great
- **is_destructive**: Destructive potential flag
- **continent**: Estimated continent

---

## 📁 Project Structure

```
earthquake-analysis/
│
├── 01_data_retrieval.py          # API data fetching
├── 
├── 02_database_setup.py          # MySQL setup & loading
├── 03_sql_analysis.sql           # Analytical SQL queries
├── 04_streamlit_dashboard.py    # Interactive dashboard
│
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
│
├── data/                         # Data directory
│   ├── earthquakes.csv
│
└── outputs/                      # Analysis outputs
    ├── visualizations/
    └── reports/
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/earthquake-analysis.git
cd earthquake-analysis
```

### Step 2: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 3: Configure MySQL
1. Install MySQL Server
2. Create database user
3. Update database credentials in scripts:
   - `03_database_setup.py`
   - `05_streamlit_dashboard.py`

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'earthquake_db'
}
```

---

## 🚀 Execution Guide

### Step 1: Data Retrieval
Fetch earthquake data from USGS API:
```bash
python 01_data_retrieval.py
```
**Output**: `earthquake_raw_data.csv`

### Step 2: Data Preprocessing
Clean and transform the data:
```bash
python 02_data_preprocessing.py
```
**Output**: `earthquake_cleaned_data.csv`

### Step 3: Database Setup
Create MySQL database and load data:
```bash
python 03_database_setup.py
```
**Output**: MySQL database `earthquake_db` with tables

### Step 4: SQL Analysis
Run analytical queries:
```bash
mysql -u root -p earthquake_db < 04_sql_analysis.sql
```
**Output**: Query results and insights

### Step 5: Launch Dashboard
Start the interactive Streamlit dashboard:
```bash
streamlit run 05_streamlit_dashboard.py
```
**Access**: http://localhost:8501

---

## 📊 Key Analyses & Insights

### 1. Magnitude Analysis
- Distribution of earthquake magnitudes
- Strongest earthquakes globally
- Magnitude trends over time
- Average magnitude by region

### 2. Depth Analysis
- Shallow vs deep earthquakes
- Depth distribution patterns
- Correlation between depth and magnitude
- Regional depth characteristics

### 3. Temporal Patterns
- Yearly earthquake trends
- Monthly and seasonal patterns
- Hour-of-day distributions
- Growth rate analysis

### 4. Geographic Analysis
- Global earthquake distribution
- High-risk countries and regions
- Continental patterns
- Seismically active zones

### 5. Tsunami Analysis
- Tsunami-triggering events
- Magnitude thresholds for tsunamis
- Geographic tsunami patterns
- Temporal tsunami trends

### 6. Data Quality Metrics
- Station coverage analysis
- Measurement reliability
- Review status distribution
- Error margin analysis

---

## 📈 Sample SQL Queries

### Top 10 Strongest Earthquakes
```sql
SELECT id, time, place, country, mag, depth_km
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;
```

### Year with Most Earthquakes
```sql
SELECT year, COUNT(*) as total_earthquakes
FROM earthquakes
GROUP BY year
ORDER BY total_earthquakes DESC;
```

### Countries with Highest Average Magnitude
```sql
SELECT country, COUNT(*) as total, 
       ROUND(AVG(mag), 2) as avg_magnitude
FROM earthquakes
WHERE country != 'unknown'
GROUP BY country
HAVING total >= 10
ORDER BY avg_magnitude DESC
LIMIT 5;
```

---

## 🎨 Dashboard Features

### Interactive Visualizations
- **Temporal Trends**: Line charts showing earthquake frequency over time
- **Magnitude Distribution**: Histograms and pie charts
- **Depth Analysis**: Distribution plots and scatter plots
- **Geographic Maps**: Global earthquake distribution
- **Tsunami Analysis**: Comparative visualizations

### Filters & Controls
- Year selection
- Magnitude range slider
- Depth category filter
- Continental filter
- Country selection

### Data Export
- Download filtered data as CSV
- Export visualizations as images
- Generate custom reports

---

## 📝 Key Findings

### 1. Seismic Activity Patterns
- Approximately 100,000+ earthquakes recorded (mag ≥ 3.0)
- Ring of Fire accounts for 75%+ of major earthquakes
- Consistent seismic activity with seasonal variations

### 2. Magnitude Insights
- Most earthquakes are moderate (mag 3.0-5.0)
- Major earthquakes (mag ≥ 7.0) are rare but impactful
- Average global magnitude: ~4.2

### 3. Depth Characteristics
- Shallow earthquakes (< 50km) are most common
- Deep earthquakes (> 300km) occur in subduction zones
- Shallow events more likely to be destructive

### 4. Geographic Patterns
- Pacific Ring: Indonesia, Japan, Chile, Alaska
- High activity: California, Philippines, Turkey
- Increasing urbanization in high-risk zones

### 5. Tsunami Risk
- ~2-3% of earthquakes trigger tsunamis
- Tsunami events typically magnitude > 6.5
- Primarily occur in ocean/coastal regions

---

## 🎯 Project Evaluation Metrics

| Metric | Weight | Focus Area |
|--------|--------|------------|
| Data Cleaning Accuracy | 35% | Preprocessing, regex, derived fields |
| SQL Query Effectiveness | 35% | Correctness, complexity, efficiency |
| Visualization Quality | 10% | Clarity, interactivity, depth |
| Documentation | 10% | Insights explanation, methodology |
| Project Organization | 10% | Structure, naming, reproducibility |

---

## 🔮 Future Enhancements

1. **Machine Learning Models**
   - Earthquake prediction algorithms
   - Risk assessment models
   - Anomaly detection

2. **Real-time Monitoring**
   - Live data feeds
   - Automated alerts
   - Real-time dashboard updates

3. **Advanced Analytics**
   - Spatial clustering analysis
   - Network analysis of fault lines
   - Time series forecasting

4. **Enhanced Visualizations**
   - 3D earthquake visualization
   - Animated temporal maps
   - Interactive fault line mapping

5. **Integration**
   - Population density overlay
   - Infrastructure vulnerability assessment
   - Economic impact analysis

---

## 📚 References

- **USGS Earthquake API**: https://earthquake.usgs.gov/fdsnws/event/1/
- **USGS Documentation**: https://earthquake.usgs.gov/data/
- **Seismology Resources**: https://www.iris.edu/
- **Streamlit Documentation**: https://docs.streamlit.io/

---


## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📧 Contact


- GitHub Issues: [Project Issues](https://github.com/yourusername/earthquake-analysis/issues)

---

## 🙏 Acknowledgments

- USGS for providing comprehensive earthquake data
- Open-source community for tools and libraries
- Seismology research community for domain knowledge

---

**Last Updated**: January 2026
