import px
import streamlit as st
import pandas as pd
import os
from datetime import date
from st_pages import add_page_title, get_nav_from_toml
from functions.get_dataframe import get_dataframe

dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)


# Interaktiver Plot - Gestapeltes Balkendiagramm
st.header("Interaktiver gestapelter Balkendiagramm")

# Auswahl der Spalten für die Achsen
x_column = st.selectbox("Wählen Sie die Spalte für die X-Achse", df.columns, index=9)  # Standardmäßig 'Amount'
color_column = st.selectbox("Wählen Sie die Spalte für die Farbgruppierung", df.columns, index=3)  # Standardmäßig 'Typ'

# Erstellen des gestapelten Balkendiagramms
fig = px.bar(df,
             x=x_column,
             y='Storage location',
             color=color_column,
             orientation='h',  # Horizontaler Balken
             title="Gestapeltes Balkendiagramm des Inventars")

st.plotly_chart(fig)