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

