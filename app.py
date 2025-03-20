import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Visualize CSV Data with Streamlit ")

df = pd.read_csv("datasets/trips_data_1000.csv")
print(df.describe())

cars_brand = st.sidebar.multiselect("Select the car brand", df["car_brand"].unique(),  df["car_brand"].unique())
df = df[df["car_brand"].isin(cars_brand)]

col1, col2, col3, col4  = st.columns(4)

col1.metric("Car Models in Use", df.shape[0])
col2.metric("Unique Customers",  df["customer_email"].nunique())
with col3:
    total_distance = df['distance'].sum() / 1000
    st.metric("Total Distance", value=f"{total_distance:.2f} K")
with col4:
    average_revenue = df['revenue'].mean()
    st.metric("Average Revenue Per Trip", value=f"{average_revenue:.2f} €")

col1, col2, col3 = st.columns(3)
# Chart 1: Bar chart of customers by country
with col1:
    st.subheader("Customers by City")
    country_counts = df['customer_city'].value_counts()
    st.bar_chart(country_counts)

# Chart 2 : Revenue by Car Model
with col2:
    st.subheader("Revenue by Car Model")
    revenue_by_car = df.groupby('car_model')['revenue'].sum()
    st.bar_chart(revenue_by_car)
# Chart 3 : Average Trip distance per city
with col3:
    st.subheader("Average Trip Distance per city")
    avg_distance_by_city = df.groupby('customer_city')['distance'].mean()
    st.bar_chart(avg_distance_by_city)
# Convert the pickup time to a date type column 
df['Trips Date'] = pd.to_datetime(df['pickup_time']).dt.date

# Chart 3: Revenue over time 
st.subheader("Revenue Over Time")
revenue_over_time = df.groupby('Trips Date')['revenue'].sum()
st.area_chart(revenue_over_time)

# Chart 4: Line chart of Trips over time
st.subheader("Trips Over Time")
Trips_Count = df["Trips Date"].value_counts()
st.line_chart(Trips_Count)

st.write(" Preview Uploaded data")
st.dataframe(df.head())

# Load Data
df = pd.read_csv("datasets/trips_data_1000.csv")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chatbot UI
st.title("Trip Data Chatbot")
st.write("Ask me about trips, revenue, or average trip distance! (e.g., 'What is the total revenue')")

# User Input
user_query = st.chat_input("Type your question...")

if user_query:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Default response
    response = "Sorry, I didn't understand your question."

    # Check for total revenue queries
    if "total revenue" in user_query.lower():
        total_revenue = df["revenue"].sum()
        response = f"Total revenue was **${round(total_revenue, 2):,}**."

    # Check for total trips queries
    elif "total trips" in user_query.lower():
        total_trips = len(df)
        response = f"There were **{total_trips:,} trips** recorded in the dataset."

    # Check for average distance queries
    elif "average trip distance" in user_query.lower():
        avg_distance = df['distance'].mean()
        response = f"The average trip distance was **{round(avg_distance, 2)} km**."

    # Store and display chatbot response
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
