
import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Commercial Market Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("Commercial Market Intelligence")

st.markdown("""
Interactive dashboard for commercial sales, product performance,
customer segmentation and geographic market analysis.
""")

st.info(
    "Dataset: UCI Online Retail | "
    "Historical transactions from December 2010 to December 2011. "
    "All revenue figures are reported in GBP (£)."
)

st.divider()



DATA_PATH = "data/processed/"


@st.cache_data
def load_products():
    return pd.read_csv(
        DATA_PATH + "physical_products.csv",
        usecols=["StockCode", "Description", "Quantity", "Revenue"]
    )


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




total_customers = customer_segments["Customers"].sum()

total_revenue = customer_segments["Total_Revenue"].sum()

total_transactions = customer_country["Total_Transactions"].sum()

average_revenue = total_revenue / total_customers



tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Customers",
    "Geographic Analysis",
    "Products"
])



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
        f"{total_customers:,}"
    )

    col2.metric(
        "Identified Customer Revenue",
        f"£{total_revenue:,.2f}"
    )

    col3.metric(
        "Identified Customer Transactions",
        f"{total_transactions:,}"
    )

    col4.metric(
        "Revenue per Identified Customer",
        f"£{average_revenue:,.2f}"
    )



with tab2:

    st.subheader("Customer Segmentation")

    st.bar_chart(
        customer_segments["Customers"],
        x_label="Customer Segment",
        y_label="Number of Customers"
    )

    st.subheader("Revenue Contribution by Segment")

    st.bar_chart(
        customer_segments["Revenue_Share"],
        x_label="Customer Segment",
        y_label="Revenue Share (%)"
    )

    st.divider()

    st.subheader("Customer Segment Details")

    st.dataframe(
        customer_segments.style.format({
            "Total_Revenue": "£{:,.2f}",
            "Average_Revenue": "£{:,.2f}",
            "Average_Frequency": "{:.2f}",
            "Average_Recency": "{:.2f}",
            "Revenue_Share": "{:.2f}%"
        }),
        width="stretch"
    )

    st.divider()

    st.subheader("Explore Individual Customers")

    segments = sorted(customer_rfm["Segment"].unique())

    selected_segment = st.selectbox(
        "Select a customer segment:",
        ["All Segments"] + segments
    )

    if selected_segment == "All Segments":

        filtered_customers = customer_rfm

    else:

        filtered_customers = customer_rfm[
            customer_rfm["Segment"] == selected_segment
        ]

    st.write(
        f"Customers found: {len(filtered_customers):,}"
    )

    st.dataframe(
        filtered_customers,
        width="stretch"
    )



with tab3:

    st.subheader("Geographic Market Performance")

    top_countries = customer_country.sort_values(
        "Total_Revenue",
        ascending=False
    ).head(10)

    st.bar_chart(
        top_countries["Total_Revenue"],
        x_label="Country",
        y_label="Revenue (£)"
    )

    st.divider()

    st.subheader("Explore Geographic Markets")

    countries = sorted(customer_country.index.unique())

    selected_country = st.selectbox(
        "Select a country:",
        ["All Countries"] + countries
    )

    if selected_country == "All Countries":

        filtered_countries = customer_country

    else:

        filtered_countries = customer_country.loc[
            [selected_country]
        ]

    st.dataframe(
        filtered_countries.style.format({
            "Total_Revenue": "£{:,.2f}",
            "Revenue_Per_Customer": "£{:,.2f}"
        }),
        width="stretch"
    )




with tab4:

    st.subheader("Product Performance Overview")

    products = load_products()
    

    

    st.subheader("Top 10 Products by Revenue")

    top_products = (
        products
        .groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(
        top_products.sort_values(),
        horizontal=True,
        x_label="Revenue (£)",
        y_label="Product"
    )

    # Top 10 products by units sold

    st.subheader("Top 10 Products by Units Sold")

    top_products_units = (
        products
        .groupby("Description")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(
        top_products_units.sort_values(),
        horizontal=True,
        x_label="Units Sold",
        y_label="Product"
    )

    st.divider()

    

    st.subheader("Product Performance Details")

    product_summary = (
        products
        .groupby(["StockCode", "Description"])
        .agg(
            Total_Units=("Quantity", "sum"),
            Total_Revenue=("Revenue", "sum")
        )
        .reset_index()
    )

    product_summary["Average_Unit_Price"] = (
        product_summary["Total_Revenue"] /
        product_summary["Total_Units"]
    )

    st.dataframe(
        product_summary.sort_values(
            "Total_Revenue",
            ascending=False
        ),
        width="stretch",
        hide_index=True
    )

    

    st.subheader("Search Products")

    product_search = st.text_input(
        "Enter a product name:"
    )

    if product_search:

        search_results = product_summary[
            product_summary["Description"].str.contains(
                product_search,
                case=False,
                na=False
            )
        ]

        st.write(
            f"Products found: {len(search_results):,}"
        )

        st.dataframe(
            search_results,
            width="stretch",
            hide_index=True
        )

    st.divider()

    

    st.subheader("Product Revenue Concentration")

    total_product_revenue = product_summary["Total_Revenue"].sum()

    product_revenue_sorted = product_summary.sort_values(
        "Total_Revenue",
        ascending=False
    ).copy()

    product_revenue_sorted["Cumulative_Revenue"] = (
        product_revenue_sorted["Total_Revenue"].cumsum()
    )

    product_revenue_sorted["Cumulative_Percentage"] = (
        product_revenue_sorted["Cumulative_Revenue"] /
        total_product_revenue
    ) * 100

    products_for_80 = (
        product_revenue_sorted["Cumulative_Percentage"] < 80
    ).sum() + 1

    col1, col2 = st.columns(2)

    col1.metric(
        "Unique Products",
        f"{len(product_summary):,}"
    )

    col2.metric(
        "Products Generating 80% of Revenue",
        f"{products_for_80:,}"
    )

    st.write(
        f"These products represent "
        f"{products_for_80 / len(product_summary) * 100:.2f}% "
        f"of the catalog."
    )

    

    st.subheader("Pareto Analysis - Cumulative Revenue")

    pareto_chart_data = product_revenue_sorted.head(100).copy()

    pareto_chart_data["Product_Rank"] = range(
        1,
        len(pareto_chart_data) + 1
    )

    pareto_chart_data = pareto_chart_data.set_index(
        "Product_Rank"
    )

    st.line_chart(
        pareto_chart_data["Cumulative_Percentage"],
        x_label="Product Rank",
        y_label="Cumulative Revenue (%)"
    )

    st.caption(
        "The chart displays the cumulative revenue contribution "
        "of the top 100 products."
    )
