import streamlit as st
import pandas as pd
import plotly.express as px
from functions.get_dataframe import get_dataframe

# Lade den DataFrame
dateipfad = "data/"
name = "inventory.csv"
df = get_dataframe(dateipfad=dateipfad, name=name)

if df.empty:
    st.error("Der DataFrame ist leer. Bitte überprüfen Sie die Datenquelle.")
else:
    #Konvertiere die 'Date'-Spalte in datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Bestimme den minimalen und maximalen Zeitraum und konvertiere in datetime.date
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()

    # Schieberegler für Start- und Enddatum
    start_date = st.slider("Startdatum", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.slider("Enddatum", min_value=min_date, max_value=max_date, value=max_date)

    # Sicherstellen, dass das Enddatum nicht vor dem Startdatum liegt
    if start_date > end_date:
        st.error("Das Enddatum darf nicht vor dem Startdatum liegen.")
    else:
        # Konvertiere die Schieberegler-Auswahl zurück in pd.Timestamp
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        # Filtere den DataFrame basierend auf den ausgewählten Daten für den Balkendiagramm
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
        ausbuchung_df["Umsatz"]=-1*ausbuchung_df["Gesamtpreis current value"]
        # Scatterplot: "Gesamtpreis paid" nach "Date" und "Brand"
        if not ausbuchung_df.empty:
            scatter_fig = px.scatter(ausbuchung_df,
                                    x='Date',
                                    y="Umsatz",
                                    color='Brand',
                                    title="Gesamtpreis current value nach Datum (Alles was ausgebucht wurde)",
                                    labels={'Gesamtpreis current value': 'Gesamtpreis current value', 'Date': 'Datum', 'Brand': 'Marke'},
                                    hover_name='Brand', # optional: Zeigt den Markennamen beim Hover an
                                    size_max=60) # optional: Maximale Größe der Punkte

            # Scatterplot in Streamlit anzeigen
            st.plotly_chart(scatter_fig)
        else:
            st.write("Keine Daten für den Vorgang 'Ausbuchung'.")
