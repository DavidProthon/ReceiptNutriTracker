import streamlit as st
import pandas as pd

from process_data import ProcessData
from graph_generator import GraphGenerator

#TODO
#move processing from data_preparation to the data_processing module

@st.cache_data
def data_preparation():
    df = ProcessData().get_df_macronutriens_page()
    if df.empty:
        return df
    
    df["Datum_nákupu"] = pd.to_datetime(df["Datum_nákupu"])
    df["Měsíc"] = df["Datum_nákupu"].dt.to_period("M")

    df = ProcessData.add_number_of_days_in_month(df)

    df = ProcessData.get_value_items(df,"Bílkoviny")
    df = ProcessData.get_value_items(df,"Sacharidy")
    df = ProcessData.get_value_items(df,"Cukry")
    df = ProcessData.get_value_items(df,"Tuky")
    df = ProcessData.get_value_items(df,"Nasycené_mastné_kyseliny")
    df = ProcessData.get_value_items(df,"Vláknina")
    df = ProcessData.get_value_items(df,"Sůl")

    df = ProcessData.get_complex_carbs(df)
    df = ProcessData.get_unsaturated_fatty_acids(df)

    df = ProcessData.get_value_items_in_kj(df,"Bílkoviny[g]_na_den","Bílkoviny")
    df = ProcessData.get_value_items_in_kj(df,"Komplexní_sacharidy_na_den[g]","Sacharidy")
    df = ProcessData.get_value_items_in_kj(df,"Cukry[g]_na_den","Sacharidy")
    df = ProcessData.get_value_items_in_kj(df,"Nenasycené_mastné_kyseliny_na_den[g]","Tuky")
    df = ProcessData.get_value_items_in_kj(df,"Nasycené_mastné_kyseliny[g]_na_den","Tuky")

    return df

df = data_preparation()

if not df.empty:

    def first_chart(df):
        show_columns =["Měsíc","Bílkoviny[g]_na_den","Komplexní_sacharidy_na_den[g]","Cukry[g]_na_den","Nasycené_mastné_kyseliny[g]_na_den","Nenasycené_mastné_kyseliny_na_den[g]","Vláknina[g]_na_den","Sůl[g]_na_den"]
        chart = GraphGenerator(df)
        fig = chart.show_bar_chart(show_columns, chart_name ="Průměrný příjem živin na den v jednotlivých měsících[g]")
        st.pyplot(fig)

    def second_chart(df):
        show_columns =["Měsíc","Bílkoviny[g]_na_den_[kcal]","Komplexní_sacharidy_na_den[g]_[kcal]","Cukry[g]_na_den_[kcal]","Nasycené_mastné_kyseliny[g]_na_den_[kcal]","Nenasycené_mastné_kyseliny_na_den[g]_[kcal]"]
        chart = GraphGenerator(df)
        fig = chart.show_bar_chart(show_columns,fontsize=12,chart_name ="Průměrná energie příjatá z živin na den v jednotlivých měsících[kcal]")
        st.pyplot(fig)

    def third_chart(df):
        show_columns =["Měsíc","Bílkoviny[g]_na_den_[kcal]","Komplexní_sacharidy_na_den[g]_[kcal]","Cukry[g]_na_den_[kcal]","Nasycené_mastné_kyseliny[g]_na_den_[kcal]","Nenasycené_mastné_kyseliny_na_den[g]_[kcal]"]
        chart = GraphGenerator(df)
        fig = chart.show_bar_chart(show_columns,convert_to_percentages = True, fontsize=12, chart_name ="Průměrná energie příjatá z živin na den v jednotlivých měsících[%]")
        st.pyplot(fig)

    first_chart(df)
    second_chart(df)
    third_chart(df)

else:
    st.write("Data nenalezena! Nejprve přejdi na stránku 'Zpracování účtenek' a nech si zpracovat účtenky.")
    st.write("Poté vpravo nahoře rozklikni tři tečky a zmáčkni 'Clear cache'")

