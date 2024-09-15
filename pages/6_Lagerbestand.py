import streamlit as st
import pandas as pd
import os
from datetime import date
from st_pages import add_page_title, get_nav_from_toml
from functions.get_dataframe import get_dataframe

dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)

st.header("Gefilterte Inventarliste OHNE outdated Vorgänge")
st.write("alle outdated Zeilen sind ausgeblendet, da diese nicht mehr aktualisiert oder ausgebucht werden können - bei jeder Aktualisierung oder Ausbuchung werden neue Zeilen mit current-date erstellt. Somit gibt es keine Doppelungen in den Mengen, aber alle Einbuchungen, alle Preisaktualisierungen und alle Ausbuchungen sind aufgeführt.")

st.dataframe(df[df['Status'].str.contains(r'^current', case=False, na=False)])
