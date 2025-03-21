import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚗 Car Sharing Dashboard")

# Load and prepare data
@st.cache_data
def load_data():
    trips = pd.read_csv("datasets/trips.csv")
    cars = pd.read_csv("datasets/cars.csv")
    cities = pd.read_csv("datasets/cities.csv")
    df = trips.merge(cars, left_on='car_id', right_on='id')
    df = df.merge(cities, left_on='city_id', right_on='city_id')

    # Remove extra columns if they exist
    columns_to_drop = ["id_car", "id_customer", "id_x", "id_y", "id"]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    # Add formatted columns
    df['pickup_time'] = pd.to_datetime(df['pickup_time'])
    df['dropoff_time'] = pd.to_datetime(df['dropoff_time'])
    df['pickup_date'] = df['pickup_time'].dt.date
    df['duration_min'] = (df['dropoff_time'] - df['pickup_time']).dt.total_seconds() / 60
    return df

df = load_data()

# Sidebar filter for car brand
cars_brand = st.sidebar.multiselect("Select the Car Brand", df["brand"].unique(), df["brand"].unique())
df = df[df["brand"].isin(cars_brand)]

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Trips Count", df.shape[0])
col2.metric("Unique Customers", df["customer_id"].nunique())
with col3:
    total_km = df["distance"].sum()
    st.metric("Total Distance", value=f"{total_km:.2f} km")
with col4:
    average_price = df["daily_price"].mean()
    st.metric("Avg. Revenue / Trip", value=f"{average_price:.2f} €")

# Visualizations
col1, col2, col3 = st.columns(3)

# Customers by City
with col1:
    st.subheader("Trips by City")
    city_counts = df['name'].value_counts()
    st.bar_chart(city_counts)

# Revenue by Car Model
with col2:
    st.subheader("Revenue by Car Model")
    revenue_by_model = df.groupby("model")["price"].sum()
    st.bar_chart(revenue_by_model)

# Average Trip Duration per City
with col3:
    st.subheader("Average Trip Duration per City")
    avg_duration = df.groupby("name")["duration_min"].mean()
    st.bar_chart(avg_duration)

# Revenue Over Time
df['Trips Date'] = df['pickup_date']
st.subheader("💰 Revenue Over Time")
revenue_over_time = df.groupby('Trips Date')['price'].sum()
st.area_chart(revenue_over_time)

# Trips Over Time
st.subheader("📈 Trips Over Time")
trips_over_time = df['Trips Date'].value_counts().sort_index()
st.line_chart(trips_over_time)

# Preview Data
st.subheader("🔍 Preview Trip Data")
st.dataframe(df.head())

# === OPTIONAL: Chatbot Interface ===
st.title("💬 Trip Data Chatbot")
st.write("Ask me about total revenue, number of trips, or average distance!")

# Initialize chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_query = st.chat_input("Type your question...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    response = "Sorry, I didn't understand your question."

    if "total revenue" in user_query.lower():
        revenue = df["price"].sum()
        response = f"Total revenue was **{round(revenue, 2):,} €**."
    elif "total trips" in user_query.lower():
        response = f"There were **{df.shape[0]:,} trips** recorded."
    elif "average trip distance" in user_query.lower():
        avg_dist = df["distance_km"].mean()
        response = f"The average trip distance was **{round(avg_dist, 2)} km**."

    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
