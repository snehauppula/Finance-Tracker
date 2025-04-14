import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set Seaborn style for consistency
sns.set_style("whitegrid")
plt.rcParams["font.size"] = 12  # Slightly larger font for readability

# Title and intro
st.title("💰 Personal Finance Tracker")
st.markdown("Analyze your spending patterns with ease—upload your transaction data below!")

# File uploader with improved UX
file = st.file_uploader(
    "Upload CSV File",
    type=["csv"],
    help="Expected columns: 'Date' (e.g., 2025-01-01), 'Amount' (e.g., 45.80), 'Category' (e.g., Food)"
)

if file is not None:
    # Load and preprocess data with error handling
    try:
        df = pd.read_csv(file, on_bad_lines='skip')
        if not {'Date', 'Amount', 'Category'}.issubset(df.columns):
            st.error("CSV must include 'Date', 'Amount', and 'Category' columns.")
            st.stop()
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    # Data cleaning
    df.fillna({'Amount': 0, 'Category': 'Unknown'}, inplace=True)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
    df = df[df['Amount'] >= 0]  # Filter out negatives
    df['Category'] = df['Category'].str.capitalize().str.strip()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True)

    if df.empty:
        st.warning("No valid data after cleaning. Check your file format.")
        st.stop()

    # Sidebar filters with better layout
    st.sidebar.header("🔍 Filters")
    category_options = ["All"] + sorted(df['Category'].unique().tolist())
    category_filter = st.sidebar.selectbox("Category", options=category_options)
    if category_filter != "All":
        df = df[df['Category'] == category_filter]

    if not df['Date'].empty:
        min_date, max_date = df['Date'].min().date(), df['Date'].max().date()
        if min_date < max_date:
            date_range = st.sidebar.slider(
                "Date Range", min_date, max_date, (min_date, max_date), format="YYYY-MM-DD"
            )
            df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & 
                    (df['Date'] <= pd.to_datetime(date_range[1]))]
        else:
            st.sidebar.info("Date range filter unavailable (single date detected).")

    # Tabs for organized layout
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🍰 Spending Breakdown", "📈 Trends"])

    with tab1:  # Overview
        st.subheader("Data Snapshot")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(df.style.format({"Amount": "${:.2f}"}), height=250, use_container_width=True)
        with col2:
            total_spending = df['Amount'].sum().round(2)
            st.metric("Total Spending", f"${total_spending:,.2f}", delta_color="off")
            if not df.empty:
                top_category = df.groupby('Category')['Amount'].sum().idxmax()
                top_spending = df.groupby('Category')['Amount'].sum().max().round(2)
                st.metric("Top Category", top_category, f"${top_spending:,.2f}", delta_color="off")

    with tab2:  # Spending Breakdown
        st.subheader("Spending by Category")
        if not df.empty:
            col1, col2 = st.columns([1, 2])
            category_spending = df.groupby('Category')['Amount'].sum().round(2)
            with col1:
                st.write("**Category Totals:**")
                for cat, amt in category_spending.items():
                    st.write(f"{cat}: ${amt:,.2f}")
            with col2:
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.pie(category_spending, labels=category_spending.index, autopct='%1.0f%%', 
                       colors=sns.color_palette("muted"), startangle=90)
                ax.set_title("Spending Distribution", pad=20)
                st.pyplot(fig)

    with tab3:  # Trends
        if not df['Date'].empty:
            st.subheader("Spending Trends")
            df['Month'] = df['Date'].dt.to_period('M').astype(str)
            monthly_spending = df.groupby('Month')['Amount'].sum().reset_index()

            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.barplot(x='Month', y='Amount', data=monthly_spending, palette='viridis', ax=ax)
                ax.set_title("Monthly Spending", pad=20)
                ax.set_xlabel("Month", labelpad=10)
                ax.set_ylabel("Amount ($)", labelpad=10)
                plt.xticks(rotation=45, ha="right")
                st.pyplot(fig)
            with col2:
                df['Week'] = df['Date'].dt.to_period('W').astype(str)
                weekly_spending = df.groupby('Week')['Amount'].sum().reset_index().tail(10)
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.barplot(x='Week', y='Amount', data=weekly_spending, palette='coolwarm', ax=ax)
                ax.set_title("Weekly Spending (Last 10 Weeks)", pad=20)
                ax.set_xlabel("Week", labelpad=10)
                ax.set_ylabel("Amount ($)", labelpad=10)
                plt.xticks(rotation=45, ha="right")
                st.pyplot(fig)

            st.subheader("Day & Month Trends")
            df['DayOfWeek'] = df['Date'].dt.day_name()
            df['Month'] = df['Date'].dt.month_name()
            heatmap_data = df.pivot_table(values='Amount', index='DayOfWeek', columns='Month', 
                                        aggfunc='sum', fill_value=0)
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", 
                        cbar_kws={'label': 'Spending ($)'}, ax=ax)
            ax.set_title("Spending by Day and Month", pad=20)
            st.pyplot(fig)

    # Download button
    st.download_button(
        label="⬇️ Download Filtered Data",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="filtered_finance_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file with 'Date', 'Amount', and 'Category' columns to get started.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Sneha’s Finance Tracker")