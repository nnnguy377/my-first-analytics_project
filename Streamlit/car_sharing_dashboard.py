import streamlit as st
import pandas as pd

# Function to load CSV files into dataframes
@st.cache_data
def load_data():
    trips = pd.read_csv("datasets/trips.csv")
    cars = pd.read_csv("datasets/cars.csv")
    cities = pd.read_csv("datasets/cities.csv")
    return trips, cars, cities

# Load data
trips, cars, cities = load_data()

# Merge trips with cars (joining on car_id)
trips_merged = trips.merge(cars, left_on='car_id', right_on='id')

# Merge with cities for car's city (joining on city_id)
trips_merged = trips_merged.merge(cities, left_on='city_id', right_on='id')

# Clean useless columns
trips_merged = trips_merged.drop(columns=["id_car", "city_id", "id_customer", "id_x", "id_y", "id"])

# Update date format
trips_merged['pickup_time'] = pd.to_datetime(trips_merged['pickup_time'])
trips_merged['dropoff_time'] = pd.to_datetime(trips_merged['dropoff_time'])
trips_merged['pickup_date'] = trips_merged['pickup_time'].dt.date

# Sidebar filter: car brand
brands = trips_merged['brand'].unique()
selected_brands = st.sidebar.multiselect("Select the Car Brand", brands)

# Filter by selected brand(s)
if selected_brands:
    trips_merged = trips_merged[trips_merged['brand'].isin(selected_brands)]

# Compute business performance metrics
total_trips = trips_merged.shape[0]
total_distance = trips_merged['distance_km'].sum()

# Top car model by revenue
revenue_per_model = trips_merged.groupby('model')['price'].sum()
top_car = revenue_per_model.idxmax()

# Display metrics
st.title("🚗 Car Sharing Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Trips", value=total_trips)
with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)
with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

# Show preview of dataframe
st.subheader("Trips Data Preview")
st.write(trips_merged.head())

# --- Visualizations ---

# 1. Trips Over Time
st.subheader("📈 Number of Trips Over Time")
trips_by_date = trips_merged.groupby('pickup_date').size()
st.line_chart(trips_by_date)

# 2. Revenue Per Car Model
st.subheader("💰 Revenue Per Car Model")
st.bar_chart(revenue_per_model)

# 3. Average Trip Duration by City
st.subheader("⏱️ Average Trip Duration by City")
trips_merged['duration_min'] = (trips_merged['dropoff_time'] - trips_merged['pickup_time']).dt.total_seconds() / 60
avg_duration = trips_merged.groupby('name')['duration_min'].mean()
st.area_chart(avg_duration)
