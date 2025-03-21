import streamlit as st
import pandas as pd

# Function to load CSV files into dataframes
@st.cache_data
def load_data():
trips = pd.read_csv("data/trips.csv")
cars = pd.read_csv("data/cars.csv")
cities = pd.read_csv("data/cities.csv")
return trips, cars, cities

trips_merged = trips.merge(cars, on='car_id', how='left')
trips_merged = trips_merged.merge(cities, on='city_id', how='left')

print(trips_merged.head())
print(trips_merged.columns)
print(trips_merged.shape)