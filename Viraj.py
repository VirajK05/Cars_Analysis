import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Car MSRP Explorer", layout="wide")

# Title and description
st.title("🚗 Car MSRP Explorer")
st.markdown("""
Welcome to the **Car MSRP Explorer**!  
This app helps you explore different car brands and models along with their **Manufacturer's Suggested Retail Price (MSRP)**.

🔍 Select a car brand and type from the dropdowns below to visualize the MSRP of available models.
""")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("CARS.csv")
    df.MSRP = df.MSRP.replace('[$,]', '', regex=True).astype('Int64')
    df.Invoice = df.Invoice.replace('[$,]', '', regex=True).astype('Int64')
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔧 Filter Options")

# Car brand selection
brands = sorted(df['Make'].unique())
selected_brand = st.sidebar.selectbox("Select Car Brand", brands)

# Filter dataframe based on brand
brand_df = df[df['Make'] == selected_brand]

# Car type selection
types = sorted(brand_df['Type'].unique())
selected_type = st.sidebar.selectbox("Select Car Type", types)

# Filter dataframe based on car type
filtered_df = brand_df[brand_df['Type'] == selected_type]

# If filtered data is empty
if filtered_df.empty:
    st.warning("No cars found for the selected brand and type.")
else:
    st.markdown(f"### 📊 MSRP for {selected_brand} - {selected_type} Models")

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    plot = sns.barplot(x=filtered_df['Model'], y=filtered_df['MSRP'], palette="viridis", ax=ax)
    ax.set_title(f"MSRP Comparison of {selected_brand} - {selected_type} Cars", fontsize=14, weight='bold')
    ax.set_ylabel("MSRP (USD)", fontsize=12, weight='bold')
    ax.set_xlabel("Model", fontsize=12)
    plt.xticks(rotation=90)

    # Annotate MSRP on bars
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"${height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=9, color='black', weight='bold')

    st.pyplot(fig)

    # Optional data table
    with st.expander("📄 View Raw Data Table"):
        st.dataframe(filtered_df[['Make', 'Model', 'Type', 'MSRP', 'Invoice']].sort_values(by="MSRP", ascending=False))
