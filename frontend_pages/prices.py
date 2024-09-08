import streamlit as st
import pandas as pd

from process_data import ProcessData
from graph_generator import GraphGenerator

#TODO
#add more filters, it's really a pain to find the right item
#Add a graph of the total spending for each month

@st.cache_data
def data_preparation():
    df = ProcessData().get_df_prices_page()
    if df.empty:
        return df
        
    df["Datum_nákupu"] = pd.to_datetime(df["Datum_nákupu"])

    return df

df = data_preparation()

if not df.empty:

    df_unique = df["Položka"].unique()
    selected_items = st.multiselect("Vyberte_položky", df_unique)

    def first_chart(df):
        chart = GraphGenerator(df)
        chart.select_required_items(selected_items)
        fig = chart.show_line_chart("Cena","Cena_za_položku_Kč]")
        st.pyplot(fig)

    def second_chart(df):
        chart = GraphGenerator(df)
        chart.select_required_items(selected_items)
        fig = chart.show_line_chart("Poměrová_cena","Cena_za_100g_[Kč]")
        st.pyplot(fig)

    first_chart(df)
    second_chart(df)
else:
    st.write("Data nenalezena! Nejprve přejdi na stránku 'Zpracování účtenek' a nech si zpracovat účtenky.")
    st.write("Poté vpravo nahoře rozklikni tři tečky a zmáčkni 'Clear cache'")
    
    
