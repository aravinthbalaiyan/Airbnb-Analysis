# Import necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Set up page configuration
icon = Image.open("profile.png")
st.set_page_config(
    page_title="Airbnb Data Visualization | By Aravinth",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This dashboard app is created by *Aravinth*!
                    Data has been gathered from mongodb atlas"""}
)


# Create option menu in the sidebar
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Overview", "Explore"],
                           icons=["house", "graph-up-arrow", "bar-chart-line"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                          )

# Read the cleaned DataFrame from a CSV file
df = pd.read_csv('Airbnb_data.csv')

# Home Page
if selected == "Home":
    st.image("Back_you_python.png")
    col1, col2 = st.columns(2)
    col1.markdown("## Domain: Travel Industry, Property Management, and Tourism")
    col1.markdown("## Technologies used: Python, Pandas, Plotly, Streamlit, MongoDB")
    col1.markdown("## Overview: Analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")
    col2.markdown("#   ")
    col2.markdown("#   ")

# Overview Page
if selected == "Overview":
    # Raw Data Tab
    if st.button("Click to view Dataframe"):
        st.write(df)

    # Get user inputs
    country = st.sidebar.multiselect('Select a Country', sorted(df.Country.unique()), sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type', sorted(df.Property_type.unique()), sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type', sorted(df.Room_type.unique()), sorted(df.Room_type.unique()))
    price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

    # Convert the user input into a query
    query = (df['Country'].isin(country)) & (df['Property_type'].isin(prop)) & (df['Room_type'].isin(room)) & (df['Price'] >= price[0]) & (df['Price'] <= price[1])

    col1, col2 = st.columns(2)

    with col1:
        # Top 10 Property Types Bar Chart
        df1 = df[query].groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
        fig = px.bar(df1,
                     title='Top 10 Property Types',
                     x='Listings',
                     y='Property_type',
                     orientation='h',
                     color='Property_type',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        # Top 10 Hosts Bar Chart
        df2 = df[query].groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
        fig = px.bar(df2,
                     title='Top 10 Hosts with Highest number of Listings',
                     x='Listings',
                     y='Host_name',
                     orientation='h',
                     color='Host_name',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Total Listings in Each Room Types Pie Chart
        df1 = df[query].groupby(["Room_type"]).size().reset_index(name="counts")
        fig = px.pie(df1,
                     title='Total Listings in each Room_types',
                     names='Room_type',
                     values='counts',
                     color_discrete_sequence=px.colors.sequential.Rainbow)
        fig.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig, use_container_width=True)

        # Total Listings by Country Choropleth Map
        country_df = df[query].groupby(['Country'], as_index=False)['Name'].count().rename(columns={'Name': 'Total_Listings'})
        fig = px.choropleth(country_df,
                            title='Total Listings in each Country',
                            locations='Country',
                            locationmode='country names',
                            color='Total_Listings',
                            color_continuous_scale=px.colors.sequential.Plasma)
        st.plotly_chart(fig, use_container_width=True)

# Explore Page
if selected == "Explore":
    st.markdown("Explore more about the Airbnb data")

    # Get user inputs
    country = st.sidebar.multiselect('Select a Country', sorted(df.Country.unique()), sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type', sorted(df.Property_type.unique()), sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type', sorted(df.Room_type.unique()), sorted(df.Room_type.unique()))
    price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

    # Convert the user input into a query
    query = (df['Country'].isin(country)) & (df['Property_type'].isin(prop)) & (df['Room_type'].isin(room)) & (df['Price'] >= price[0]) & (df['Price'] <= price[1])

    st.markdown("Price Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Avg Price by Room Type Bar Chart
        pr_df = df[query].groupby('Room_type', as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price in each Room type')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("Availability Analysis")

        # Availability by Room Type Box Plot
        fig = px.box(data_frame=df[query],
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Avg Price in Countries Scattergeo
        country_df = df[query].groupby('Country', as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                             locations='Country',
                             color='Price',
                             hover_data=['Price'],
                             locationmode='country names',
                             size='Price',
                             title='Avg Price in each Country',
                             color_continuous_scale='agsunset')
        col2.plotly_chart(fig, use_container_width=True)

        st.markdown("#   ")
        st.markdown("#   ")

        # Avg Availability in Countries Scattergeo
        country_df = df[query].groupby('Country', as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                             locations='Country',
                             color='Availability_365',
                             hover_data=['Availability_365'],
                             locationmode='country names',
                             size='Availability_365',
                             title='Avg Availability in each Country',
                             color_continuous_scale='agsunset')
        st.plotly_chart(fig, use_container_width=True)
