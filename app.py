import streamlit as st
import pandas as pd
import os
from datetime import date
import plotly.express as px
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide")
# Get navigation from the TOML file
nav = get_nav_from_toml("pages_sections.toml")
# Streamlit logo and title
# st.logo("images/logo.JPG")
pg = st.navigation(nav)

add_page_title(pg)
pg.run()



# # Pfad zur CSV-Datei
# csv_file_path = 'data/inventory.csv'
#
# # Überprüfen, ob die Datei existiert und laden oder neuen DataFrame erstellen
# if os.path.exists(csv_file_path):
#     df = pd.read_csv(csv_file_path)
# else:
#     df = pd.DataFrame(columns=["Date", "Storage location", "Brand", "Typ", "Serie", "Set", "Language",
#                                "Edition", "Definition", "PSA", "Amount",
#                                "Price paid per unit (incl. MWST)", "Current value per unit", "Vorgang", "Gesamtpreis paid", "Gesamtpreis current value", "Status"])
#
# ######################## Neues Produkt anlegen #####################################
# ############################## Start ###############################################
#
# # Sidebar zur Eingabe der Daten - Produkt anlegen - Einbuchung
# st.sidebar.header("Neues Produkt einbuchen")
# date_input = st.sidebar.date_input("Datum", date.today())
# storage_location = st.sidebar.text_input("Lagerort")
# brand = st.sidebar.text_input("Marke")
# typ = st.sidebar.selectbox("Typ", ["Card", "Booster Pack", "Booster Box", "Case", "ETB", "Collection Box"])
# serie = st.sidebar.text_input("Serie")
# set_name = st.sidebar.text_input("Set")
# language = st.sidebar.text_input("Sprache")
# edition = st.sidebar.text_input("Edition")
# definition = st.sidebar.text_input("Definition")
# psa = st.sidebar.text_input("PSA")
# amount = st.sidebar.number_input("Menge", min_value=1, step=1)
# price_per_unit = st.sidebar.number_input("Preis pro Einheit (inkl. MWST)", min_value=0.0, step=0.01)
# current_value = st.sidebar.number_input("Aktueller Wert pro Einheit", min_value=0.0, step=0.01)
#
# #errechnete Variablen aus den Eingaben - Gesamtpreise
# gesamtpreispaid = amount * price_per_unit
# gesamtpreiscurrent = amount * current_value
#
#
# date = date.today()
#
# # Button zum Speichern der Eingabe
# if st.sidebar.button("Eingabe speichern"):
#     # Neue Zeile mit den eingegebenen Daten erstellen, inklusive "Vorgang" = "Einbuchung"
#     new_row = pd.DataFrame({
#         "Date": [date_input],
#         "Vorgang": ["Einbuchung"],  # Wert für Einbuchung setzen
#         "Storage location": [storage_location],
#         "Brand": [brand],
#         "Typ": [typ],
#         "Serie": [serie],
#         "Set": [set_name],
#         "Language": [language],
#         "Edition": [edition],
#         "Definition": [definition],
#         "PSA": [psa],
#         "Amount": [amount],
#         "Price paid per unit (incl. MWST)": [price_per_unit],
#         "Current value per unit": [current_value],
#         "Gesamtpreis paid":[gesamtpreispaid],
#         "Gesamtpreis current value": [gesamtpreiscurrent],
#         "Status": [f"current-{date}"]
#
#     })
#
#     # Neue Zeile zum DataFrame hinzufügen
#     df = pd.concat([df, new_row], ignore_index=True)
#
#     # DataFrame in CSV-Datei speichern
#     df.to_csv(csv_file_path, index=False)
#     st.success("Die Eingabe wurde gespeichert.")
#
# ######################## Neues Produkt anlegen #####################################
# ############################## Ende ###############################################
#
#
#
# ######################## Produkt aktualisieren - Filter #####################################
# ##############################      Start     ###############################################
#
# # Sidebar zum Filtern
# st.sidebar.header("Produkt suchen und aktualisieren")
# st.sidebar.subheader("Filteroptionen")
#
# # Filter-Optionen zur Einschränkung der Suche
# # Zustände für die Filter speichern
# if 'selected_brand' not in st.session_state:
#     st.session_state.selected_brand = ""
# if 'selected_typ' not in st.session_state:
#     st.session_state.selected_typ = ""
# if 'selected_serie' not in st.session_state:
#     st.session_state.selected_serie = ""
# if 'selected_set' not in st.session_state:
#     st.session_state.selected_set = ""
# if 'selected_language' not in st.session_state:
#     st.session_state.selected_language = ""
# if 'selected_edition' not in st.session_state:
#     st.session_state.selected_edition = ""
# if 'selected_definition' not in st.session_state:
#     st.session_state.selected_definition = ""
# if 'selected_psa' not in st.session_state:
#     st.session_state.selected_psa = ""
#
#
#
# # Filter-Optionen zur Einschränkung der Suche
# selected_brand = st.sidebar.selectbox("Marke Filter", [""] + list(df["Brand"].unique()))
# selected_typ = st.sidebar.selectbox("Typ Filter", ["", "Card", "Booster Pack", "Booster Box", "Case", "ETB", "Collection Box"])
# selected_serie = st.sidebar.selectbox("Serie Filter", [""] + list(df["Serie"].unique()))
# selected_set = st.sidebar.selectbox("Set Filter", [""] + list(df["Set"].unique()))
# selected_language = st.sidebar.selectbox("Sprache Filter", [""] + list(df["Language"].unique()))
# selected_edition = st.sidebar.selectbox("Edition Filter", [""] + list(df["Edition"].unique()))
# selected_definition = st.sidebar.selectbox("Definition Filter", [""] + list(df["Definition"].unique()))
# selected_psa = st.sidebar.selectbox("PSA Filter", [""] + list(df["PSA"].unique()))
#
# # Anwenden der Filter auf den DataFrame
# filtered_df = df.copy()
#
# # Clear Filter Button
# if st.sidebar.button("Clear Filter"):
#     # st.session_state.selected_brand = ""
#     selected_brand = ""
#     filtered_df = filtered_df[filtered_df["Brand"].str.contains(selected_brand, case=False, na=False)]
#     selected_typ = ""
#     filtered_df = filtered_df[filtered_df["Typ"].str.contains(selected_brand, case=False, na=False)]
#     selected_serie = ""
#     filtered_df = filtered_df[filtered_df["Serie"].str.contains(selected_brand, case=False, na=False)]
#     selected_set = ""
#     filtered_df = filtered_df[filtered_df["Set"].str.contains(selected_brand, case=False, na=False)]
#     selected_language = ""
#     filtered_df = filtered_df[filtered_df["Language"].str.contains(selected_brand, case=False, na=False)]
#     selected_edition = ""
#     filtered_df = filtered_df[filtered_df["Edition"].str.contains(selected_brand, case=False, na=False)]
#     selected_definition = ""
#     filtered_df = filtered_df[filtered_df["Definition"].str.contains(selected_brand, case=False, na=False)]
#     selected_psa = ""
#     filtered_df = filtered_df[filtered_df["PSA"].str.contains(selected_brand, case=False, na=False)]
#
# if selected_brand:
#     filtered_df = filtered_df[filtered_df["Brand"].str.contains(selected_brand, case=False, na=False)]
#
# if selected_typ:
#     filtered_df = filtered_df[filtered_df["Typ"] == selected_typ]
#
# if selected_serie:
#     filtered_df = filtered_df[filtered_df["Serie"].str.contains(selected_serie, case=False, na=False)]
#
# if selected_set:
#     filtered_df = filtered_df[filtered_df["Set"].str.contains(selected_set, case=False, na=False)]
#
# if selected_language:
#     filtered_df = filtered_df[filtered_df["Language"].str.contains(selected_language, case=False, na=False)]
#
# if selected_edition:
#     filtered_df = filtered_df[filtered_df["Edition"].str.contains(selected_edition, case=False, na=False)]
#
# if selected_definition:
#     filtered_df = filtered_df[filtered_df["Definition"].str.contains(selected_definition, case=False, na=False)]
#
# if selected_psa:
#     filtered_df = filtered_df[filtered_df["PSA"].str.contains(selected_psa, case=False, na=False)]
#
#
#
#
# # Anzeige des gefilterten DataFrames
# st.header("Gefilterte Produkte")
# st.dataframe(filtered_df)
#
# # Auswahl einer Zeile aus dem gefilterten DataFrame
# if not filtered_df.empty:
#     selected_index = st.selectbox("Wählen Sie eine Zeile zum Aktualisieren", filtered_df.index)
#     selected_row = filtered_df.loc[selected_index]
#
#
#     # Neue Werte für das Datum und den aktuellen Wert pro Einheit
#     new_date = st.sidebar.date_input("Neues Datum", date.today())
#     new_current_value = st.sidebar.number_input("Neuer aktueller Wert pro Einheit", min_value=0.0, step=0.01,
#                                                 value=float(selected_row["Current value per unit"]))
#
#     # Button zum Aktualisieren
#     if st.sidebar.button("Produkt aktualisieren"):
#         # Alte Zeile aktualisieren (Status auf "outdated")
#         df.at[selected_index, "Status"] = f"outdated-{new_date}"
#
#         # Neue Zeile erstellen (Status auf "current")
#         new_row = selected_row.copy()
#         new_row["Date"] = new_date
#         new_row["Current value per unit"] = new_current_value
#         new_row["Status"] = f"current-{new_date}"
#         new_row["Vorgang"] = f"Aktualisierung"
#
#         # Neue Zeile zum DataFrame hinzufügen
#         df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
#
#         # DataFrame in CSV-Datei speichern
#         df.to_csv(csv_file_path, index=False)
#         st.success("Das Produkt wurde erfolgreich aktualisiert.")
#
# # Aktuellen DataFrame anzeigen
# st.header("Aktuelle Inventarliste")
# st.dataframe(df)
#
# ######################## Produkt aktualisieren - Filter #####################################
# ##############################      Ende     ###############################################
#
#
#
# # Neue Maske zur Ausbuchung
# st.sidebar.header("Produkt Ausbuchung")
# if not df.empty:
#     brands = df["Brand"].unique()
#     # Auswahl des Produkts anhand der Marke für die Ausbuchung
#     selected_brand_for_out = st.sidebar.selectbox("Wählen Sie die Marke, die ausgebucht werden soll", brands)
#
#     # Filtere die Zeilen für die ausgewählte Marke
#     brand_rows_for_out = df[df["Brand"] == selected_brand_for_out]
#
#     if not brand_rows_for_out.empty:
#         # Eingabefeld für das Datum der Ausbuchung
#         out_date_input = st.sidebar.date_input("Ausbuchungsdatum", date.today())
#
#         # Eingabefeld für die Menge der Ausbuchung
#         out_amount = st.sidebar.number_input("Auszubuchende Menge", min_value=1, step=1)
#
#         # Eingabefeld für den Preis pro Einheit (falls sich dieser ändern soll)
#         out_price_per_unit = st.sidebar.number_input("Preis pro Einheit (inkl. MWST) bei Ausbuchung", min_value=0.0,
#                                                      value=float(brand_rows_for_out.iloc[0]["Price paid per unit (incl. MWST)"]), step=0.01)
#
#         # Eingabefeld für den aktuellen Wert pro Einheit (falls sich dieser ändern soll)
#         out_current_value = st.sidebar.number_input("Aktueller Wert pro Einheit bei Ausbuchung", min_value=0.0,
#                                                     value=float(brand_rows_for_out.iloc[0]["Current value per unit"]), step=0.01)
#
#         # Button zur Durchführung der Ausbuchung
#         if st.sidebar.button("Ausbuchung durchführen"):
#             # Neue Zeile für die Ausbuchung erstellen (Menge negativ)
#             out_row = pd.DataFrame({
#                 "Date": [out_date_input],
#                 "Storage location": [brand_rows_for_out.iloc[0]["Storage location"]],
#                 "Brand": [selected_brand_for_out],
#                 "Typ": [brand_rows_for_out.iloc[0]["Typ"]],
#                 "Serie": [brand_rows_for_out.iloc[0]["Serie"]],
#                 "Set": [brand_rows_for_out.iloc[0]["Set"]],
#                 "Language": [brand_rows_for_out.iloc[0]["Language"]],
#                 "Edition": [brand_rows_for_out.iloc[0]["Edition"]],
#                 "Definition": [brand_rows_for_out.iloc[0]["Definition"]],
#                 "PSA": [brand_rows_for_out.iloc[0]["PSA"]],
#                 "Amount": [-out_amount],  # Menge negativ
#                 "Price paid per unit (incl. MWST)": [out_price_per_unit],  # Angepasster Preis bei Ausbuchung
#                 "Current value per unit": [out_current_value]  # Angepasster aktueller Wert bei Ausbuchung
#             })
#
#             # Neue Zeile zum DataFrame hinzufügen
#             df = pd.concat([df, out_row], ignore_index=True)
#
#             # DataFrame in CSV-Datei speichern
#             df.to_csv(csv_file_path, index=False)
#             st.success(f"Die Ausbuchung von {out_amount} Einheiten für {selected_brand_for_out} wurde durchgeführt.")
#
#
#
# # Interaktiver Plot - Gestapeltes Balkendiagramm
# st.header("Interaktiver gestapelter Balkendiagramm")
#
# # Auswahl der Spalten für die Achsen
# x_column = st.selectbox("Wählen Sie die Spalte für die X-Achse", df.columns, index=9)  # Standardmäßig 'Amount'
# color_column = st.selectbox("Wählen Sie die Spalte für die Farbgruppierung", df.columns, index=3)  # Standardmäßig 'Typ'
#
# # Erstellen des gestapelten Balkendiagramms
# fig = px.bar(df,
#              x=x_column,
#              y='Storage location',
#              color=color_column,
#              orientation='h',  # Horizontaler Balken
#              title="Gestapeltes Balkendiagramm des Inventars")
#
# st.plotly_chart(fig)
#
# # Suchfunktion für den DataFrame
# st.header("Suche im Inventar")
# search_query = st.text_input("Suchbegriff eingeben")
#
# if search_query:
#     search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
#     st.write(f"Suchergebnisse für '{search_query}':")
#     st.dataframe(search_results)
