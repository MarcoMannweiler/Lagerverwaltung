import streamlit as st
import pandas as pd
import os
from datetime import date
from st_pages import add_page_title, get_nav_from_toml
from functions.get_dataframe import get_dataframe

dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)

######################## Neues Produkt anlegen #####################################
############################## Start ###############################################
st.header("Logbuch")

placeholder = st.empty()


# DataFrame initial anzeigen
with placeholder.container():
    st.dataframe(df)

# Sidebar zur Eingabe der Daten - Produkt anlegen - Einbuchung
st.sidebar.header("Neues Produkt einbuchen")
date_input = st.sidebar.date_input("Datum", date.today())
storage_location = st.sidebar.text_input("Lagerort")
brand = st.sidebar.text_input("Marke")
typ = st.sidebar.selectbox("Typ", ["Card", "Booster Pack", "Booster Box", "Case", "ETB", "Collection Box"])
serie = st.sidebar.text_input("Serie")
set_name = st.sidebar.text_input("Set")
language = st.sidebar.text_input("Sprache")
edition = st.sidebar.text_input("Edition")
definition = st.sidebar.text_input("Definition")
psa = st.sidebar.text_input("PSA")
amount = st.sidebar.number_input("Menge", min_value=1, step=1)
price_per_unit = st.sidebar.number_input("Preis pro Einheit (inkl. MWST)", min_value=0.0, step=0.01)
current_value = st.sidebar.number_input("Aktueller Wert pro Einheit", min_value=0.0, step=0.01)

#errechnete Variablen aus den Eingaben - Gesamtpreise
gesamtpreispaid = amount * price_per_unit
gesamtpreiscurrent = amount * current_value


date = date.today()

# Button zum Speichern der Eingabe
if st.sidebar.button("Eingabe speichern"):
    # Neue Zeile mit den eingegebenen Daten erstellen, inklusive "Vorgang" = "Einbuchung"
    new_row = pd.DataFrame({
        "Date": [date_input],
        "Vorgang": ["Einbuchung"],  # Wert für Einbuchung setzen
        "Storage location": [storage_location],
        "Brand": [brand],
        "Typ": [typ],
        "Serie": [serie],
        "Set": [set_name],
        "Language": [language],
        "Edition": [edition],
        "Definition": [definition],
        "PSA": [psa],
        "Amount": [amount],
        "Price paid per unit (incl. MWST)": [price_per_unit],
        "Current value per unit": [current_value],
        "Gesamtpreis paid":[gesamtpreispaid],
        "Gesamtpreis current value": [gesamtpreiscurrent],
        "Status": [f"current-{date}"]

    })

    # Neue Zeile zum DataFrame hinzufügen
    df = pd.concat([df, new_row], ignore_index=True)

    with placeholder.container():
        st.dataframe(df)


    # DataFrame in CSV-Datei speichern
    df.to_csv(dateipfad+name, index=False)
    st.success("Die Eingabe wurde gespeichert.")

######################## Neues Produkt anlegen #####################################
############################## Ende ###############################################