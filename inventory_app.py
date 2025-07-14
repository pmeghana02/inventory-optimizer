import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
 
# Load the data
df = pd.read_csv("supply_chain_data.csv")
 
# Drop duplicates and handle missing values
df.drop_duplicates(inplace=True)
df.dropna(subset=['Price', 'Lead times', 'Number of products sold', 'Revenue generated', 'Stock levels', 'Order quantities'], inplace=True)
 
# Select features and target
features = ['Price', 'Lead times', 'Number of products sold', 'Revenue generated', 'Stock levels']
target = 'Order quantities'
 
X = df[features]
y = df[target]
 
# Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor()
model.fit(X_train, y_train)
 
# Make predictions for full dataset
df['predicted_sales'] = model.predict(X)
 
# Calculate safety stock and reorder point per row
Z = 1.65  # 95% service level
df['daily_demand'] = df['Number of products sold'] / 30
df['safety_stock'] = Z * df['daily_demand'].std() * np.sqrt(df['Lead times'])
df['reorder_point'] = (df['daily_demand'] * df['Lead times']) + df['safety_stock']
df['optimized_stock'] = df['predicted_sales'] * 1.10  # Add 10% buffer
 
# Streamlit UI
st.title("📦 Inventory Forecast Dashboard")

 
# SKU Selector
sku_list = df['SKU'].unique()
selected_sku = st.selectbox("Select SKU", sku_list)
 
# Display metrics for selected SKU
product_row = df[df['SKU'] == selected_sku].iloc[0]
st.write(product_row)

st.markdown("### 🔍 Product Inventory Insights")
 
st.write(f"**Predicted Sales:** {round(product_row['predicted_sales'])}")
st.write(f"**Safety Stock:** {round(product_row['safety_stock'])}")
st.write(f"**Reorder Point:** {round(product_row['reorder_point'])}")
st.write(f"**Optimized Stock (10% buffer):** {round(product_row['optimized_stock'])}")
