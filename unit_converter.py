import streamlit as st

conversion_factors = {
    '📏 Length': {
        'meter': 1,
        'kilometer': 0.001,
        'centimeter': 100,
        'millimeter': 1000,
        'mile': 0.000621371,
        'yard': 1.09361,
        'foot': 3.28084,
        'inch': 39.3701
    },
    '⚖️ Weight': {
        'kilogram': 1,
        'gram': 1000,
        'milligram': 1000000,
        'pound': 2.20462,
        'ounce': 35.274
    },
    '🌡️ Temperature': {
        'celsius': 1,
        'fahrenheit': 33.8,
        'kelvin': 274.15
    },
    '🧪 Volume': {
        'liter': 1,
        'milliliter': 1000,
        'cubic meter': 0.001,
        'cubic foot': 0.0353147,
        'gallon': 0.264172,
        'quart': 1.05669,
        'pint': 2.11338
    },
    '⏳ Time': {
        'second': 1,
        'minute': 1/60,
        'hour': 1/3600,
        'day': 1/86400,
        'week': 1/604800
    }
}

def convert_units(value, from_unit, to_unit, category):
    base_category = category.split(' ')[-1]
    if base_category == 'Temperature':
        if from_unit == 'celsius':
            if to_unit == 'fahrenheit':
                return value * 9/5 + 32
            elif to_unit == 'kelvin':
                return value + 273.15
        elif from_unit == 'fahrenheit':
            if to_unit == 'celsius':
                return (value - 32) * 5/9
            elif to_unit == 'kelvin':
                return (value - 32) * 5/9 + 273.15
        elif from_unit == 'kelvin':
            if to_unit == 'celsius':
                return value - 273.15
            elif to_unit == 'fahrenheit':
                return (value - 273.15) * 9/5 + 32
        return value
    else:
        base_value = value / conversion_factors[category][from_unit]
        return base_value * conversion_factors[category][to_unit]


st.set_page_config(page_title="Ultimate Unit Converter", page_icon="📐", layout="wide")

# Dark mode toggle in session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode



dark_mode_css = """
<style>
    :root {
        --primary-bg: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        --card-bg: #2d3436;
        --text-color: #dfe6e9;
        --header-bg: #2d3436;
        --result-bg: linear-gradient(145deg, #34495e 0%, #2c3e50 100%);
    }
    
    .light-mode {
        --primary-bg: linear-gradient(135deg, #E3F2FD 0%, #F5F5F5 100%);
        --card-bg: #FFFFFF;
        --text-color: #2F4F4F;
        --header-bg: #FFFFFF;
        --result-bg: linear-gradient(145deg, #B3E5FC 0%, #E1F5FE 100%);
    }

    body {
        background: var(--primary-bg);
        color: var(--text-color);
        transition: all 0.3s ease;
    }

    .header {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background-color: var(--header-bg);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: var(--text-color);
    }

    .category-box {
        background-color: var(--card-bg);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        color: var(--text-color);
    }

    .result-box {
        background: var(--result-bg);
        padding: 25px;
        border-radius: 15px;
        margin-top: 25px;
        box-shadow: 0 3px 5px rgba(0,0,0,0.1);
        color: var(--text-color);
    }

    .stSelectbox, .stNumberInput {
        border-radius: 10px !important;
        border: 1px solid #BBDEFB !important;
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }
</style>
"""


st.markdown(dark_mode_css, unsafe_allow_html=True)
st.markdown(f'<body class="{"light-mode" if not st.session_state.dark_mode else "dark-mode"}">', unsafe_allow_html=True)



st.markdown('<div class="header">🚀 Ultimate Unit Converter 🌈</div>', unsafe_allow_html=True)


col1, col2 = st.columns([1, 1])

with col1:
    category = st.selectbox(
        "Select Category",
        list(conversion_factors.keys()),
        index=0,
        key='category'
    )

with col2:
    category_name = category.split(' ')[-1]
    st.markdown(f"""
    <div style="background:{'#404040' if st.session_state.dark_mode else '#F0F4C3'};padding:15px;border-radius:10px;">
        <h4 style="color:{'#bdc3c7' if st.session_state.dark_mode else '#827717'};margin:0;">ℹ️ {category_name} Units</h4>
        <p style="color:{'#95a5a6' if st.session_state.dark_mode else '#9E9D24'};margin:5px 0 0 0;">
            {f"Standard {category_name.lower()} measurement units" if category_name != 'Temperature' else "Temperature conversion between different scales"}
        </p>
    </div>
    """, unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="category-box">', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        from_unit = st.selectbox(
            "From Unit",
            list(conversion_factors[category].keys()),
            key='from_unit'
        )

    with col_right:
        to_unit = st.selectbox(
            "To Unit",
            list(conversion_factors[category].keys()),
            key='to_unit'
        )

    value = st.number_input(
        "Enter Value", 
        min_value=0.0, 
        value=1.0,
        step=0.1, 
        key='conversion_value'
    )

    try:
        result = convert_units(value, from_unit, to_unit, category)
        formatted_result = f"{result:.6f}".rstrip('0').rstrip('.') if '.' in f"{result:.6f}" else f"{result:.6f}"
        
        st.markdown(f"""
        <div class="result-box">
            <h3 style='margin:0;'>🎯 Conversion Result</h3>
            <p style='font-size: 28px; font-weight: bold; margin:10px 0;'>
                {value} {from_unit} = 
            </p>
            <p style='font-size: 36px; font-weight: bold; margin:0;'>
                {formatted_result} {to_unit}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error in conversion: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center;'>🌟 Made by ❤️ Nimra Akram using Streamlit 🌟</div>", unsafe_allow_html=True)
