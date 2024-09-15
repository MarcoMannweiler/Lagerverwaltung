import streamlit as st
import pandas as pd
import plotly.express as px
from functions.get_dataframe import get_dataframe

# Lade den DataFrame
dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)

# Filterung der Zeilen nach Status und Vorgang für Gesamtpreis paid
filtered_df_gesamtpaid = df[(df['Status'].str.contains('current*')) &
                            (df['Vorgang'].isin(['Einbuchung', 'Aktualisierung']))]

# Berechnung der Summe der Spalte "Gesamtpreis paid"
summe_gesamtpaid = filtered_df_gesamtpaid['Gesamtpreis paid'].sum()

# Filterung der Zeilen nach Status und Vorgang für Gesamtpreis sold
filtered_df_gesamtsold = df[(df['Status'].str.contains('current*')) &
                            (df['Vorgang'].isin(['Ausbuchung']))]

# Berechnung der Summe der Spalte "Gesamtpreis current value" (sold)
summe_gesamtsold = filtered_df_gesamtsold['Gesamtpreis current value'].sum()

# Anzeige der Summen
#st.write(f"Die Gesamtsumme der bezahlten Preise beträgt: {summe_gesamtpaid}")
#st.write(f"Die Gesamtsumme der verkauften Preise beträgt: {summe_gesamtsold}")

# Berechnung der Summen nach "Brand" für paid und sold
summe_paid_by_brand = filtered_df_gesamtpaid.groupby('Brand')['Gesamtpreis paid'].sum().reset_index()
summe_sold_by_brand = filtered_df_gesamtsold.groupby('Brand')['Gesamtpreis current value'].sum().reset_index()

# Zusammenführen der Datenframes für die Darstellung
merged_df = pd.merge(summe_paid_by_brand, summe_sold_by_brand, on="Brand", how="outer").fillna(0)

# Umbenennen der Spalten für bessere Lesbarkeit
merged_df.columns = ['Brand', 'Gesamtpreis paid', 'Gesamtpreis sold']

# Hinzufügen einer Zeile für die Gesamtsummen am Anfang des DataFrames
gesamt_df = pd.DataFrame({'Brand': ['Gesamt'],
                          'Gesamtpreis paid': [summe_gesamtpaid],
                          'Gesamtpreis sold': [summe_gesamtsold]})

# Gesamtsummen am Anfang einfügen
merged_df = pd.concat([gesamt_df, merged_df], ignore_index=True)

# Plotten des horizontalen Balkendiagramms
fig = px.bar(merged_df,
             x=['Gesamtpreis paid', 'Gesamtpreis sold'],
             y='Brand',
             orientation='h',
             title="Gesamtpreis Paid und Sold nach Brand (inkl. Gesamtsumme)",
             labels={'value': 'Gesamtpreis', 'Brand': 'Marke'})

# Plot in Streamlit anzeigen
st.plotly_chart(fig)














#####
######
###
####
###


# import streamlit as st
# import pandas as pd
# import os
# from datetime import date
# from st_pages import add_page_title, get_nav_from_toml
# from functions.get_dataframe import get_dataframe
#
# dateipfad = "data/"
# name = "inventory.csv"
# df = get_dataframe(dateipfad=dateipfad, name=name)
#
#
# # Filterung der Zeilen nach Status und Vorgang
# filtered_df_gesamtpaid = df[(df['Status'].str.contains('current*')) &
#                  (df['Vorgang'].isin(['Einbuchung', 'Aktualisierung']))]
#
# # Berechnung der Summe der Spalte "Gesamtpreis paid"
# summe_gesamtpaid = filtered_df_gesamtpaid['Gesamtpreis paid'].sum()
#
# st.write(f"Die Summe beträgt: {summe_gesamtpaid}")
#
#
# # Filterung der Zeilen nach Status und Vorgang - Ausbuchung
# filtered_df_gesamtsold = df[(df['Status'].str.contains('current*')) &
#                  (df['Vorgang'].isin(['Ausbuchung']))]
#
# # Berechnung der Summe der Spalte "Gesamtpreis paid"
# summe_gesamtsold = filtered_df_gesamtsold['Gesamtpreis current value'].sum()
#
# st.write(f"Die Summe beträgt: {summe_gesamtsold}")

