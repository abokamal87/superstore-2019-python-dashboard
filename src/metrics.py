import pandas as pd

def compute_kpis(df: pd.DataFrame) -> dict:
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    orders = df["Order ID"].nunique()
    customers = df["Customer ID"].nunique()
    loss_lines = int((df["Profit"] < 0).sum())
    margin = (total_profit / total_sales) if total_sales else 0.0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "orders": orders,
        "customers": customers,
        "loss_lines": loss_lines,
        "profit_margin": margin,
    }

def yoy_sales_profit(df: pd.DataFrame) -> pd.DataFrame:
    # Year-over-year totals
    yearly = df.groupby("Year", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
    ).sort_values("Year")

    yearly["Sales YoY %"] = yearly["Sales"].pct_change() * 100
    yearly["Profit YoY %"] = yearly["Profit"].pct_change() * 100
    return yearly