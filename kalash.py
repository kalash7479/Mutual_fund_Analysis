import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from io import StringIO

# ----------------------
# Page Configuration
# ----------------------
st.set_page_config(page_title="Mutual Fund Explorer", layout="wide")

st.title("📊 Mutual Funds India – Advanced Explorer")
st.caption("Analyze, compare, and export mutual fund performance with interactive insights")

# ----------------------
# Helper Functions
# ----------------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.replace(" ", "")
    return df

# ----------------------
# File Upload
# ----------------------
uploaded_file = st.file_uploader(
    "📂 Upload your `mutual_funds_india.csv` file",
    type=["csv"]
)

if uploaded_file is None:
    st.info("👈 Upload a CSV file to start exploring mutual fund data.")
    st.stop()

# Load data
try:
    df = load_data(uploaded_file)
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# ----------------------
# Sidebar Filters
# ----------------------
with st.sidebar:
    st.header("🔍 Filters & Controls")

    # Category filter
    categories = sorted(df['category'].dropna().unique())
    selected_category = st.selectbox("📌 Select Category", categories)
    df_cat = df[df['category'] == selected_category]

    # AMC filter
    amcs = sorted(df_cat['AMC_name'].dropna().unique())
    selected_amc = st.selectbox("🏦 Select AMC", amcs)
    df_amc = df_cat[df_cat['AMC_name'] == selected_amc]

    # Search fund name
    search_text = st.text_input("🔎 Search Mutual Fund Name").strip().lower()
    if search_text:
        df_amc = df_amc[df_amc['MutualFundName'].str.lower().str.contains(search_text)]

    # Return range filter
    min_ret, max_ret = float(df_amc['return_1yr'].min()), float(df_amc['return_1yr'].max())
    return_range = st.slider(
        "📉 Filter by 1-Year Return (%)",
        min_value=min_ret,
        max_value=max_ret,
        value=(min_ret, max_ret)
    )
    df_amc = df_amc[
        (df_amc['return_1yr'] >= return_range[0]) &
        (df_amc['return_1yr'] <= return_range[1])
    ]

    # Sorting
    sort_option = st.selectbox(
        "↕️ Sort By",
        ["Return: High to Low", "Return: Low to High", "Fund Name A–Z"]
    )

    # Chart options
    palette_option = st.selectbox(
        "🎨 Bar Chart Palette",
        ['viridis', 'deep', 'muted', 'pastel', 'dark', 'colorblind', 'ocean', 'rocket', 'mako']
    )

    show_data = st.checkbox("📄 Show Data Table", value=True)

# ----------------------
# Sorting Logic
# ----------------------
if sort_option == "Return: High to Low":
    df_amc = df_amc.sort_values(by='return_1yr', ascending=False)
elif sort_option == "Return: Low to High":
    df_amc = df_amc.sort_values(by='return_1yr', ascending=True)
else:
    df_amc = df_amc.sort_values(by='MutualFundName')

# ----------------------
# Main Content
# ----------------------
st.markdown(f"## 📌 {selected_amc} | {selected_category}")

if df_amc.empty:
    st.warning("No mutual funds match the selected filters.")
    st.stop()

# ----------------------
# KPI Metrics
# ----------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Total Funds", len(df_amc))
col2.metric("📈 Avg Return (1Y)", f"{df_amc['return_1yr'].mean():.2f}%")
col3.metric("🚀 Best Return", f"{df_amc['return_1yr'].max():.2f}%")
col4.metric("📉 Worst Return", f"{df_amc['return_1yr'].min():.2f}%")

# ----------------------
# Data Table
# ----------------------
if show_data:
    st.subheader("📄 Fund Details")
    st.dataframe(
        df_amc[['MutualFundName', 'return_1yr']].reset_index(drop=True),
        use_container_width=True
    )

# ----------------------
# Bar Chart
# ----------------------
st.subheader("📊 1-Year Return Comparison")
fig, ax = plt.subplots(figsize=(14, 6))
sb.barplot(
    data=df_amc,
    x='MutualFundName',
    y='return_1yr',
    palette=palette_option,
    ax=ax
)
ax.set_xlabel("Mutual Fund")
ax.set_ylabel("1-Year Return (%)")
ax.set_title(f"{selected_amc} – Fund Performance")
plt.xticks(rotation=75, ha='right')
st.pyplot(fig)

# ----------------------
# Distribution Plot
# ----------------------
st.subheader("📈 Return Distribution")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sb.histplot(df_amc['return_1yr'], kde=True, ax=ax2)
ax2.set_xlabel("1-Year Return (%)")
ax2.set_title("Distribution of Returns")
st.pyplot(fig2)

# ----------------------
# Download Filtered Data
# ----------------------
st.subheader("⬇️ Export Data")
csv_buffer = StringIO()
df_amc.to_csv(csv_buffer, index=False)
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_buffer.getvalue(),
    file_name="filtered_mutual_funds.csv",
    mime="text/csv"
)
