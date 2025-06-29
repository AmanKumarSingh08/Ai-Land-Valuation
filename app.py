import os
import pickle as pk
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get paths
MODEL_PATH = os.getenv('MODEL_PATH')
DATA_PATH = os.getenv('DATA_PATH')

# Show debug info
# st.write("🔍 Model Path:", MODEL_PATH)
# st.write("🔍 Data Path:", DATA_PATH)

# Load model
if not os.path.exists(MODEL_PATH):
    st.error(f"❌ Model file not found at {MODEL_PATH}")
    st.stop()

if not os.path.exists(DATA_PATH):
    st.error(f"❌ Data file not found at {DATA_PATH}")
    st.stop()

# Load model and data
model = pk.load(open(MODEL_PATH, 'rb'))
data = pd.read_csv(DATA_PATH)

# App UI
st.header('🏠 Bangalore House Prices Predictor')

loc = st.selectbox('Choose the Location', sorted(data['location'].unique()))
sqft = st.number_input('Enter Total Sqft Area', min_value=100.0, step=10.0)
beds = st.number_input('Enter No. of Bedrooms', min_value=1, step=1)
bath = st.number_input('Enter No. of Bathrooms', min_value=1, step=1)
balc = st.number_input('Enter No. of Balconies', min_value=0, step=1)

# Prepare input
input_df = pd.DataFrame([[loc, sqft, bath, balc, beds]],
                        columns=['location', 'total_sqft', 'bath', 'balcony', 'bedrooms'])

# Prediction
if st.button("Predict Price"):
    try:
        prediction = model.predict(input_df)
        price = round(prediction[0] * 1e5, 2)  # converting from lakhs
        st.success(f"💰 Estimated House Price: ₹ {price:,.2f}")
    except Exception as e:
        st.error(f"Prediction error: {e}")
