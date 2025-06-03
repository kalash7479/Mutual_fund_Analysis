import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mutual Fund Explorer", layout="wide")

st.title("📊 Mutual Funds India - 1 Year Returns Explorer")

# Upload CSV file
uploaded_file = st.file_uploader("📂 Upload your `mutual_funds_india.csv` file", type=["csv"])

if uploaded_file is not None:
    # Read file
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.replace(" ", "")  # Clean column names

    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filter Options")

        # Category dropdown
        categories = sorted(df['category'].dropna().unique())
        selected_category = st.selectbox("Select Category", categories)

        # Filter by category
        filtered_by_category = df[df['category'] == selected_category]

        # AMC dropdown
        amcs = sorted(filtered_by_category['AMC_name'].dropna().unique())
        selected_amc = st.selectbox("Select AMC", amcs)

        # Filter by AMC
        filtered_data = filtered_by_category[filtered_by_category['AMC_name'] == selected_amc]

        # Optional search by mutual fund name
        mf_search = st.text_input("🔎 Search Mutual Fund Name (optional)").strip().lower()
        if mf_search:
            filtered_data = filtered_data[filtered_data['MutualFundName'].str.lower().str.contains(mf_search)]

        # Color palette selector
        palette_option = st.selectbox("🎨 Select Bar Chart Color Palette", [
            'viridis', 'deep', 'muted', 'pastel', 'dark', 'colorblind', 'ocean', 'rocket', 'mako'
        ])

        # Toggle raw data
        show_data = st.checkbox("📄 Show Raw Filtered Data")

    st.markdown(f"### Showing Results for **{selected_amc}** in **{selected_category}**")

    if filtered_data.empty:
        st.warning("No mutual funds found with the selected filters or search term.")
    else:
        # Show data table
        if show_data:
            st.dataframe(filtered_data[['MutualFundName', 'return_1yr']].reset_index(drop=True))

        # Bar plot
        st.subheader("📈 1-Year Returns")
        fig, ax = plt.subplots(figsize=(12, 6))
        sb.barplot(
            x=filtered_data['MutualFundName'],
            y=filtered_data['return_1yr'],
            palette=palette_option,
            ax=ax
        )
        plt.xticks(rotation=90)
        plt.xlabel("Mutual Fund")
        plt.ylabel("1-Year Return (%)")
        plt.title(f"Return Comparison: {selected_amc}")
        st.pyplot(fig)
else:
    st.info("👈 Please upload your CSV file from the sidebar to begin.")
