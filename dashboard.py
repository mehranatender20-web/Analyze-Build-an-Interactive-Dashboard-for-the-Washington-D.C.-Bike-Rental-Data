import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go



st.set_page_config(
    page_title="Assignment Dashboard",
    layout="wide"
)

st.title("Data Analysis And Visualization Dashboard")
st.write("Dashboard for the Washington D.C. Bike Rental Data")
   

st.set_page_config(page_title="Bike Sharing Demand Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv('train.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    
   
    df['hour'] = df['datetime'].dt.hour
    df['month'] = df['datetime'].dt.month_name()
    df['year'] = df['datetime'].dt.year
    df['day_type'] = df['workingday'].map({1: 'Working Day', 0: 'Weekend/Holiday'})
    
    
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {1: "Clear", 2: "Mist/Cloudy", 3: "Light Rain/Snow", 4: "Heavy Rain/Ice"}
    df['season'] = df['season'].map(season_map)
    df['weather'] = df['weather'].map(weather_map)
    
    return df

df = load_data()


st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect("Select Year", options=df['year'].unique(), default=df['year'].unique())
selected_season = st.sidebar.multiselect("Select Season", options=df['season'].unique(), default=df['season'].unique())

filtered_df = df[(df['year'].isin(selected_year)) & (df['season'].isin(selected_season))]


st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Insights into rental patterns based on time, user type, and weather.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Rentals", f"{filtered_df['count'].sum():,}")
kpi2.metric("Avg Temp", f"{filtered_df['temp'].mean():.1f}°C")
kpi3.metric("Registered Users", f"{filtered_df['registered'].sum():,}")
kpi4.metric("Casual Users", f"{filtered_df['casual'].sum():,}")

st.divider()


col1, col2 = st.columns(2)

with col1:
    st.subheader("Hourly Rental Patterns")
    hourly_trend = filtered_df.groupby(['hour', 'day_type'])['count'].mean().reset_index()
    fig_hour = px.line(hourly_trend, x='hour', y='count', color='day_type', 
                       title="Average Hourly Rentals", markers=True)
    st.plotly_chart(fig_hour, use_container_width=True)

with col2:
    st.subheader("Weather & Season Impact")
    weather_impact = filtered_df.groupby('weather')['count'].mean().sort_values(ascending=False).reset_index()
    fig_weather = px.bar(weather_impact, x='weather', y='count', color='weather',
                         title="Average Rentals by Weather Condition")
    st.plotly_chart(fig_weather, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("User Type Distribution")
    user_totals = pd.DataFrame({
        'User Type': ['Registered', 'Casual'],
        'Total': [filtered_df['registered'].sum(), filtered_df['casual'].sum()]
    })
    fig_pie = px.pie(user_totals, values='Total', names='User Type', hole=0.4,
                     color_discrete_sequence=['#1f77b4', '#ff7f0e'])
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.subheader("Temperature vs Demand")
    fig_scatter = px.scatter(filtered_df.sample(1000), x='temp', y='count', color='season',
                             opacity=0.5, title="Correlation: Temp vs Count (Sampled)")
    st.plotly_chart(fig_scatter, use_container_width=True)

if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df.head(100))




