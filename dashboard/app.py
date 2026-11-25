
import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Commercial Market Intelligence",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = "data/processed/"


# --------------------------------------------------
# DATA LOADING FUNCTIONS
# --------------------------------------------------

@st.cache_data
def load_products():

    return pd.read_csv(
        DATA_PATH + "product_summary.csv",
        index_col=0
    )


@st.cache_data
def load_monthly_sales():

    monthly_data = pd.read_csv(
        DATA_PATH + "monthly_sales.csv",
        index_col=0
    )

    monthly_sales = monthly_data["Revenue"]

    monthly_growth = monthly_sales.pct_change() * 100

    return monthly_sales, monthly_growth


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

customer_segments = pd.read_csv(
    DATA_PATH + "customer_segment_analysis.csv",
    index_col=0
)

customer_rfm = pd.read_csv(
    DATA_PATH + "customer_rfm_segments.csv",
    index_col=0
)

customer_country = pd.read_csv(
    DATA_PATH + "customer_country_analysis.csv",
    index_col=0
)

products = load_products()

monthly_sales, monthly_growth = load_monthly_sales()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div style="
    background: linear-gradient(120deg, #14213D, #274C77);
    padding: 32px;
    border-radius: 12px;
    margin-bottom: 20px;
">
    <h1 style="
        color: white;
        font-size: 36px;
        margin-bottom: 10px;
    ">
        Commercial Market Intelligence
    </h1>
    <p style="
        color: #DCE6F1;
        font-size: 16px;
        margin-bottom: 0;
    ">
        Retail analytics | Customer intelligence |
        Product performance | Market insights
    </p>
</div>
""", unsafe_allow_html=True)


st.info(
    "Dataset: UCI Online Retail | "
    "Historical transactions from December 2010 to December 2011. "
    "All revenue figures are reported in GBP (£)."
)

st.divider()


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_customers = customer_segments["Customers"].sum()

total_revenue = customer_segments["Total_Revenue"].sum()

total_transactions = customer_country["Total_Transactions"].sum()

average_revenue = total_revenue / total_customers

best_month = monthly_sales.idxmax()

best_month_revenue = monthly_sales.max()

best_growth_month = monthly_growth.idxmax()

best_growth = monthly_growth.max()


# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Customers",
    "Geographic Analysis",
    "Products"
])


# --------------------------------------------------
# TAB 1: OVERVIEW
# --------------------------------------------------

with tab1:

    st.subheader("Business Overview")

    st.markdown("""
    This overview summarizes the commercial performance
    of identified customers, including revenue, transactions
    and customer value.
    """)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Identified Customers",
        f"{total_customers:,.0f}"
    )

    col2.metric(
        "Identified Customer Revenue",
        f"£{total_revenue:,.2f}"
    )

    col3.metric(
        "Identified Customer Transactions",
        f"{total_transactions:,.0f}"
    )

    col4.metric(
        "Revenue per Identified Customer",
        f"£{average_revenue:,.2f}"
    )

    st.divider()

    col1, col2 = st.columns(2)

    col1.metric(
        "Best Sales Month",
        best_month,
        f"£{best_month_revenue:,.2f}"
    )

    col2.metric(
        "Highest Monthly Growth",
        best_growth_month,
        f"{best_growth:.2f}%"
    )

    st.subheader("Monthly Revenue Trend")

    st.line_chart(
        monthly_sales,
        x_label="Month",
        y_label="Revenue (£)"
    )

    st.caption(
        "Monthly revenue from physical product sales, "
        "December 2010–December 2011. "
        "December 2011 is incomplete."
    )

    st.divider()

    st.subheader("Monthly Revenue Growth (%)")

    st.bar_chart(
        monthly_growth.dropna(),
        x_label="Month",
        y_label="Growth (%)"
    )

    st.caption(
        "Month-over-month revenue growth. "
        "Positive values indicate growth, negative values indicate a decline."
    )


# --------------------------------------------------
# TAB 2: CUSTOMERS
# --------------------------------------------------

with tab2:

    st.subheader("Customer Segmentation")

    st.bar_chart(
        customer_segments["Customers"],
        horizontal=True,
        x_label="Number of Customers",
        y_label="Segment"
    )

    st.subheader("Revenue Contribution by Segment")

    st.bar_chart(
        customer_segments["Total_Revenue"],
        horizontal=True,
        x_label="Revenue (£)",
        y_label="Segment"
    )

    st.subheader("Customer Segment Details")

    st.dataframe(
        customer_segments,
        width="stretch"
    )

    st.divider()

    st.subheader("Customer RFM Explorer")

    selected_segment = st.selectbox(
        "Select a customer segment",
        ["All"] + sorted(
            customer_rfm["Segment"].unique().tolist()
        )
    )

    if selected_segment == "All":

        filtered_customers = customer_rfm

    else:

        filtered_customers = customer_rfm[
            customer_rfm["Segment"] == selected_segment
        ]

    st.dataframe(
        filtered_customers,
        width="stretch"
    )


# --------------------------------------------------
# TAB 3: GEOGRAPHIC ANALYSIS
# --------------------------------------------------

with tab3:

    st.subheader("Geographic Market Performance")

    top_countries = (
        customer_country["Total_Revenue"]
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(
        top_countries,
        horizontal=True,
        x_label="Revenue (£)",
        y_label="Country"
    )

    st.subheader("Country Details")

    selected_country = st.selectbox(
        "Select a country",
        customer_country.index.tolist()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Customers",
        f"{customer_country.loc[selected_country, 'Total_Customers']:,}"
    )

    col2.metric(
        "Total Revenue",
        f"£{customer_country.loc[selected_country, 'Total_Revenue']:,.2f}"
    )

    col3.metric(
        "Revenue per Customer",
        f"£{customer_country.loc[selected_country, 'Revenue_Per_Customer']:,.2f}"
    )

    st.dataframe(
        customer_country.loc[[selected_country]],
        width="stretch"
    )


# --------------------------------------------------
# TAB 4: PRODUCTS
# --------------------------------------------------

with tab4:

    st.subheader("Product Performance Overview")

    # Load pre-aggregated product data
    product_summary = products.copy()

    # Top 10 products by revenue
    top_products = (
        product_summary["Total_Revenue"]
        .nlargest(10)
        .sort_values()
    )

    st.bar_chart(
        top_products,
        horizontal=True,
        x_label="Revenue (£)",
        y_label="Product"
    )

    # Top 10 products by units sold
    st.subheader("Top Products by Units Sold")

    top_units = (
        product_summary["Total_Units"]
        .nlargest(10)
        .sort_values()
    )

    st.bar_chart(
        top_units,
        horizontal=True,
        x_label="Units Sold",
        y_label="Product"
    )

    # Product summary
    st.subheader("Product Summary")

    st.dataframe(
        product_summary.sort_values(
            "Total_Revenue",
            ascending=False
        ),
        width="stretch"
    )

    st.divider()

    # Product search
    st.subheader("Product Search")

    search_term = st.text_input(
        "Search for a product"
    )

    if search_term:

        st.caption(
            f"Search results for: {search_term}"
        )

        search_results = product_summary[
            product_summary.index.str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

        if not search_results.empty:

            st.caption(
                f"Products found: {len(search_results):,}"
            )

            st.dataframe(
                search_results,
                width="stretch"
            )

        else:

            st.warning(
                "No products found. Try another search term."
            )

    st.divider()

    # Pareto analysis
    st.subheader("Revenue Concentration (Pareto Analysis)")

    pareto = (
        product_summary["Total_Revenue"]
        .sort_values(ascending=False)
        .reset_index()
    )

    pareto["Cumulative_Revenue"] = (
        pareto["Total_Revenue"].cumsum()
    )

    pareto["Cumulative_Percentage"] = (
        pareto["Cumulative_Revenue"] /
        pareto["Total_Revenue"].sum()
    ) * 100

    products_for_80 = (
        pareto["Cumulative_Percentage"] <= 80
    ).sum() + 1

    total_products = len(pareto)

    col1, col2 = st.columns(2)

    col1.metric(
        "Products needed for approximately 80% of revenue",
        f"{products_for_80:,}"
    )

    col2.metric(
        "Total unique products",
        f"{total_products:,}"
    )

    st.line_chart(
        pareto["Cumulative_Percentage"],
        x_label="Products (ranked by revenue)",
        y_label="Cumulative Revenue (%)"
    )
