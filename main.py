import datetime
from datetime import datetime as dt
from datetime import timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def display(value):
    f = format(value, "_")
    return f.replace("_", "'")


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
    return fig, ax


st.header("Covid & Vaccination stats for Basel, Switzerland")
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
st.markdown(f"Data for yesterday: **{yesterday.strftime('%Y-%m-%d')}**")
print(df_vacc.columns)
col1, col2, col3, col4 = st.beta_columns(4)
col1.text("New confirmed cases")
col1.markdown(
    f'**{df_cases[(df_cases["date"] == yesterday)]["ndiff_conf"].values[0]}**'
)

col2.text("Vaccinated")
col2.markdown(
    f'**{display(df_vacc[(df_vacc["datum"] == yesterday)]["total_verabreichte_impfungen_pro_tag"].values[0])}**'
)

col3.text("Full vaccinated")
fully_vacc = df_vacc[(df_vacc["datum"] == yesterday)]["total_personen_mit_zweiter_dosis"].values[0]
col3.markdown(f'**{display(fully_vacc)}**')

col4.text("% of population")
col4.markdown(f"** {fully_vacc*100/201909:.1f}% ** (of 201'909)")


df_last_week = df_vacc.iloc[:8, :]
st.subheader("Vaccinated/day for last 8 days")
fig, ax = vaccination_lc(
    df_last_week["datum"], df_last_week["im_impfzentrum_verabreichte_impfungen_pro_tag"]
)
day_fmt = mdates.DateFormatter('%A')
ax.xaxis.set_major_formatter(day_fmt)
st.write(fig)

st.subheader("Vaccinated/day since start")
fig, ax = vaccination_lc(
    df_vacc["datum"], df_vacc["im_impfzentrum_verabreichte_impfungen_pro_tag"]
)
st.pyplot(fig)


source_link = "Source: [Open Data Basel](https://data.bs.ch/), created by [Joshy](https://www.linkedin.com/in/joshy-cyriac-4089482/)"
st.markdown(source_link, unsafe_allow_html=True)
