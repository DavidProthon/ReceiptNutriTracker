import streamlit as st
import pandas as pd

from process_data import ProcessData
from graph_generator import GraphGenerator

#TODO 
#move processing from data_preparation to the data_processing module

@st.cache_data
def data_preparation():
    df = ProcessData().get_df_amount_of_food_page()
    if df.empty:
        return df
    
    df["Datum_nákupu"] = pd.to_datetime(df["Datum_nákupu"])
    df["Měsíc"] = df["Datum_nákupu"].dt.to_period("M")

    df = ProcessData.add_number_of_days_in_month(df)

    return df

df = data_preparation()

if not df.empty:
    df_unique = df["Druh_potraviny"].unique()
    selected_items = st.multiselect("Vyberte položky", df_unique)

    def first_chart(df,selected_items):
        chart = GraphGenerator(df)
        df,new_columns = ProcessData.get_quantity_of_selected_type(df,selected_items)
        fig = chart.show_bar_chart(new_columns,fontsize=12)
        st.pyplot(fig)

    first_chart(df,selected_items)

else:
    st.write("Data nenalezena! Nejprve přejdi na stránku 'Zpracování účtenek' a nech si zpracovat účtenky.")
    st.write("Poté vpravo nahoře rozklikni tři tečky a zmáčkni 'Clear cache'")

