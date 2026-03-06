import streamlit as st
import pandas as pd
import os

from src.data import load_data, apply_filters
from src.metrics import compute_kpis, yoy_sales_profit
from src.charts import (
    sales_profit_trend,
    bar_by_category,
    avg_discount_by_category,
    sales_by_region,
    discount_vs_profit,
    top_products,
)

def color_profit(val):
    if val < 0:
        return "color: red"
    else:
        return "color: lightgreen"

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

@st.cache_data
def get_data():
    return load_data("data/raw/Sample - Superstore 2019.xlsx")

df = get_data()

st.title("Superstore Performance Dashboard")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

years_all = sorted([y for y in df["Year"].dropna().unique()])
regions_all = sorted(df["Region"].dropna().unique())
categories_all = sorted(df["Category"].dropna().unique())
segments_all = sorted(df["Segment"].dropna().unique())

years = st.sidebar.multiselect("Year", years_all, default=years_all)
regions = st.sidebar.multiselect("Region", regions_all, default=regions_all)
categories = st.sidebar.multiselect("Category", categories_all, default=categories_all)
segments = st.sidebar.multiselect("Segment", segments_all, default=segments_all)

df_f = apply_filters(df, years=years, regions=regions, categories=categories, segments=segments)
# -----------------------------
# Download filtered dataset
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Export")

@st.cache_data
def to_csv_bytes(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv(index=False).encode("utf-8")

csv_bytes = to_csv_bytes(df_f)

st.sidebar.download_button(
    label="Download filtered data (CSV)",
    data=csv_bytes,
    file_name="superstore_filtered.csv",
    mime="text/csv",
    use_container_width=True
)

# -------------------------
# KPI Row + Trend Indicators
# -------------------------
k = compute_kpis(df_f)
yoy = yoy_sales_profit(df_f)

# last YoY values (if available)
sales_yoy = float(yoy["Sales YoY %"].dropna().iloc[-1]) if yoy["Sales YoY %"].dropna().shape[0] else None
profit_yoy = float(yoy["Profit YoY %"].dropna().iloc[-1]) if yoy["Profit YoY %"].dropna().shape[0] else None

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Total Sales", f"${k['total_sales']:,.0f}", f"{sales_yoy:.1f}% YoY" if sales_yoy is not None else None)
c2.metric("Total Profit", f"${k['total_profit']:,.0f}", f"{profit_yoy:.1f}% YoY" if profit_yoy is not None else None)
c3.metric("Profit Margin", f"{k['profit_margin']*100:.2f}%")
c4.metric("Orders", f"{k['orders']:,}")
c5.metric("Customers", f"{k['customers']:,}")
c6.metric("Loss Lines", f"{k['loss_lines']:,}")

st.divider()

# -------------------------
# Tabs (Company-style)
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Category", "Products", "Discount & Risk"])

with tab1:
    left, right = st.columns(2)
    left.plotly_chart(sales_profit_trend(df_f), use_container_width=True)
    right.plotly_chart(sales_by_region(df_f), use_container_width=True)

    st.subheader("Executive Insights (auto)")

    loss_rate = (df_f["Profit"] < 0).mean() * 100

    if loss_rate > 15:
        st.warning("⚠ High percentage of loss-making transactions detected. Review discount strategy.")

    insights = []

    insights.append(f"Loss line rate: {loss_rate:.1f}% of rows have negative profit.")

    # Simple auto-insights based on filtered data
    cat_profit = df_f.groupby("Category")["Profit"].sum().sort_values(ascending=False)

    if len(cat_profit) >= 1:
        insights.append(f"Top profitable category: {cat_profit.index[0]} (Profit = ${cat_profit.iloc[0]:,.0f})")

    worst_cat = df_f.groupby("Category")["Profit"].sum().sort_values().index[0]
    insights.append(f"Worst performing category: {worst_cat}, indicating potential pricing or discount strategy issues.")
    insights.append("Higher discounts are associated with negative profit (see Discount & Risk tab).")

    for insight in insights:
        st.write(f"• {insight}")

with tab2:
    colA, colB = st.columns(2)
    colA.plotly_chart(bar_by_category(df_f, "Sales", "Total Sales by Category"), use_container_width=True)
    colB.plotly_chart(bar_by_category(df_f, "Profit", "Total Profit by Category"), use_container_width=True)

    st.plotly_chart(avg_discount_by_category(df_f), use_container_width=True)

    st.subheader("Drill-down: Sub-Category inside a Category")
    chosen_cat = st.selectbox("Choose a Category", categories_all, index=0)
    df_cat = df_f[df_f["Category"] == chosen_cat]
    sub_profit = df_cat.groupby("Sub-Category", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).sort_values("Profit")
    st.dataframe(sub_profit, use_container_width=True)

with tab3:
    colA, colB = st.columns(2)
    fig_top_sales, top_sales_tbl = top_products(df_f, metric="Sales", n=10, ascending=False, title="Top 10 Products by Sales")
    fig_top_loss, top_loss_tbl = top_products(df_f, metric="Profit", n=10, ascending=True, title="Top 10 Loss-Making Products")

    colA.plotly_chart(fig_top_sales, use_container_width=True)
    colB.plotly_chart(fig_top_loss, use_container_width=True)

    st.subheader("Top Loss-Making Sub-Categories")
    loss_sub = df_f.groupby("Sub-Category")["Profit"].sum().sort_values().head(10).reset_index()
    st.dataframe(loss_sub, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # High Sales but Negative Profit
    # --------------------------------------------------

    st.subheader("High Sales but Negative Profit")

    high_sales_loss = (
        df_f.groupby("Product Name")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )

    high_sales_loss = high_sales_loss[
        (high_sales_loss["Sales"] > high_sales_loss["Sales"].quantile(0.75)) &
        (high_sales_loss["Profit"] < 0)
    ].sort_values("Profit")

    st.dataframe(high_sales_loss)


    st.divider()

    # --------------------------------------------------
    # Worst Profit Margin Products
    # --------------------------------------------------

    st.subheader("Products with Worst Profit Margin")

    margin_df = (
        df_f.groupby("Product Name")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )

    margin_df["Profit Margin"] = margin_df["Profit"] / margin_df["Sales"]

    worst_margin = margin_df.sort_values("Profit Margin").head(10)

    st.dataframe(worst_margin.style.applymap(color_profit, subset=["Profit"]))

    

with tab4:
    st.plotly_chart(discount_vs_profit(df_f), use_container_width=True)

    st.subheader("Risk Table: High Discount + Negative Profit")
    risk = df_f[(df_f["Discount"] >= 0.4) & (df_f["Profit"] < 0)].copy()
    risk = risk.sort_values("Profit").head(25)

    cols = ["Order ID", "Order Date", "Region", "Category", "Sub-Category", "Product Name", "Discount", "Sales", "Profit"]
    st.dataframe(risk[cols], use_container_width=True)

    st.caption("Rule used: Discount >= 40% AND Profit < 0 (Top 25 worst cases).")