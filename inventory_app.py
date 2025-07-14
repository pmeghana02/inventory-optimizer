import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
 
st.title("Supply Chain Inventory Optimizer")
 
uploaded_file = st.file_uploader("Upload your Supply Chain CSV file", type="csv")
 
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Normalize column names to lowercase
    df.columns = df.columns.str.lower()
 
    st.subheader("Preview of Uploaded Data")
    st.write(df.head())
 
    required_columns = ['Price', 'Stock levels', 'Number of products sold']
 
    if all(col in df.columns for col in required_columns):
        X = df[['Price', 'Stock levels']]
        y = df['Number of products sold']
 
        # Build and train the model
        model = LinearRegression()
        model.fit(X, y)
 
        # Predict
        df['predicted_sales'] = model.predict(X)
 
        st.subheader("Predicted Sales")
        st.write(df[['price', 'availability', 'number of products sold', 'predicted_sales']])
    else:
        st.error("❌ Required columns not found in dataset. Please make sure your CSV contains: Price, Availability, and Number of products sold."
