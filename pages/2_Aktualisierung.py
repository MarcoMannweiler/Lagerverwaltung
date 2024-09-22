import streamlit as st
import pandas as pd
from datetime import date

from functions.apply_filters import apply_filters
from functions.get_dataframe import get_dataframe
from functions.make_filter import make_filter_options

dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)

######################## Produkt aktualisieren - Filter #####################################
##############################      Start     ###############################################

st.header("Produkt suchen und aktualisieren")
st.subheader("Filteroptionen")

# Initialisierung der Session State Filter Variablen, falls sie noch nicht existieren
if 'selected_brand' not in st.session_state:
    st.session_state.selected_brand = ""
if 'selected_typ' not in st.session_state:
    st.session_state.selected_typ = ""
if 'selected_serie' not in st.session_state:
    st.session_state.selected_serie = ""
if 'selected_set' not in st.session_state:
    st.session_state.selected_set = ""
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = ""
if 'selected_edition' not in st.session_state:
    st.session_state.selected_edition = ""
if 'selected_definition' not in st.session_state:
    st.session_state.selected_definition = ""
if 'selected_psa' not in st.session_state:
    st.session_state.selected_psa = ""

# Clear Filter Button prüfen und Session-State-Filter zurücksetzen
if st.button("Clear Filter"):
    st.session_state.selected_brand = ""
    st.session_state.selected_typ = ""
    st.session_state.selected_serie = ""
    st.session_state.selected_set = ""
    st.session_state.selected_language = ""
    st.session_state.selected_edition = ""
    st.session_state.selected_definition = ""
    st.session_state.selected_psa = ""

# Filter-Optionen in vier Spalten auf der Hauptseite
col1, col2, col3, col4 = st.columns(4)

# Die Filter-Widgets anzeigen, wobei der Zustand aus dem Session-State verwendet wird
with col1:
    selected_brand = st.selectbox("Marke", [""] + sorted(df["Brand"].unique()), index=0, key="selected_brand")
    selected_serie = st.selectbox("Serie", [""] + sorted(df["Serie"].unique()), index=0, key="selected_serie")

with col2:
    selected_typ = st.selectbox("Typ", [""] + sorted(df["Typ"].unique()), index=0, key="selected_typ")
    selected_set = st.selectbox("Set", [""] + sorted(df["Set"].unique()), index=0, key="selected_set")

with col3:
    selected_language = st.selectbox("Sprache", [""] + sorted(df["Language"].unique()), index=0, key="selected_language")
    selected_edition = st.selectbox("Edition", [""] + sorted(df["Edition"].unique()), index=0, key="selected_edition")

with col4:
    selected_definition = st.selectbox("Definition", [""] + sorted(df["Definition"].unique()), index=0, key="selected_definition")
    selected_psa = st.selectbox("PSA", [""] + sorted(df["PSA"].unique()), index=0, key="selected_psa")

# Anwenden der Filter auf den DataFrame
filtered_df = apply_filters(df, selected_brand, selected_typ, selected_serie, selected_set, selected_language, selected_edition, selected_definition, selected_psa)

# Anzeige des gefilterten DataFrames
st.header("Liste des Lagerbestands")
st.write("Alle outdated Zeilen (1), alle Ausbuchungen (2) und alle Zeilen mit Menge 0 (3) sind ausgeblendet, da diese nicht aktualisiert werden können - sie sind nicht auf Lager")

filtered_df = filtered_df[
    (filtered_df['Status'].str.contains(r'^current', case=False, na=False)) &  # Status enthält 'current'
    (filtered_df['Amount'] != 0) &  # Amount ist nicht gleich 0
    (~filtered_df['Vorgang'].str.contains('Ausbuchung', case=False, na=False))  # Vorgang enthält nicht 'Ausbuchung'
]

st.dataframe(filtered_df)

# Auswahl einer Zeile aus dem gefilterten DataFrame
if not filtered_df.empty:
    selected_index = st.selectbox("Wählen Sie eine Zeile zum Aktualisieren", filtered_df.index)
    selected_row = filtered_df.loc[selected_index]

    # Neue Werte für das Datum und den aktuellen Wert pro Einheit
    new_date = st.date_input("Neues Datum", date.today())
    new_current_value = st.number_input("Neuer aktueller Wert pro Einheit", min_value=0.0, step=0.01,
                                        value=float(selected_row["Current value per unit"]))

    # Button zum Aktualisieren
    if st.button("Produkt aktualisieren"):
        # Alte Zeile aktualisieren (Status auf "outdated")
        df.at[selected_index, "Status"] = f"outdated-{new_date}"

        # Neue Zeile erstellen (Status auf "current")
        new_row = selected_row.copy()
        new_row["Date"] = new_date
        new_row["Current value per unit"] = new_current_value
        new_row["Status"] = f"current-{new_date}"
        new_row["Vorgang"] = f"Aktualisierung"
        new_row["Gesamtpreis current value"] = filtered_df.loc[selected_index, 'Amount'] * new_current_value

        # Neue Zeile zum DataFrame hinzufügen
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # DataFrame in CSV-Datei speichern
        df.to_csv(dateipfad+name, index=False)
        st.success("Das Produkt wurde erfolgreich aktualisiert.")

# Aktuellen DataFrame anzeigen
st.header("Aktualisiertes Logbuch")
st.dataframe(df)

######################## Produkt aktualisieren - Filter #####################################
##############################      Ende     ###############################################
