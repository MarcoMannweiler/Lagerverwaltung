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

# Sidebar zum Filtern
st.sidebar.header("Produkt suchen und aktualisieren")
st.sidebar.subheader("Filteroptionen")

# Filter-Optionen zur Einschränkung der Suche
# Zustände für die Filter speichern
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

# Filter-Optionen zur Einschränkung der Suche
selected_brand,selected_typ,selected_serie,selected_set,selected_language,selected_edition,selected_definition,selected_psa = make_filter_options(df=df)

# Anwenden der Filter auf den DataFrame
filtered_df = apply_filters(df, selected_brand, selected_typ, selected_serie, selected_set, selected_language, selected_edition, selected_definition, selected_psa)


# Clear Filter Button
if st.sidebar.button("Clear Filter"):
    st.session_state.selected_brand = ""
    st.session_state.selected_typ = ""
    st.session_state.selected_serie = ""
    st.session_state.selected_set = ""
    st.session_state.selected_language = ""
    st.session_state.selected_edition = ""
    st.session_state.selected_definition = ""
    st.session_state.selected_psa = ""
    # Reset filtered_df to the original DataFrame
    filtered_df = df.copy()


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
    new_date = st.sidebar.date_input("Neues Datum", date.today())
    new_current_value = st.sidebar.number_input("Neuer aktueller Wert pro Einheit", min_value=0.0, step=0.01,
                                                value=float(selected_row["Current value per unit"]))

    # Button zum Aktualisieren
    if st.sidebar.button("Produkt aktualisieren"):
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