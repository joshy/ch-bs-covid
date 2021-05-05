import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime
from datetime import datetime as dt
from datetime import timedelta

import streamlit as st

# st.set_page_config(layout="wide")


def vaccination_lc(x, y):
    fig, ax = plt.subplots(figsize=(15, 3), dpi=600)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.step(
        x,
        y,
        where="mid",
        color="#024b7a",
    )
    ax.yaxis.grid(alpha=0.3, linestyle="--")
    ax.set_facecolor("#f9f9f9")
    return fig


st.header("Switzerland - Basel - Covid data")
df_vacc = pd.read_csv(
    "https://data.bs.ch/api/v2/catalog/datasets/100111/exports/csv?limit=-1&timezone=UTC&delimiter=%3B&order_by=datum%20desc",
    sep=";",
    parse_dates=["datum"],
)
df_vacc["weekday"] = df_vacc["datum"].dt.weekday


df_cases = pd.read_csv(
    "https://data.bs.ch/api/v2/catalog/datasets/100073/exports/csv?limit=100&timezone=UTC&delimiter=%3B&order_by=date%20desc",
    sep=";",
    parse_dates=["date"],
)


yesterday = dt.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
    days=1
)
st.write(f"Data for yesterday: {yesterday.strftime('%Y-%m-%d')}")
col1, col2 = st.beta_columns(2)
col1.text("Vaccinated yesterday")
col1.markdown(
    f'**{df_vacc[(df_vacc["datum"] == yesterday)]["im_impfzentrum_verabreichte_impfungen_pro_tag"].values[0]}**'
)
col2.text("New confirmed COVID cases Basel-Stadt")
col2.markdown(
    f'**{df_cases[(df_cases["date"] == yesterday)]["ndiff_conf"].values[0]}**'
)


df_last_week = df_vacc.iloc[:7, :]
st.subheader("Vaccination delivered last 7 days")
fig = vaccination_lc(
    df_last_week["datum"], df_last_week["im_impfzentrum_verabreichte_impfungen_pro_tag"]
)
st.write(fig)

st.subheader("Vaccination delivered from start")
fig = vaccination_lc(
    df_vacc["datum"], df_vacc["im_impfzentrum_verabreichte_impfungen_pro_tag"]
)
st.pyplot(fig)
