import pandas as pd
import plotly.express as px

def sales_profit_trend(df: pd.DataFrame):
    monthly = df.groupby("Month", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
    ).sort_values("Month")

    fig = px.line(monthly, x="Month", y=["Sales", "Profit"], markers=True, title="Sales & Profit Trend (Monthly)")
    fig.update_layout(xaxis_title="Month", yaxis_title="Amount")
    return fig

def bar_by_category(df: pd.DataFrame, value_col: str, title: str):
    agg = df.groupby("Category", as_index=False)[value_col].sum().sort_values(value_col, ascending=False)
    fig = px.bar(agg, x="Category", y=value_col, title=title, text_auto=".2s")
    fig.update_layout(xaxis_title="", yaxis_title=value_col)
    return fig

def avg_discount_by_category(df: pd.DataFrame):
    agg = df.groupby("Category", as_index=False)["Discount"].mean().sort_values("Discount", ascending=False)
    fig = px.bar(agg, x="Category", y="Discount", title="Average Discount by Category", text_auto=".2%")
    fig.update_layout(xaxis_title="", yaxis_title="Avg Discount")
    return fig

def sales_by_region(df: pd.DataFrame):
    agg = df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(agg, x="Region", y="Sales", title="Sales by Region", text_auto=".2s")
    fig.update_layout(xaxis_title="", yaxis_title="Sales")
    return fig

def discount_vs_profit(df: pd.DataFrame):
    fig = px.scatter(
        df,
        x="Discount",
        y="Profit",
        hover_data=["Category", "Sub-Category", "Product Name", "Region"],
        title="Discount vs Profit"
    )
    fig.update_layout(xaxis_title="Discount", yaxis_title="Profit")
    return fig

def top_products(df: pd.DataFrame, metric: str, n: int = 10, ascending: bool = False, title: str = ""):
    agg = df.groupby("Product Name", as_index=False)[metric].sum().sort_values(metric, ascending=ascending).head(n)
    fig = px.bar(agg.sort_values(metric), x=metric, y="Product Name", orientation="h", title=title)
    fig.update_layout(xaxis_title=metric, yaxis_title="")
    return fig, agg