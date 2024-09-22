import plotly.express as px
import streamlit as st
import pandas as pd
import os
from datetime import date
from st_pages import add_page_title, get_nav_from_toml
from functions.get_dataframe import get_dataframe

dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)

st.title('Lagerbestand nach Marken')

# Kombinieren der Spalten in eine neue Spalte für den Plot
df['Combination'] = df[['Brand', 'Typ', 'Serie', 'Set', 'Language', 'Edition', 'Definition', 'PSA']].agg('-'.join, axis=1)

# Aggregiere die Amounts nach den eindeutigen Kombinationen
agg_df = df.groupby('Combination', as_index=False)['Amount'].sum()


# Erstellen eines vertikalen Balkendiagramms mit Plotly
fig = px.bar(agg_df,
             x='Combination',
             y='Amount',
             title='',
             labels={'Amount': 'Amount', 'Combination': 'Kombination'},
             color='Amount')

# Plotly-Diagramm anzeigen
st.plotly_chart(fig)



st.title('Lagerbestand einer jeweiligen Marke')

# Dropdown zur Auswahl der Brand-Spalte
selected_brand = st.selectbox('Wähle eine Brand aus', df['Brand'].unique())

# Daten für die ausgewählte Brand filtern
filtered_df = df[df['Brand'] == selected_brand]

# Erstellen eines horizontalen Balkendiagramms mit Plotly
fig = px.bar(filtered_df,
             x='Amount',
             y='Serie',
             orientation='h',  # Horizontal ausgerichtet
             title=f'Amount nach Serie für {selected_brand}',
             labels={'Amount': 'Amount', 'Serie': 'Serie'})

# Plotly-Diagramm anzeigen
st.plotly_chart(fig)




st.header("Liste des Lagerbestands")
st.write("Alle outdated Zeilen (1), alle Ausbuchungen (2) und alle Zeilen mit Menge 0 (3) sind ausgeblendet, da diese nicht mehr ausgebucht werden können - sie sind nicht auf Lager")

filtered_df = df[
    (df['Status'].str.contains(r'^current', case=False, na=False)) &  # Status enthält 'current'
    (df['Amount'] != 0) &  # Amount ist nicht gleich 0
    (~df['Vorgang'].str.contains('Ausbuchung', case=False, na=False))  # Vorgang enthält nicht 'Ausbuchung'
]

st.dataframe(filtered_df)

