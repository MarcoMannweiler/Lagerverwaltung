import os
import pandas as pd


def get_dataframe(dateipfad, name):
    # Verzeichnis erstellen, falls es noch nicht existiert
    if not os.path.exists(dateipfad):
        os.makedirs(dateipfad)

    # Pfad zur CSV-Datei
    csv_file_path = os.path.join(dateipfad, name)

    # Überprüfen, ob die Datei existiert und laden oder neuen DataFrame erstellen
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
    else:
        df = pd.DataFrame(columns=["Date", "Storage location", "Brand", "Typ", "Serie", "Set", "Language",
                                   "Edition", "Definition", "PSA", "Amount",
                                   "Price paid per unit (incl. MWST)", "Current value per unit", "Vorgang",
                                   "Gesamtpreis paid", "Gesamtpreis current value", "Status"])

    return df
