import streamlit as st
import pandas as pd
import os
from datetime import date
from st_pages import add_page_title, get_nav_from_toml
from functions.get_dataframe import get_dataframe

dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)


# Filterung der Zeilen nach Status und Vorgang
filtered_df_gesamtpaid = df[(df['Status'].str.contains('current*')) &
                 (df['Vorgang'].isin(['Einbuchung', 'Aktualisierung']))]

# Berechnung der Summe der Spalte "Gesamtpreis paid"
summe_gesamtpaid = filtered_df_gesamtpaid['Gesamtpreis paid'].sum()

st.write(f"Die Summe beträgt: {summe_gesamtpaid}")


# Filterung der Zeilen nach Status und Vorgang - Ausbuchung
filtered_df_gesamtsold = df[(df['Status'].str.contains('current*')) &
                 (df['Vorgang'].isin(['Ausbuchung']))]

# Berechnung der Summe der Spalte "Gesamtpreis paid"
summe_gesamtsold = filtered_df_gesamtsold['Gesamtpreis current value'].sum()

st.write(f"Die Summe beträgt: {summe_gesamtsold}")
