import streamlit as st
import pandas as pd

# Chargement des données
@st.cache_data
def load_data():
    trips = pd.read_csv("data/trips.csv")
    cars = pd.read_csv("data/cars.csv")
    cities = pd.read_csv("data/cities.csv")
    return trips, cars, cities

# Load datasets
trips, cars, cities = load_data()

# Fusion des datasets
trips_merged = trips.merge(cars, on='car_id', how='left')
trips_merged = trips_merged.merge(cities, on='city_id', how='left')

# -------------------------------
# 🎛️ Sidebar Filter: Car Brand
# -------------------------------
unique_brands = trips_merged['brand'].dropna().unique()
selected_brands = st.sidebar.multiselect("Select the Car Brand", unique_brands)

# Filtrer le dataframe si des marques sont sélectionnées
if selected_brands:
    trips_merged = trips_merged[trips_merged['brand'].isin(selected_brands)]

# -------------------------------
# 📊 Business Performance Metrics
# -------------------------------

# Total number of trips
total_trips = len(trips_merged)

# Total distance (assuming the column is named 'distance')
total_distance = trips_merged['distance'].sum()

# Car model with the highest revenue
# Assuming there's a column called 'revenue' in the trips dataset
if not trips_merged.empty and 'revenue' in trips_merged.columns:
    revenue_by_model = trips_merged.groupby('model')['revenue'].sum()
    top_car = revenue_by_model.idxmax()
else:
    top_car = "N/A"

# -------------------------------
# 🧮 Display Metrics in Columns
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Trips", value=total_trips)

with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)

with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

st.write("Aperçu du DataFrame fusionné (trips_merged) :")
st.write(trips_merged.head())

# Assurer que la colonne date est bien convertie en datetime
trips_merged['trip_date'] = pd.to_datetime(trips_merged['trip_date'])

# Grouper par date
trips_over_time = trips_merged.groupby(trips_merged['trip_date'].dt.date).size()

st.subheader("📅 Trips Over Time")
st.line_chart(trips_over_time)

# Vérifier qu'on a une colonne revenue et model
revenue_per_model = trips_merged.groupby('model')['revenue'].sum().sort_values(ascending=False)

st.subheader("🚗 Revenue Per Car Model")
st.bar_chart(revenue_per_model)

# Vérifie que la colonne 'duration' existe (en minutes ou heures par exemple)
avg_duration_by_city = trips_merged.groupby('city_name')['duration'].mean().sort_values(ascending=False)

st.subheader("⏱️ Average Trip Duration by City")
st.area_chart(avg_duration_by_city)

revenue_by_brand = trips_merged.groupby('brand')['revenue'].sum().sort_values(ascending=False)

st.subheader("💰 Revenue by Car Brand")
st.bar_chart(revenue_by_brand)

