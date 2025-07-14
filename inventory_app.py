import streamlit as st
import pandas as pd
 
st.title("Supply Chain Inventory Optimizer")
 
uploaded_file = st.file_uploader("Upload your Supply Chain CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    required_columns = ['price', 'stock levels', 'number of products sold']
    if all(col in df.columns for col in required_columns):
        st.subheader("Preview of Uploaded Data")
        st.write(df.head())
 
        if 'predicted_sales' in df.columns and 'optimized_stock' in df.columns:
            st.subheader("Predicted Sales vs Optimized Stock")
            st.line_chart(df[['predicted_sales', 'optimized_stock']])
        else:
            st.warning("Predicted columns not found in uploaded file.")
    else:
        st.error("Required columns not found. Please ensure your CSV contains 'price', 'stock levels', and 'number of products sold'")
