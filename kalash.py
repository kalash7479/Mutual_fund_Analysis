import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="Mutual Fund Explorer", layout="wide")

# Title
st.title("📊 Mutual Funds India - 1 Year Returns Analysis")

# Load Data
df = pd.read_csv('../kalas/Downloads/mutual_funds_india.csv')
df.columns = df.columns.str.replace(" ", "")  # Remove spaces from column names

# Category Selection
categories = df['category'].unique()
selected_category = st.selectbox("Select a Fund Category", sorted(categories))

# Filter by category
filtered_df = df[df['category'] == selected_category]

# AMC Selection
amcs = filtered_df['AMC_name'].unique()
selected_amc = st.selectbox("Select an AMC", sorted(amcs))

# Filter by AMC
final_df = filtered_df[filtered_df['AMC_name'] == selected_amc]

# Display filtered data
st.subheader("Filtered Mutual Funds")
st.dataframe(final_df[['MutualFundName', 'return_1yr']].reset_index(drop=True))

# Bar Plot
st.subheader("📈 1-Year Returns Bar Plot")
fig, ax = plt.subplots(figsize=(12, 6))
sb.barplot(x=final_df['MutualFundName'], y=final_df['return_1yr'], palette='ocean', ax=ax)
plt.xticks(rotation=90)
plt.xlabel("Mutual Fund Name")
plt.ylabel("1-Year Return (%)")
plt.title(f"{selected_amc} - {selected_category} Returns")
st.pyplot(fig)
