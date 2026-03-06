# Superstore Sales Analytics Dashboard

An **end-to-end Data Analytics project** that analyzes retail sales data, builds interactive dashboards, applies machine learning for profit prediction, and performs sales forecasting using time series models.

---

# Live Dashboard

**Interactive Streamlit App**

https://superstore-2019-python-dashboard-zxena2enreadmjjm5szriw.streamlit.app/

---

# Project Overview

This project analyzes the **Superstore retail dataset** to extract business insights, build interactive dashboards, and apply predictive analytics techniques.

The solution includes:

* Data exploration and preparation
* Interactive dashboard using Streamlit
* Machine learning model to predict profitable vs loss transactions
* Time series forecasting to estimate future sales
* Deployment to Streamlit Cloud

---

# Key Features

### 1. Sales Performance Dashboard

Interactive dashboard displaying:

* Total Sales
* Total Profit
* Profit Margin
* Number of Orders
* Customer count
* Loss-making transactions

Includes multiple analysis tabs:

* Overview
* Category Analysis
* Product Analysis
* Discount & Risk Analysis

---

### 2. Profit Prediction (Machine Learning)

A classification model predicts whether an order will be:

* Profitable
* Loss-making

Input features include:

* Sales
* Discount
* Quantity
* Category
* Sub-Category
* Region
* Segment
* Ship Mode

The model returns:

* Profit probability
* Loss probability
* Risk indicator

---

### 3. Sales Forecasting

A **Prophet time-series model** predicts future monthly sales.

Forecast section includes:

* Expected sales next month
* Expected sales next quarter
* Forecast growth rate
* Forecast chart with confidence interval
* Next 6 months forecast table

---

# Project Structure

```
superstore-2019-python-dashboard

assets/                 Dashboard screenshots
data/
    raw/                Original dataset
    forecast_sales.csv  Forecast output

models/
    profit_prediction_model.pkl

notebooks/
    01_data_understanding.ipynb
    02_dashboard_preparation.ipynb
    03_profit_prediction.ipynb
    04_sales_forecasting.ipynb

src/
    data.py
    metrics.py
    charts.py

app.py
requirements.txt
README.md
```

---

# Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Prophet
* Plotly
* Matplotlib
* Streamlit

---

# Business Insights

Key insights discovered during analysis:

* Technology category generates the highest profit
* Furniture category has the highest risk of loss
* High discounts strongly correlate with negative profit
* Sales show a consistent upward trend over the years
* Peak sales typically occur during the fourth quarter

---

# How to Run the Project

Clone the repository:

```
git clone https://github.com/your-repo-link
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the dashboard:

```
streamlit run app.py
```

---

# Author

Mohamed Kamal

Data Analyst | Python | Machine Learning | Data Visualization
