import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Set the title
st.title("Car MSRP Visualizer")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("CARS.csv")
    df.MSRP = df.MSRP.replace('[$,]', '', regex=True).astype('Int64')
    df.Invoice = df.Invoice.replace('[$,]', '', regex=True).astype('Int64')
    return df

df = load_data()

# Dropdown for brand selection
brands = df['Make'].unique()
selected_brand = st.selectbox("Select Car Brand", brands)

# Filter by selected brand
brand_df = df[df['Make'] == selected_brand]

# Dropdown for type selection based on brand
types = brand_df['Type'].unique()
selected_type = st.selectbox("Select Car Type", types)

# Filter by selected type
filtered_df = brand_df[brand_df['Type'] == selected_type]

# Display barplot
st.subheader(f"MSRP of {selected_brand} - {selected_type} Cars")
fig, ax = plt.subplots(figsize=(10, 5))
sb.barplot(x=filtered_df['Model'], y=filtered_df['MSRP'], ax=ax)
plt.xticks(rotation=90)
plt.tight_layout()
st.pyplot(fig)
