import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv("your_dataset.csv")  # Replace with your actual file name
df.columns = df.columns.str.replace(" ", "")

# Title
st.title("Mutual Fund Returns Viewer")

# Category selection
categories = df['category'].unique()
selected_category = st.selectbox("Select Category", categories)

# Filter by category
filtered_df = df[df['category'] == selected_category]

# AMC selection
amc_names = filtered_df['AMC_name'].unique()
selected_amc = st.selectbox("Select AMC Name", amc_names)

# Filter by AMC
final_df = filtered_df[filtered_df['AMC_name'] == selected_amc]

# Show mutual funds list
st.subheader("Mutual Funds in Selected Category & AMC")
st.write(final_df[['MutualFundName', 'return_1yr']])

# Plotting
st.subheader("1-Year Returns")
fig, ax = plt.subplots(figsize=(12, 6))
sb.barplot(x=final_df['MutualFundName'], y=final_df['return_1yr'], palette='ocean', ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)
