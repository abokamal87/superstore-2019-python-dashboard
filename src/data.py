import pandas as pd
import numpy as np

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    # Dates
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    # Time features
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)  # e.g. 2016-01

    # Profit metrics
    df["Profit Margin"] = np.where(df["Sales"] != 0, df["Profit"] / df["Sales"], np.nan)
    df["Is Loss"] = df["Profit"] < 0

    # Shipping delay (optional)
    df["Ship Delay Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    return df

def apply_filters(
    df: pd.DataFrame,
    years: list[int] | None = None,
    regions: list[str] | None = None,
    categories: list[str] | None = None,
    segments: list[str] | None = None,
) -> pd.DataFrame:
    out = df.copy()

    if years:
        out = out[out["Year"].isin(years)]
    if regions:
        out = out[out["Region"].isin(regions)]
    if categories:
        out = out[out["Category"].isin(categories)]
    if segments:
        out = out[out["Segment"].isin(segments)]

    return out