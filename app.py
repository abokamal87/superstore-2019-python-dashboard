import streamlit as st
import pandas as pd

st.title("Superstore Dashboard - Setup Test")

df = pd.read_excel("data/raw/Sample - Superstore 2019.xlsx")  # <-- xlsx

st.write("Dataset Shape:", df.shape)
st.dataframe(df.head())