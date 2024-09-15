import streamlit as st

def make_filter_options(df):
    # Create a sidebar with various selectbox options
    selected_brand = st.sidebar.selectbox("Marke", [""] + list(df["Brand"].unique()))
    selected_typ = st.sidebar.selectbox("Typ", ["", "Card", "Booster Pack", "Booster Box", "Case", "ETB", "Collection Box"])
    selected_serie = st.sidebar.selectbox("Serie", [""] + list(df["Serie"].unique()))
    selected_set = st.sidebar.selectbox("Set", [""] + list(df["Set"].unique()))
    selected_language = st.sidebar.selectbox("Sprache", [""] + list(df["Language"].unique()))
    selected_edition = st.sidebar.selectbox("Edition", [""] + list(df["Edition"].unique()))
    selected_definition = st.sidebar.selectbox("Definition", [""] + list(df["Definition"].unique()))
    selected_psa = st.sidebar.selectbox("PSA", [""] + list(df["PSA"].unique()))

    # Return the selected values
    return selected_brand, selected_typ, selected_serie, selected_set, selected_language, selected_edition, selected_definition, selected_psa
