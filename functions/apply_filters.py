import pandas as pd

def apply_filters(df, selected_brand, selected_typ, selected_serie, selected_set, selected_language, selected_edition, selected_definition, selected_psa):
    # Start with the original DataFrame
    filtered_df = df.copy()

    # Apply filters based on selected values
    if selected_brand:
        filtered_df = filtered_df[filtered_df["Brand"].str.contains(selected_brand, case=False, na=False)]

    if selected_typ:
        filtered_df = filtered_df[filtered_df["Typ"] == selected_typ]

    if selected_serie:
        filtered_df = filtered_df[filtered_df["Serie"].str.contains(selected_serie, case=False, na=False)]

    if selected_set:
        filtered_df = filtered_df[filtered_df["Set"].str.contains(selected_set, case=False, na=False)]

    if selected_language:
        filtered_df = filtered_df[filtered_df["Language"].str.contains(selected_language, case=False, na=False)]

    if selected_edition:
        filtered_df = filtered_df[filtered_df["Edition"].str.contains(selected_edition, case=False, na=False)]

    if selected_definition:
        filtered_df = filtered_df[filtered_df["Definition"].str.contains(selected_definition, case=False, na=False)]

    if selected_psa:
        filtered_df = filtered_df[filtered_df["PSA"].str.contains(selected_psa, case=False, na=False)]

    return filtered_df