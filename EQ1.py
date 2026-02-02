import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import re
import matplotlib.pyplot as plt


st.title("Globel seismic trends")
st.markdown("""
This dashboard analyzes **global earthquake data (2019–2023)**  
Source: **USGS Earthquake API**
""")
# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("## ⚙️ Dashboard Controls")

data_source = st.sidebar.radio(
    "Select Data Source",
    ["CSV File"," MySQL Database"]
)
st.title("data  overview")
df = pd.read_csv("EQ.csv")
st.write(df)
st.divider()
#load data
@st.cache_data
def load_data():
    df = pd.read_csv("EQ.csv")
    df["time"] = pd.to_datetime(df["time"])
    return df

df = load_data()
#dataset 
st.header("📄 Dataset Overview")

st.write("Shape:", df.shape)
st.dataframe(df.head())
#key mag/dep
st.header(" Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Earthquakes", len(df))
col2.metric("Max Magnitude", round(df["mag"].max(), 2))
col3.metric("Avg Depth (km)", round(df["depth_km"].mean(), 2))
#visual mag distri
st.header("📈 Earthquake Magnitude Distribution")

fig, ax = plt.subplots()
ax.hist(df["mag"], bins=20)
ax.set_xlabel("Magnitude")
ax.set_ylabel("Frequency")
ax.set_title("Distribution of Earthquake Magnitudes")

st.pyplot(fig)







# make sure time is datetime
df["time"] = pd.to_datetime(df["time"])

# extract year
df["year"] = df["time"].dt.year

# count earthquakes per year
year_counts = df["year"].value_counts().sort_index()
# assume df already loaded from SQL
df["time"] = pd.to_datetime(df["time"])   # IMPORTANT
df["year"] = df["time"].dt.year            # CREATE year

year_counts = df["year"].value_counts().sort_index()

st.subheader("Earthquakes per Year")
st.bar_chart(year_counts)





url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

all_records = []
start_year = datetime.now().year - 5   # last 5 years
end_year = datetime.now().year

for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"

        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": 3
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"⚠️ Failed for {start_date}: {response.text[:200]}")
            continue

        try:
            data = response.json()
        except Exception as e:
            print(f"⚠️ JSON error for {start_date}: {e}")
            continue

        for f in data["features"]:
            p = f["properties"]
            g = f["geometry"]["coordinates"]
            all_records.append({
                "id": f.get("id"),
                "time": pd.to_datetime(p.get("time"), unit="ms"),
                "updated": pd.to_datetime(p.get("updated"), unit="ms"),
                "latitude": g[1] if g else None,
                "longitude": g[0] if g else None,
                "depth_km": g[2] if g else None,
                "mag": p.get("mag"),
                "magType": p.get("magType"),
                "place": p.get("place"),
                "status": p.get("status"),
                "tsunami": p.get("tsunami"),
                "alert": p.get("alert"),
                "felt": p.get("felt"),
                "cdi": p.get("cdi"),
                "mmi": p.get("mmi"),
                "sig": p.get("sig"),
                "net": p.get("net"),
                "code": p.get("code"),
                "ids": p.get("ids"),
                "sources": p.get("sources"),
                "types": p.get("types"),
                "nst": p.get("nst"),
                "dmin": p.get("dmin"),
                "rms": p.get("rms"),
                "gap": p.get("gap"),
                "type": p.get("type")








              # Event type
            })

#Convert to DataFrame
df = pd.DataFrame(all_records)
# Summary
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print(df.head())



# Variables prepared
all_records = []
start_year = datetime.now().year - 5
end_year = datetime.now().year

# Loop through years
for year in range(start_year, end_year + 1):
    for month in range(1, 13):

        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        # Example: just print the range
        print(start_date, "→", end_date)


params = { 
    "format": "geojson",      # Request data in GeoJSON format (easy to parse)
    "starttime": "2024-01-01", # Start of the time range
    "endtime": "2024-02-01",   # End of the time range
    "minmagnitude": 3           # Only earthquakes magnitude >= 3
}

print(params)
if response.status_code != 200:
    # Print the first 200 characters of the error message
    print("⚠️ Request failed:", response.text[:200])
else:
    print("✅ Success! Data fetched.")
    print(response)

print(data)
#SAVE DATAFRAME TO CSV
df.to_csv("EQ.csv", index=False)
print(" CSV saved: EQ.csv")

#MAGNITUDE BOXPLOT
import matplotlib.pyplot as plt

plt.figure(figsize=(6,4))
plt.boxplot(df["mag"].dropna())
plt.title("Earthquake Magnitude Distribution (2019)")
plt.ylabel("Magnitude")
plt.show()




import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# ---------------------------
# MySQL Database Connection
# ---------------------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "priyadharshini123"
DB_NAME = "test_db"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")


#sql queries -------
query = "SELECT * FROM earthquakes"
df = pd.read_sql(query, engine) 
def get_continent(place):
    if place is None:
        return "Unknown"
    place = place.lower()
    if "india" in place:
        return "Asia"
    elif "japan" in place:
        return "Asia"
    elif "california" in place:
        return "North America"
    else:
        return "Other"
    
df["continent"] = df["place"].apply(get_continent)

df = pd.read_sql(query, engine)
st.dataframe(df)


queries = {

    


    # ---------------- Magnitude & Depth ----------------
    "1. Top 10 strongest earthquakes (mag)": """
        SELECT place, mag, time
        FROM earthquakes
        ORDER BY mag DESC
        LIMIT 10;
    """,

    "2. Top 10 deepest earthquakes (depth_km)": """
        SELECT place, depth_km, mag
        FROM earthquakes
        ORDER BY depth_km DESC
        LIMIT 10;
    """,

    "3. Shallow earthquakes (<50 km) & mag > 7.5": """
       
        SELECT place, mag, depth_km
        FROM earthquakes
        WHERE depth_km < 50 AND mag > 7.5;
    """,

    "4. Average depth per continent": """
         SELECT 
            continent,
            ROUND(AVG(depth_km), 2) AS avg_depth_km
        FROM earthquakes
        GROUP BY continent
        ORDER BY avg_depth_km DESC;
    """,

    "5. Average magnitude per magType": """
        SELECT magType, ROUND(AVG(mag),2) AS avg_mag
        FROM earthquakes
        GROUP BY magType;
    """,

    # ---------------- Time Analysis ----------------
    

    "6. Year with most earthquakes": """
        SELECT 
        YEAR(time) AS year,
        COUNT(*) AS total_earthquakes
        FROM earthquakes
        GROUP BY YEAR(time)
        ORDER BY total_earthquakes DESC
        LIMIT 1;
    
    """,

 

    "7. Month with highest earthquakes": """
        SELECT MONTH(time) AS month, COUNT(*) AS total
        FROM earthquakes
        GROUP BY MONTH(time)
        ORDER BY total DESC
        LIMIT 1;
    
    """,

    "8. Day of week with most earthquakes": """
        SELECT DAYNAME(time) AS day, COUNT(*) AS total
        FROM earthquakes
        GROUP BY DAYNAME(time)
        ORDER BY total DESC;

    """,

    "9. Earthquakes per hour": """
        SELECT HOUR(time) AS hour, COUNT(*) AS total
        FROM earthquakes
        GROUP BY hour
        ORDER BY hour;
    """,

    "10. Most active reporting network (net)": """
        SELECT net, COUNT(*) AS total
        FROM earthquakes
        GROUP BY net
        ORDER BY total DESC
        LIMIT 1;
    """,

    # ---------------- Casualties & Economic Loss ----------------
    "11. Top 5 places with highest casualties":"""
        SELECT place, COUNT(*) AS total_earthquakes
        FROM earthquakes
        GROUP BY place
        ORDER BY total_earthquakes DESC
        LIMIT 5;

   
     """,

    "12. Total economic loss per continent": """
        SELECT continent, SUM(economic_loss) AS total_loss
        FROM earthquakes
        GROUP BY continent;
    """,

    "13. Average economic loss by alert level": """
        SELECT alert, ROUND(AVG(economic_loss),2) AS avg_loss
        FROM earthquakes
        GROUP BY alert;
    """,

    # ---------------- Event Type & Quality ----------------
    "14. Reviewed vs Automatic earthquakes": """
        SELECT status, COUNT(*) AS total
        FROM earthquakes
        GROUP BY status;
    """,

    "15. Count by earthquake type": """
        SELECT type, COUNT(*) AS total
        FROM earthquakes
        GROUP BY type;
    """,

    "16. Count by data types": """
        SELECT types, COUNT(*) AS total
        FROM earthquakes
        GROUP BY types;
    """,

    "17. Average RMS & gap per continent": """
        SELECT continent,
               ROUND(AVG(rms),3) AS avg_rms,
               ROUND(AVG(gap),2) AS avg_gap
        FROM earthquakes
        GROUP BY continent;
    """,

    "18. High station coverage (nst > 100)": """
        SELECT place, nst, mag
        FROM earthquakes
        WHERE nst > 100
        ORDER BY nst DESC;
    """,

    # ---------------- Tsunami & Alerts ----------------
    "19. Tsunamis triggered per year": """
        SELECT YEAR(time) AS year, COUNT(*) AS total
        FROM earthquakes
        WHERE tsunami = 1
        GROUP BY YEAR(time);

    """,

    "20. Earthquakes by alert level": """
        SELECT alert, COUNT(*) AS total
        FROM earthquakes
        GROUP BY alert;
    """,

    # ---------------- Seismic Patterns & Trends ----------------
    "21. Top 5 countries by avg magnitude (last 10 years)": """
        SELECT country, ROUND(AVG(mag),2) AS avg_mag
        FROM earthquakes
        WHERE YEAR(time) >= YEAR(CURDATE()) - 10
        GROUP BY country
        ORDER BY avg_mag DESC
        LIMIT 5;
    """,

    "22. Countries with shallow & deep earthquakes in same month": """
       SELECT
    country,
    YEAR(time) AS year,
    MONTH(time) AS month
    FROM earthquakes_2019_2023
    GROUP BY
    country,
    YEAR(time),
    MONTH(time)
    HAVING
    SUM(depth_km < 50) > 0
    AND SUM(depth_km > 300) > 0;

    """,

    "23. Year-over-year earthquake growth": """
        WITH yearly AS (
    SELECT
        YEAR(time) AS year,
        COUNT(*) AS total
    FROM earthquakes
    GROUP BY YEAR(time)
    )
    SELECT
        year,
        total,
        ROUND(
        (total - LAG(total) OVER (ORDER BY year)) /
        LAG(total) OVER (ORDER BY year) * 100,
        2
        ) AS growth_rate
    FROM yearly
    ORDER BY year;


    """,

    "24. Top 3 most seismically active regions": """
        SELECT continent,
               COUNT(*) AS frequency,
               ROUND(AVG(mag),2) AS avg_mag
        FROM earthquakes
        GROUP BY continent
        ORDER BY frequency * avg_mag DESC
        LIMIT 3;
    """,

    # ---------------- Depth, Location & Distance ----------------
    "25. Avg depth near equator (±5° latitude)": """
        SELECT country, ROUND(AVG(depth_km),2) AS avg_depth
        FROM earthquakes
        WHERE latitude BETWEEN -5 AND 5
        GROUP BY country;
    """,

    "26. Highest shallow-to-deep ratio by country": """
        SELECT country,
               SUM(depth_km < 50) / SUM(depth_km > 300) AS ratio
        FROM earthquakes
        GROUP BY country
        HAVING SUM(depth_km > 300) > 0
        ORDER BY ratio DESC;
    """,

    "27. Avg magnitude difference (tsunami vs non-tsunami)": """
        SELECT
          (SELECT AVG(mag) FROM earthquakes WHERE tsunami = 1) -
          (SELECT AVG(mag) FROM earthquakes WHERE tsunami = 0)
          AS mag_difference;
    """,

    "28. Lowest data reliability (high rms & gap)": """
        SELECT place, rms, gap
        FROM earthquakes
        ORDER BY (rms + gap) DESC
        LIMIT 10;
    """,

    "29. Consecutive earthquakes within 50 km & 1 hour": """
        SELECT a.id AS eq1, b.id AS eq2
        FROM earthquakes a
        JOIN earthquakes b
        ON a.time < b.time
        AND TIMESTAMPDIFF(MINUTE, a.time, b.time) <= 60
        AND ST_DISTANCE_SPHERE(
            POINT(a.longitude, a.latitude),
            POINT(b.longitude, b.latitude)
        ) <= 50000;
    """,

    "30. Regions with most deep-focus earthquakes (>300 km)": """
        SELECT continent, COUNT(*) AS total
        FROM earthquakes
        WHERE depth_km > 300
        GROUP BY continent
        ORDER BY total DESC;
        """

}


# ---------------- STREAMLIT UI ----------------
st.title("🌍 Earthquake Data Analysis Dashboard")
st.write("Select any problem statement (1–30) to run the corresponding SQL query.")

# ---------------- DROPDOWN ----------------
task = st.selectbox("Choose Task Number", list(queries.keys()))

# ---------------- RUN BUTTON ----------------
if st.button("Run Query"):
    query = queries[task]
    df = pd.read_sql(query,engine)

    st.subheader(f"Results for: {task}")
    st.dataframe(df, use_container_width=True)

