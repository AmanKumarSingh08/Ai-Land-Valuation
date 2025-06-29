import os
import pickle as pk
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read paths from .env
MODEL_PATH = os.getenv('MODEL_PATH')
DATA_PATH = os.getenv('DATA_PATH')

# Validate MODEL_PATH
if not MODEL_PATH:
    st.error("❌ MODEL_PATH is not set in environment variables.")
    st.stop()
if not os.path.exists(MODEL_PATH):
    st.error(f"❌ Model file not found at: {MODEL_PATH}")
    st.info("Please check your `.env` file or upload the model file to the specified path.")
    st.stop()

# Validate DATA_PATH
if not DATA_PATH:
    st.error("❌ DATA_PATH is not set in environment variables.")
    st.stop()
if not os.path.exists(DATA_PATH):
    st.error(f"❌ Data file not found at: {DATA_PATH}")
    st.info("Please check your `.env` file or upload the data file to the specified path.")
    st.stop()

# Load model
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pk.load(f)
except Exception as e:
    st.error(f"❌ Could not load model: {e}")
    st.stop()

# Load data
try:
    data = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error(f"❌ Could not load data: {e}")
    st.stop()

# Streamlit App
st.header('🏠 Bangalore House Prices Predictor')

# UI Inputs
loc = st.selectbox('📍 Choose Location', sorted(data['location'].dropna().unique()))
sqft = st.number_input('📏 Enter Total Sqft Area', min_value=100.0, step=10.0)
beds = st.number_input('🛏️ Enter No. of Bedrooms', min_value=1, step=1)
bath = st.number_input('🛁 Enter No. of Bathrooms', min_value=1, step=1)
balc = st.number_input('🚪 Enter No. of Balconies', min_value=0, step=1)

# Prepare input for prediction
input_df = pd.DataFrame([[loc, sqft, bath, balc, beds]],
                        columns=['location', 'total_sqft', 'bath', 'balcony', 'bedrooms'])

# Make prediction
if st.button("🔮 Predict Price"):
    try:
        prediction = model.predict(input_df)
        price = round(prediction[0] * 1e5, 2)  # Convert lakhs to rupees
        st.success(f"💰 Estimated House Price: ₹ {price:,.2f}")
    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
