import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# App title and configuration
st.set_page_config(
    page_title="Simple Weather App",
    page_icon="🌤️",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .weather-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .temp-big {
        font-size: 3rem;
        font-weight: bold;
        color: #FF5722;
    }
    .weather-icon {
        font-size: 4rem;
        text-align: center;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #666;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🌤️ Simple Weather App</h1>', unsafe_allow_html=True)

# Sidebar for API key input
with st.sidebar:
    st.header("⚙Configuration")
    
    # Option to use demo mode or real API
    demo_mode = st.toggle("Use Demo Mode", value=True, 
                         help="Use sample data if you don't have an API key")
    
    if not demo_mode:
        api_key = st.text_input("Enter OpenWeatherMap API Key", type="password",
                               help="Get free API key from https://openweathermap.org/api")
        
        if not api_key:
            # Try to get from environment variable
            api_key = os.getenv("OPENWEATHER_API_KEY", "")
        
        if api_key:
            st.success("✅ API key loaded")
        else:
            st.warning("⚠️ Please enter your API key")
    else:
        api_key = "demo"
        st.info("Demo mode enabled - Using sample data")
    
    st.divider()
    st.markdown("### How to get API key:")
    st.markdown("""
    1. Go to [OpenWeatherMap](https://openweathermap.org/api)
    2. Sign up for free account
    3. Get your API key from dashboard
    4. Enter it in the field above
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # City input
    default_city = st.session_state.get('last_city', 'London')
    city = st.text_input("Enter City Name", value=default_city)
    
    # Country code (optional)
    country = st.text_input("Country Code (optional, e.g., US, UK)", 
                           placeholder="Leave empty for default")

with col2:
    # Unit selection
    unit = st.selectbox("Temperature Unit", 
                       ["Celsius", "Fahrenheit"])
    
    # Button to get weather
    get_weather = st.button("Get Weather", type="primary", use_container_width=True)

# Function to get weather icon
def get_weather_icon(condition):
    icons = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '❄️',
        'Mist': '🌫️',
        'Fog': '🌁',
        'Haze': '😶‍🌫️'
    }
    return icons.get(condition, '🌤️')

# Function to get weather data
def get_weather_data(city_name, country_code, api_key, units='metric'):
    if api_key == "demo":
        # Return demo data
        demo_data = {
            "weather": [{"main": "Clear", "description": "clear sky", "icon": "01d"}],
            "main": {"temp": 25, "feels_like": 26, "temp_min": 23, "temp_max": 27, "humidity": 65, "pressure": 1013},
            "wind": {"speed": 3.6, "deg": 200},
            "name": city_name,
            "sys": {"country": country_code if country_code else "GB"}
        }
        return demo_data
    
    # Base URL for OpenWeatherMap API
    base_url = "https://api.openweathermap.org/data/2.5/weather?lat=30.9644&lon=70.9360&appid=665f1f975fe5874e657815c39ad0d901"
    
    # Prepare query parameters
    params = {
        'q': f"{city_name},{country_code}" if country_code else city_name,
        'appid': api_key,
        'units': 'metric' if units == 'Celsius' else 'imperial'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        if response.status_code == 401:
            st.error("Invalid API key. Please check your API key.")
        elif response.status_code == 404:
            st.error("City not found. Please check the city name.")
        return None

# When button is clicked
if get_weather and city:
    # Store last city in session state
    st.session_state['last_city'] = city
    
    # Show loading spinner
    with st.spinner(f"Getting weather for {city}..."):
        weather_data = get_weather_data(city, country, api_key, unit)
    
    if weather_data:
        # Check if API returned an error
        if 'cod' in weather_data and weather_data['cod'] != 200:
            st.error(f"Error: {weather_data.get('message', 'Unknown error')}")
        else:
            # Display weather information
            temp_unit = "°C" if unit == "Celsius" else "°F"
            wind_unit = "m/s" if unit == "Celsius" else "mph"
            
            st.markdown(f'<div class="weather-card">', unsafe_allow_html=True)
            
            # City and country
            country_code = weather_data['sys'].get('country', '')
            st.subheader(f"{weather_data['name']}, {country_code}")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                # Weather icon
                weather_main = weather_data['weather'][0]['main']
                weather_icon = get_weather_icon(weather_main)
                st.markdown(f'<div class="weather-icon">{weather_icon}</div>', unsafe_allow_html=True)
            
            with col2:
                # Temperature
                temp = weather_data['main']['temp']
                st.markdown(f'<div class="temp-big">{temp:.1f}{temp_unit}</div>', unsafe_allow_html=True)
                
                # Weather description
                weather_desc = weather_data['weather'][0]['description'].title()
                st.markdown(f"**{weather_desc}**")
            
            with col3:
                # Additional info
                feels_like = weather_data['main']['feels_like']
                st.metric("Feels Like", f"{feels_like:.1f}{temp_unit}")
            
            # More weather details in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                min_temp = weather_data['main']['temp_min']
                st.metric("Min Temp", f"{min_temp:.1f}{temp_unit}")
            
            with col2:
                max_temp = weather_data['main']['temp_max']
                st.metric("Max Temp", f"{max_temp:.1f}{temp_unit}")
            
            with col3:
                humidity = weather_data['main']['humidity']
                st.metric("Humidity", f"{humidity}%")
            
            with col4:
                wind_speed = weather_data['wind']['speed']
                st.metric("Wind Speed", f"{wind_speed} {wind_unit}")
            
            # Pressure
            pressure = weather_data['main']['pressure']
            st.metric("Pressure", f"{pressure} hPa")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display raw JSON data in expander (for debugging)
            with st.expander("View Raw Data"):
                st.json(weather_data)
    else:
        if api_key == "demo":
            st.info("Showing demo data for London")
            # Show demo data
            weather_data = {
                "weather": [{"main": "Clear", "description": "clear sky", "icon": "01d"}],
                "main": {"temp": 25, "feels_like": 26, "temp_min": 23, "temp_max": 27, "humidity": 65, "pressure": 1013},
                "wind": {"speed": 3.6, "deg": 200},
                "name": "London",
                "sys": {"country": "GB"}
            }
            
            temp_unit = "°C" if unit == "Celsius" else "°F"
            wind_unit = "m/s" if unit == "Celsius" else "mph"
            
            st.markdown(f'<div class="weather-card">', unsafe_allow_html=True)
            st.subheader(f"London, GB (Demo Data)")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f'<div class="weather-icon">☀️</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="temp-big">25{temp_unit}</div>', unsafe_allow_html=True)
                st.markdown(f"**Clear Sky**")
            
            st.info("This is demo data. Enter your API key in the sidebar to get real weather data.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Unable to fetch weather data. Please check your inputs.")
elif get_weather and not city:
    st.warning("Please enter a city name")

# Footer
st.markdown("---")
st.markdown('<div class="footer">Simple Weather App | Made with Streamlit | Uses OpenWeatherMap API</div>', unsafe_allow_html=True)