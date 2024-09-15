import streamlit as st
import pandas as pd
from functions.get_dataframe import get_dataframe
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

# Datei und Pfad des Datensatzes
dateipfad = "data/"
name = "inventory.csv"
df_original = get_dataframe(dateipfad=dateipfad, name=name)  # Original DataFrame laden

# Ensure there is a unique identifier for each row (if not present, create one)
if 'id' not in df_original.columns:
    df_original.reset_index(drop=True, inplace=True)
    df_original['id'] = df_original.index

# Suchfunktion für den DataFrame
st.header("Suche im Inventar")
search_query = st.text_input("Suchbegriff eingeben")

# Filtere den DataFrame basierend auf der Suchanfrage
if search_query:
    filtered_df = df_original[df_original.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.write(f"Suchergebnisse für '{search_query}':")
else:
    filtered_df = df_original

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

# Ensure the 'id' column is in the updated DataFrame
if 'id' not in updated_df.columns:
    updated_df['id'] = updated_df.index

# Merge updated_df into df_original based on 'id'
df_merged = df_original.merge(updated_df, on='id', suffixes=('', '_updated'), how='left')

# Update original DataFrame with changes from updated DataFrame
for col in df_original.columns:
    if col != 'id':
        df_merged[col] = df_merged[f"{col}_updated"].combine_first(df_merged[col])

# Drop columns from the merge that are not needed anymore
df_original_updated = df_merged[df_original.columns]
df_original_updated = df_original_updated.drop(columns=['id'])

# Ausgabe des aktualisierten Datensatzes (optional)
st.write("Aktualisierter Datensatz:")
st.dataframe(df_original_updated)

# Button, um Änderungen zu speichern
if st.button("Änderungen speichern"):
    # Geänderten DataFrame in CSV speichern
    df_original_updated.to_csv(dateipfad + name, index=False)
    st.success(f"Änderungen wurden erfolgreich in {name} gespeichert!")
