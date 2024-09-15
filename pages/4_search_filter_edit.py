import streamlit as st
import pandas as pd
from functions.get_dataframe import get_dataframe
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

# Datei und Pfad des Datensatzes
dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)

# Suchfunktion für den DataFrame
st.header("Suche im Inventar")
search_query = st.text_input("Suchbegriff eingeben")

# Filtere den DataFrame basierend auf der Suchanfrage
if search_query:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.write(f"Suchergebnisse für '{search_query}':")
else:
    filtered_df = df

# AG-Grid Konfiguration erstellen
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination(paginationAutoPageSize=True)  # Optional: Pagination aktivieren
gb.configure_side_bar()  # Optional: Sidebar für Filteroptionen
gb.configure_default_column(editable=True)  # Alle Spalten als editierbar markieren

# Grid-Optionen festlegen
grid_options = gb.build()

# AG-Grid Komponente anzeigen
grid_response = AgGrid(
    filtered_df,
    gridOptions=grid_options,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,  # Nur gefilterte/sortierte Daten zurückgeben
    update_mode=GridUpdateMode.MODEL_CHANGED,  # Daten bei Änderungen aktualisieren
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=True,  # Optional: Erweiterte Features aktivieren
)

# Aktualisierter DataFrame
updated_df = pd.DataFrame(grid_response['data'])

# Ausgabe des aktualisierten Datensatzes (optional)
# st.write("Aktualisierter Datensatz:")
# st.dataframe(updated_df)

# Button, um Änderungen zu speichern
if st.button("Änderungen speichern"):
    # Geänderten DataFrame in CSV speichern
    updated_df.to_csv(dateipfad + name, index=False)
    st.success(f"Änderungen wurden erfolgreich in {name} gespeichert!")
