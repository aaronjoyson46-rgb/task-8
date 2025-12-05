
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Make sure sales_data.csv is in the same folder as this app
    df = pd.read_csv("sales_data.csv")
    df["revenue"] = df["price"] * df["quantity"]
    return df

def main():
    st.set_page_config(page_title="E-commerce Sales Dashboard", layout="wide")
    st.title("📊 E-commerce Sales Performance Dashboard")
    st.write(
        "This dashboard is part of a business analysis project focused on understanding "
        "sales performance, customer behaviour, and product category trends."
    )

    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filters")
    categories = df["category"].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "Select product categories:",
        options=categories,
        default=categories
    )

    # Apply filters
    filtered_df = df[df["category"].isin(selected_categories)]

    # KPIs
    total_revenue = filtered_df["revenue"].sum()
    total_orders = filtered_df["order_id"].nunique()
    total_customers = filtered_df["customer_id"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("Total Orders", f"{total_orders}")
    col3.metric("Unique Customers", f"{total_customers}")
    col4.metric("Avg. Order Value", f"₹{avg_order_value:,.2f}")

    st.markdown("---")

    # Revenue by Category
    st.subheader("Revenue by Category")
    revenue_by_cat = filtered_df.groupby("category")["revenue"].sum().reset_index()

    if len(revenue_by_cat) > 0:
        st.bar_chart(revenue_by_cat.set_index("category")["revenue"])
    else:
        st.info("No data available for the selected filters.")

    st.markdown("---")

    # Detailed table
    st.subheader("Detailed Sales Data")
    st.dataframe(filtered_df)

    st.markdown(
        """
        **How to use this app in your portfolio:**
        - Mention that you built an interactive Streamlit dashboard for sales analysis.  
        - Explain how the KPIs and charts support business decisions about product performance and revenue.  
        - Host this app on Streamlit Cloud or share screenshots in your PPT/Word report.
        """
    )

if __name__ == "__main__":
    main()
