import streamlit as st
import pandas as pd
import plotly.express as px
from functions.get_dataframe import get_dataframe

# Lade den DataFrame
dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)

# Versuche, die 'Date'-Spalte in gültige Datumswerte zu konvertieren, ungültige Einträge werden zu NaT
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Überprüfe, ob es ungültige Datumswerte (NaT) gibt und zeige eine Warnung an
if df['Date'].isna().sum() > 0:
    st.warning(f"Es wurden {df['Date'].isna().sum()} ungültige Datumswerte gefunden. Diese werden ignoriert.")
    # Entferne Zeilen mit ungültigen Datumswerten (NaT)
    df = df.dropna(subset=['Date'])


# Bestimme die eindeutigen, gültigen Datumswerte und sortiere sie
unique_dates = df['Date'].dt.date.unique()
unique_dates.sort()

# Überprüfe, ob es überhaupt noch Datumswerte gibt, nachdem ungültige entfernt wurden
if len(unique_dates) == 0:
    st.error("Keine gültigen Datumswerte im DataFrame gefunden.")
else:
    # Verwende einen select_slider für Start- und Enddatum, wenn Daten vorhanden sind
    start_date = st.select_slider("Startdatum", options=unique_dates, value=unique_dates[0])
    end_date = st.select_slider("Enddatum", options=unique_dates, value=unique_dates[-1])

    # Sicherstellen, dass das Enddatum nicht vor dem Startdatum liegt
    if start_date > end_date:
        st.error("Das Enddatum darf nicht vor dem Startdatum liegen.")
    else:
        # Konvertiere die ausgewählten Daten zurück in pd.Timestamp
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        # Filtere den DataFrame basierend auf den ausgewählten Daten für das Balkendiagramm
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Filterung der Zeilen nach Status und Vorgang für Gesamtpreis paid
        filtered_df_gesamtpaid = filtered_df[(filtered_df['Status'].str.contains('current*')) &
                                             (filtered_df['Vorgang'].isin(['Einbuchung', 'Aktualisierung']))]

        # Berechnung der Summe der Spalte "Gesamtpreis paid"
        summe_gesamtpaid = filtered_df_gesamtpaid['Gesamtpreis paid'].sum()

        # Filterung der Zeilen nach Status und Vorgang für Gesamtpreis sold
        filtered_df_gesamtsold = filtered_df[(df['Status'].str.contains('current*')) &
                                             (df['Vorgang'].isin(['Ausbuchung']))]

        # Berechnung der Summe der Spalte "Gesamtpreis current value" (sold)
        summe_gesamtsold = filtered_df_gesamtsold['Gesamtpreis current value'].sum()

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
        bar_fig = px.bar(merged_df,
                         x=['Gesamtpreis paid', 'Gesamtpreis sold'],
                         y='Brand',
                         orientation='h',
                         title="Gesamtpreis Paid und Sold nach Brand (inkl. Gesamtsumme)",
                         labels={'value': 'Gesamtpreis', 'Brand': 'Marke'})

        # Plot in Streamlit anzeigen
        st.plotly_chart(bar_fig)

        # Filterung der Zeilen für den Scatterplot: Verwende den gesamten DataFrame
        ausbuchung_df = df[df['Vorgang'] == 'Ausbuchung']
        ausbuchung_df["Umsatz"] = -1 * ausbuchung_df["Gesamtpreis current value"]

        # Scatterplot: "Gesamtpreis current value" nach "Date" und "Brand"
        if not ausbuchung_df.empty:
            scatter_fig = px.scatter(ausbuchung_df,
                                     x='Date',
                                     y="Umsatz",
                                     color='Brand',
                                     title="Gesamtpreis current value nach Datum (Alles was ausgebucht wurde)",
                                     labels={'Umsatz': 'Umsatz', 'Date': 'Datum', 'Brand': 'Marke'},
                                     hover_name='Brand',  # optional: Zeigt den Markennamen beim Hover an
                                     size_max=60)  # optional: Maximale Größe der Punkte

            # Scatterplot in Streamlit anzeigen
            st.plotly_chart(scatter_fig)
        else:
            st.write("Keine Daten für den Vorgang 'Ausbuchung'.")
