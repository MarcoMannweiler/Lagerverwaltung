import streamlit as st
import pandas as pd
from datetime import date
from functions.get_dataframe import get_dataframe

dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)

######################## Neues Produkt anlegen #####################################
############################## Start ###############################################
st.header("Logbuch")

placeholder = st.empty()

# Formular auf der Hauptseite mit drei Spalten
with st.form(key='Form1', clear_on_submit=True):
    st.header("Neues Produkt einbuchen")

    # Drei Spalten für die Eingabefelder
    col1, col2, col3 = st.columns(3)

    # Eingabefelder in den jeweiligen Spalten
    with col1:
        date_input = st.date_input("Datum", date.today())
        storage_location = st.text_input("Lagerort")
        brand = st.text_input("Marke")
        typ = st.selectbox("Typ", ["Card", "Booster Pack", "Booster Box", "Case", "ETB", "Collection Box"])

    with col2:
        serie = st.text_input("Serie")
        set_name = st.text_input("Set")
        language = st.text_input("Sprache")
        edition = st.text_input("Edition")

    with col3:
        definition = st.text_input("Definition")
        psa = st.text_input("PSA")
        amount = st.number_input("Menge", min_value=1, step=1)
        price_per_unit = st.number_input("Preis pro Einheit (inkl. MWST)", min_value=0.0, step=0.01)
        current_value = st.number_input("Aktueller Wert pro Einheit", min_value=0.0, step=0.01)

    # Berechnungen
    gesamtpreispaid = amount * price_per_unit
    gesamtpreiscurrent = amount * current_value

    # Button zum Speichern der Eingabe
    submit_button = st.form_submit_button("Eingabe speichern")

    if submit_button:
        # Neue Zeile mit den eingegebenen Daten erstellen
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
            "Gesamtpreis paid": [gesamtpreispaid],
            "Gesamtpreis current value": [gesamtpreiscurrent],
            "Status": [f"current-{date.today()}"]
        })

        # Neue Zeile zum DataFrame hinzufügen
        df = pd.concat([df, new_row], ignore_index=True)

        # Aktualisierten DataFrame anzeigen
        with placeholder.container():
            st.dataframe(df)

        # DataFrame in CSV-Datei speichern
        df.to_csv(dateipfad + name, index=False)
        st.success("Die Eingabe wurde gespeichert.")

######################## Neues Produkt anlegen #####################################
############################## Ende ###############################################
