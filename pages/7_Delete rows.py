import streamlit as st
import pandas as pd
from functions.get_dataframe import get_dataframe

# Datei und Pfad des Datensatzes
dateipfad = "data/"
name = "inventory.csv"

# Lade den DataFrame, wenn er nicht bereits in session_state ist
if 'df_original' not in st.session_state:
    st.session_state.df_original = get_dataframe(dateipfad=dateipfad, name=name)

# Erstelle eine 'id'-Spalte, wenn nicht vorhanden
if 'id' not in st.session_state.df_original.columns:
    st.session_state.df_original.reset_index(drop=True, inplace=True)
    st.session_state.df_original['id'] = st.session_state.df_original.index

# Zeige den DataFrame an
st.header("Aktueller Inventar-DataFrame")
st.dataframe(st.session_state.df_original)

# Auswahl der Zeile zum Löschen
row_to_delete = st.selectbox("Zeile auswählen, die gelöscht werden soll:", st.session_state.df_original.index)

# Button zum Löschen der Zeile
if st.button("Zeile löschen"):
    if row_to_delete is not None:
        st.session_state.df_original = st.session_state.df_original.drop(row_to_delete)
        st.session_state.df_original = st.session_state.df_original.reset_index(drop=True)  # Index zurücksetzen
        st.success(f"Zeile {row_to_delete} erfolgreich gelöscht!")
    else:
        st.warning("Bitte wählen Sie eine Zeile aus, um sie zu löschen.")

# Zeige den aktualisierten DataFrame nach dem Löschen
st.write("Aktualisierter DataFrame nach Löschen:")
st.dataframe(st.session_state.df_original)

# Button zum Speichern der Änderungen
if st.button("Änderungen speichern"):
    # Geänderten DataFrame in CSV speichern
    st.session_state.df_original.to_csv(dateipfad + name, index=False)
    st.success(f"Änderungen wurden erfolgreich in {name} gespeichert!")

# Hinweis: Bei Änderungen am DataFrame wird die Ansicht aktualisiert
