# Superstore 2019 Sales Analysis & Dashboard

## Project Overview

This project analyzes the **Superstore 2019 dataset** using Python in
order to uncover business insights and build an interactive dashboard.

The goal of this project is to demonstrate a complete **end‑to‑end data
analysis workflow**, including:

-   Environment setup
-   Data loading and validation
-   Exploratory Data Analysis (EDA)
-   Feature engineering
-   Business insights extraction
-   Interactive dashboard development using Streamlit

This project is designed as a **portfolio‑level data analytics project**
suitable for showcasing on GitHub.

------------------------------------------------------------------------

# Dataset

Dataset: **Sample Superstore 2019**

Rows: **9,994**\
Columns: **21**

Main fields include:

-   Order ID
-   Order Date
-   Ship Date
-   Customer ID
-   Customer Name
-   Segment
-   City
-   State
-   Region
-   Category
-   Sub‑Category
-   Sales
-   Quantity
-   Discount
-   Profit

------------------------------------------------------------------------

# Project Structure

superstore-2019-python-dashboard/

│\
├── data/\
│ └── raw/\
│ └── Sample - Superstore 2019.xlsx

│\
├── notebooks/\
│ └── 01_data_understanding.ipynb

│\
├── app.py\
├── requirements.txt\
└── README.md

------------------------------------------------------------------------

# Environment Setup

A virtual environment was created to isolate project dependencies.

Create virtual environment:

``` bash
python -m venv .venv
```

Activate environment (Windows):

``` bash
.venv\Scripts\activate
```

------------------------------------------------------------------------

# Installing Dependencies

Install required libraries:

``` bash
pip install pandas numpy matplotlib seaborn plotly streamlit openpyxl
```

Save installed packages:

``` bash
pip freeze > requirements.txt
```

------------------------------------------------------------------------

# Running the Dashboard

To run the Streamlit dashboard locally:

``` bash
streamlit run app.py
```

The application will run at:

http://localhost:8501

------------------------------------------------------------------------

# Current Progress

Completed steps:

-   Project folder creation
-   Virtual environment setup
-   Python dependency installation
-   Dataset integration
-   Streamlit test dashboard
-   Dataset validation

Dataset successfully loaded with:

-   **9,994 rows**
-   **21 columns**

The Streamlit application successfully displays the dataset preview.

------------------------------------------------------------------------

# Next Development Steps

## 1. Data Understanding

-   Data structure analysis
-   Missing values detection
-   Duplicate record detection
-   Data types validation

## 2. Exploratory Data Analysis (EDA)

-   Sales analysis
-   Profit analysis
-   Discount impact analysis
-   Category performance
-   Regional performance

## 3. Feature Engineering

New variables will be created such as:

-   Year
-   Month
-   Quarter
-   Shipping delay
-   Profit ratio

## 4. Business Insights

Identify:

-   Most profitable categories
-   Loss‑making products
-   Discount impact on profitability
-   Top performing customers

## 5. Interactive Dashboard

The final dashboard will include:

-   KPI cards
-   Sales trends
-   Category performance charts
-   Region performance charts
-   Profit vs Discount analysis
-   Interactive filters

------------------------------------------------------------------------

# Tools & Technologies

Python\
Pandas\
NumPy\
Matplotlib\
Seaborn\
Plotly\
Streamlit

------------------------------------------------------------------------

# Author

Mohamed Kamal

Data Analytics Portfolio Project
