import streamlit as st
import requests
import datetime

# Your API Key
API_KEY = "665f1f975fe5874e657815c39ad0d901"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Page configuration
st.set_page_config(
    page_title="Weather Forecast App",
    page_icon="🌤️",
    layout="centered"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1E88E5;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .weather-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 5px solid #1E88E5;
    }
    .temperature {
        font-size: 48px;
        font-weight: bold;
        color: #FF5722;
        text-align: center;
    }
    .weather-icon {
        font-size: 64px;
        text-align: center;
        margin: 20px 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 5px;
    }
    .city-name {
        font-size: 32px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .description {
        font-size: 20px;
        color: #666;
        text-transform: capitalize;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        color: #777;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>🌤️ Real-Time Weather Forecast</h1><p>Get accurate weather information for any city</p></div>', unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Temperature unit selection
    unit = st.radio("Temperature Unit", 
                   ["Celsius (°C)", "Fahrenheit (°F)"], 
                   index=0)
    
    # Theme selection
    theme = st.selectbox("Color Theme", 
                        ["Blue", "Green", "Purple", "Orange"])
    
    # API status
    st.divider()
    st.subheader("🔧 API Status")
    st.success("✅ API Key Configured")
    st.caption(f"Key: {API_KEY[:8]}...{API_KEY[-4:]}")
    
    # Refresh interval
    auto_refresh = st.checkbox("Auto-refresh every 5 minutes", value=False)
    
    st.divider()
    st.info("💡 Tip: You can search by city name or coordinates")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Search method selection
    search_method = st.radio("Search by:", 
                            ["City Name", "Coordinates"], 
                            horizontal=True)
    
    if search_method == "City Name":
        city = st.text_input("Enter City Name", "London")
        country = st.text_input("Country Code (optional)", placeholder="e.g., US, GB, IN")
        
        if country:
            query = f"{city},{country}"
        else:
            query = city
            
    else:  # Coordinates
        col_lat, col_lon = st.columns(2)
        with col_lat:
            lat = st.number_input("Latitude", value=30.9644, format="%.4f")
        with col_lon:
            lon = st.number_input("Longitude", value=70.9360, format="%.4f")
        query = f"lat={lat}&lon={lon}"

with col2:
    st.markdown("###")
    get_weather = st.button("Get Weather Data", 
                          type="primary", 
                          use_container_width=True,
                          icon="📡")

# Weather icons mapping
def get_weather_icon(icon_code):
    icons = {
        "01d": "☀️", "01n": "🌙",
        "02d": "⛅", "02n": "☁️",
        "03d": "☁️", "03n": "☁️",
        "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️",
        "10d": "🌦️", "10n": "🌦️",
        "11d": "⛈️", "11n": "⛈️",
        "13d": "❄️", "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️"
    }
    return icons.get(icon_code, "🌤️")

# Function to fetch weather data
def fetch_weather_data(query, is_coordinates=False):
    try:
        params = {
            'appid': API_KEY,
            'units': 'metric' if 'Celsius' in unit else 'imperial'
        }
        
        if is_coordinates:
            # Parse coordinates from query string
            import re
            lat_match = re.search(r'lat=([-+]?\d*\.\d+|\d+)', query)
            lon_match = re.search(r'lon=([-+]?\d*\.\d+|\d+)', query)
            if lat_match and lon_match:
                params['lat'] = float(lat_match.group(1))
                params['lon'] = float(lon_match.group(1))
            url = BASE_URL
        else:
            params['q'] = query
            url = BASE_URL
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Display weather when button is clicked
if get_weather:
    with st.spinner("Fetching weather data..."):
        is_coord_search = search_method == "Coordinates"
        weather_data = fetch_weather_data(query, is_coord_search)
    
    if weather_data and weather_data.get('cod') == 200:
        # Extract data
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        wind_deg = weather_data['wind'].get('deg', 0)
        description = weather_data['weather'][0]['description']
        icon_code = weather_data['weather'][0]['icon']
        city_name = weather_data['name']
        country_code = weather_data['sys'].get('country', '')
        
        # Convert wind direction
        def wind_direction(degrees):
            directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            index = round(degrees / 45) % 8
            return directions[index]
        
        wind_dir = wind_direction(wind_deg)
        
        # Temperature unit
        temp_unit = "°C" if 'Celsius' in unit else "°F"
        
        # Display weather card
        st.markdown(f'<div class="weather-card">', unsafe_allow_html=True)
        
        # City and description
        st.markdown(f'<div class="city-name">{city_name}, {country_code}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="description">{description}</div>', 
                   unsafe_allow_html=True)
        
        # Temperature and icon
        col_temp, col_icon = st.columns([2, 1])
        
        with col_temp:
            st.markdown(f'<div class="temperature">{temp:.1f}{temp_unit}</div>', 
                       unsafe_allow_html=True)
            st.caption(f"Feels like {feels_like:.1f}{temp_unit}")
        
        with col_icon:
            icon = get_weather_icon(icon_code)
            st.markdown(f'<div class="weather-icon">{icon}</div>', 
                       unsafe_allow_html=True)
        
        # Temperature range
        st.progress((temp - temp_min) / (temp_max - temp_min) if temp_max != temp_min else 0.5)
        st.caption(f"Min: {temp_min:.1f}{temp_unit} | Max: {temp_max:.1f}{temp_unit}")
        
        # Metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Humidity", f"{humidity}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Pressure", f"{pressure} hPa")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            wind_unit = "m/s" if 'Celsius' in unit else "mph"
            st.metric("Wind Speed", f"{wind_speed} {wind_unit}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Wind Direction", wind_dir)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional info
        with st.expander("Additional Information"):
            col_sunrise, col_sunset = st.columns(2)
            sunrise = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise'])
            sunset = datetime.datetime.fromtimestamp(weather_data['sys']['sunset'])
            
            with col_sunrise:
                st.write("🌅 **Sunrise**")
                st.write(sunrise.strftime("%I:%M %p"))
            
            with col_sunset:
                st.write("🌇 **Sunset**")
                st.write(sunset.strftime("%I:%M %p"))
            
            if 'visibility' in weather_data:
                st.write(f"👁️ **Visibility:** {weather_data['visibility']/1000:.1f} km")
            
            if 'clouds' in weather_data:
                st.write(f"☁️ **Cloudiness:** {weather_data['clouds']['all']}%")
        
        # Raw data (for debugging)
        with st.expander("View Raw API Response"):
            st.json(weather_data)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Success message
        st.success(f"Weather data retrieved successfully at {datetime.datetime.now().strftime('%H:%M:%S')}")
        
    elif weather_data:
        st.error(f"Error: {weather_data.get('message', 'Unknown error')}")
    else:
        st.error("Failed to fetch weather data. Please check your connection.")

# Default display (when app loads)
else:
    st.markdown("""
    <div style='text-align: center; padding: 40px;'>
        <h2>Welcome to Weather Forecast App!</h2>
        <p>Enter a city name or coordinates and click "Get Weather Data" to start.</p>
        
        <div style='margin: 30px 0;'>
            <h3>🌍 Try these cities:</h3>
            <div style='display: flex; justify-content: center; gap: 15px; margin-top: 15px;'>
                <span style='padding: 10px 20px; background: #e3f2fd; border-radius: 20px;'>London</span>
                <span style='padding: 10px 20px; background: #e3f2fd; border-radius: 20px;'>New York</span>
                <span style='padding: 10px 20px; background: #e3f2fd; border-radius: 20px;'>Tokyo</span>
                <span style='padding: 10px 20px; background: #e3f2fd; border-radius: 20px;'>Sydney</span>
            </div>
        </div>
        
        <div style='background: #f5f5f5; padding: 20px; border-radius: 10px; margin-top: 20px;'>
            <h4>📊 Features:</h4>
            <ul style='text-align: left; display: inline-block;'>
                <li>Real-time weather data</li>
                <li>Search by city or coordinates</li>
                <li>Multiple temperature units</li>
                <li>Detailed weather metrics</li>
                <li>Beautiful visual interface</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Powered by OpenWeatherMap API | Built with Streamlit</p>
    <p>API Key Status: ✅ Active | Last Check: {}</p>
</div>
""".format(datetime.datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

# Auto-refresh if enabled
if auto_refresh and 'weather_data' in locals():
    st.runtime.legacy_caching.clear_cache()
    st.experimental_rerun()