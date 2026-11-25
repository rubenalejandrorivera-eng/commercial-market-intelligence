Commercial Market Intelligence: Executive Summary

Project overview

I analyzed historical transaction data from a UK-based online retailer to look at sales trends, product performance, customer behavior, and how revenue splits by geography. I used Python to turn the raw transactions into business findings and built an interactive dashboard to present them.

Methodology

The data comes from the UCI Online Retail dataset, which has 541,909 transaction records from December 2010 to December 2011. The work followed these steps:

Cleaning: I found missing values, cancellations, returns, zero-price transactions, and accounting adjustments.
Transformation: I classified the transactions and separated physical product sales for the main commercial analysis.
Product analysis: I looked at revenue by product, the top performers, and how concentrated revenue is.
Customer segmentation: I used RFM (Recency, Frequency, Monetary) analysis to group customers.
Geographic analysis: I compared revenue from the United Kingdom with revenue from international markets.
Visualization: I built a Streamlit dashboard to share the results.

Key findings

Product revenue concentration. About 20.73% of the product catalog generated 80.03% of physical product revenue.
Geographic distribution. The United Kingdom accounted for 85.18% of physical product revenue and international markets for 14.82%. The five largest international markets made up 71.09% of international revenue.
Customer segments. The RFM analysis covered 4,335 customers with customer IDs. The Champions segment was about 30% of them and generated 72.77% of their revenue.
Sales by month. November 2011 was the strongest month, with about £1.46 million in physical product revenue.

Business implications

A retailer could act on these results in four ways: review inventory and merchandising with the highest-revenue products in mind, look for ways to grow international sales, build retention efforts around the most valuable customer segments, and study purchasing patterns for commercial planning.

Technologies and tools

Python, Pandas, NumPy, Matplotlib, Seaborn, Streamlit, Jupyter Notebook, Git, GitHub

Deliverables

Interactive dashboard on Streamlit Community Cloud
Data exploration and analysis notebook
Processed datasets and visualizations
Documented GitHub repository

Live dashboard: https://commercial-market-intelligence-ujikepaephucbtc5itpssy.streamlit.app/
GitHub repository: https://github.com/rubenalejandrorivera-eng/commercial-market-intelligence

Limitations

The data covers 2010 to 2011 and does not reflect current market conditions. Revenue is not profit, because product costs and operating expenses were not available. The customer segmentation only includes records with a customer ID.