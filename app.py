import streamlit as st
import pandas as pd
import os
import joblib

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
@st.cache_data
def load_forecast():
    forecast_df = pd.read_csv("data/forecast_sales.csv")
    forecast_df["ds"] = pd.to_datetime(forecast_df["ds"])
    return forecast_df

forecast_df = load_forecast()

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

monthly_sales = df.groupby(
    pd.Grouper(key="Order Date", freq="M")
)["Sales"].sum().reset_index()

monthly_sales.columns = ["ds", "y"]

@st.cache_resource
def load_model():
    return joblib.load("models/profit_model.pkl")

model = load_model()

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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Overview", "Category", "Products", "Discount & Risk", "Profit Prediction", "Sales Forecast"]
)

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

with tab5:
    st.subheader("Profit Prediction")

    st.write("Enter order details to predict whether the transaction is likely to be profitable or loss-making.")

    col1, col2 = st.columns(2)

    with col1:
        sales_input = st.number_input("Sales", min_value=0.0, value=500.0, step=50.0)
        discount_input = st.number_input("Discount", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
        quantity_input = st.number_input("Quantity", min_value=1, value=3, step=1)
        category_input = st.selectbox("Category", sorted(df["Category"].dropna().unique()))

    with col2:
        subcats = df[df["Category"] == category_input]["Sub-Category"].unique()

        subcategory_input = st.selectbox(
            "Sub-Category",
            sorted(subcats)
        )

        segment_input = st.selectbox("Segment", sorted(df["Segment"].dropna().unique()))
        region_input = st.selectbox("Region", sorted(df["Region"].dropna().unique()))
        shipmode_input = st.selectbox("Ship Mode", sorted(df["Ship Mode"].dropna().unique()))

    input_df = pd.DataFrame([{
        "Sales": sales_input,
        "Discount": discount_input,
        "Quantity": quantity_input,
        "Category": category_input,
        "Sub-Category": subcategory_input,
        "Segment": segment_input,
        "Region": region_input,
        "Ship Mode": shipmode_input
    }])

    # -----------------------
    # Prediction
    # -----------------------
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    profit_prob = probabilities[0]
    loss_prob = probabilities[1]

    st.markdown("### Prediction Result")

    if loss_prob > 0.6:
        st.error(f"⚠ High Risk Transaction ({loss_prob:.1%} probability of loss)")

    elif loss_prob > 0.4:
        st.warning(f"⚠ Moderate Risk ({loss_prob:.1%} probability of loss)")

    else:
        st.success(f"✔ Likely Profitable ({profit_prob:.1%} probability of profit)")

    # -----------------------
    # Show probabilities
    # -----------------------
    st.write("Prediction probabilities:")
    st.write(f"- Profit probability: **{profit_prob:.1%}**")
    st.write(f"- Loss probability: **{loss_prob:.1%}**")

    # -----------------------
    # Model Explainability
    # -----------------------
    st.markdown("### Model Explainability")

    import matplotlib.pyplot as plt

    feature_names = model.named_steps["prep"].get_feature_names_out()
    importances = model.named_steps["model"].feature_importances_

    feat_imp = pd.Series(importances, index=feature_names)

    top_features = feat_imp.sort_values().tail(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    top_features.plot(kind="barh", ax=ax)
    ax.set_title("Top Features Influencing Profitability")

    st.pyplot(fig)

with tab6:
    st.subheader("Sales Forecast")

    st.write("This section shows the expected future sales based on historical monthly sales using Prophet forecasting.")

    # -----------------------
    # KPI Calculations
    # -----------------------
    next_month_sales = forecast_df.iloc[0]["yhat"]
    next_quarter_sales = forecast_df.head(3)["yhat"].sum()

    last_actual_month_sales = monthly_sales["y"].iloc[-1]
    forecast_growth = ((next_month_sales - last_actual_month_sales) / last_actual_month_sales) * 100

    k1, k2, k3 = st.columns(3)

    k1.metric("Expected Sales Next Month", f"${next_month_sales:,.0f}")
    k2.metric("Expected Sales Next Quarter", f"${next_quarter_sales:,.0f}")
    k3.metric("Forecast Growth Rate", f"{forecast_growth:.2f}%")

    st.divider()

    # -----------------------
    # Forecast Chart
    # -----------------------
    st.markdown("### Forecast Chart")

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(monthly_sales["ds"], monthly_sales["y"], label="Historical Sales")
    ax.plot(forecast_df["ds"], forecast_df["yhat"], label="Forecast", color="red")
    ax.fill_between(
        forecast_df["ds"],
        forecast_df["yhat_lower"],
        forecast_df["yhat_upper"],
        color="red",
        alpha=0.2,
        label="Confidence Interval"
    )

    ax.set_title("Next 6 Months Sales Forecast")
    ax.legend()

    st.pyplot(fig)

    # -----------------------
    # Forecast Table
    # -----------------------
    st.markdown("### Next 6 Months Forecast")

    display_forecast = forecast_df.copy()
    display_forecast["ds"] = display_forecast["ds"].dt.strftime("%Y-%m-%d")

    st.dataframe(display_forecast, use_container_width=True)