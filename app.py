import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Filtruj i pobierz CSV", layout="wide")

st.title("Filtrowanie ofert Allegro")

uploaded_file = st.file_uploader("Wgraj plik CSV", type=["csv"])

if uploaded_file is not None:
    # Wczytanie pliku
    df = pd.read_csv(uploaded_file, dtype=str, sep=',')

    # Wyświetlenie kolumn, by użytkownik mógł się upewnić
    st.write("Podgląd danych:")
    st.dataframe(df.head())

    # Sprawdzenie, czy kolumny istnieją
    if "kategoria_główna" in df.columns and "podkategoria" in df.columns:
        # Filtry
        selected_main = st.multiselect("Wybierz Kategorię główną", sorted(df["kategoria_główna"].dropna().unique()))
        selected_sub = st.multiselect("Wybierz Podkategorię", sorted(df["podkategoria"].dropna().unique()))

        filtered_df = df.copy()
        if selected_main:
            filtered_df = filtered_df[filtered_df["kategoria_główna"].isin(selected_main)]
        if selected_sub:
            filtered_df = filtered_df[filtered_df["podkategoria"].isin(selected_sub)]

        st.write(f"Znaleziono {len(filtered_df)} wierszy po filtrowaniu.")

        # Podgląd filtrowanych danych
        st.dataframe(filtered_df)

        # Pobieranie CSV
        csv_buffer = StringIO()
        filtered_df.to_csv(csv_buffer, index=False, sep=',', encoding='utf-8-sig')
        st.download_button(
            label="📥 Pobierz przefiltrowany CSV",
            data=csv_buffer.getvalue(),
            file_name="przefiltrowane_oferty.csv",
            mime="text/csv"
        )
    else:
        st.error("Plik nie zawiera kolumn 'kategoria_główna' i 'podkategoria'.")
