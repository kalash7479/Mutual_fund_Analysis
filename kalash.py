import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mutual Fund Explorer", layout="wide")

st.title("📊 Mutual Funds India - 1 Year Returns Analysis")

# File uploader must be used first
uploaded_file = st.file_uploader("📂 Upload your mutual_funds_india.csv file", type=["csv"])

# ✅ Do NOT try to read file outside this block!
if uploaded_file is not None:
    # Read uploaded file
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.replace(" ", "")  # Remove spaces from column names

    # Dropdown for Category
    categories = df['category'].dropna().unique()
    selected_category = st.selectbox("Select a Fund Category", sorted(categories))

    # Filter by category
    filtered_df = df[df['category'] == selected_category]

    # Dropdown for AMC
    amcs = filtered_df['AMC_name'].dropna().unique()
    selected_amc = st.selectbox("Select an AMC", sorted(amcs))

    # Filter by AMC
    final_df = filtered_df[filtered_df['AMC_name'] == selected_amc]

    # Display Table
    st.subheader("📋 Filtered Mutual Funds")
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

else:
    st.warning("⚠️ Please upload a CSV file to proceed.")
