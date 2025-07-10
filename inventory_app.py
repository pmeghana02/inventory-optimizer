import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
 
st.title("🛒 Inventory Optimization App")
 
uploaded_file = st.file_uploader("Upload your Supply Chain CSV file", type=["csv"])
 
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")
    st.write(df.head())
 
    if all(col in df.columns for col in ['price', 'stock levels', 'availability', 'number of products sold']):
        st.success("✅ Required columns found. Running prediction...")
 
        X = df[['price', 'stock levels', 'availability']]
        y = df['number of products sold']
 
        model = LinearRegression()
        model.fit(X, y)
 
        df['predicted_sales'] = model.predict(X)
        df['optimized_stock'] = df['predicted_sales'] * 1.10  # Add 10% buffer
 
        st.subheader("📈 Predicted Sales & Optimized Stock")
        st.write(df[['predicted_sales', 'optimized_stock']])
 
        st.download_button("📥 Download Optimized Plan", df.to_csv(index=False), file_name="optimized_plan.csv")
 
    else:
        st.error("❌ Required columns not found in dataset.")
