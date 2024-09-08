import streamlit as st
import time

from main_data_store import MainDataStore
from receipts_manager import ReceiptsManager
from process_data import ProcessData

#TODO Add a function to find out how many items are missing in the database - the number of muissing object, so far i have set 1.
#TODO Add a condition, if i find 0 items, then even before I give the option to process the receipts, it says that I haven't found anything

number_of_receipts, expected_processing_time = ReceiptsManager.basic_processing_information()

st.title("Zpracování účtenek")
st.write(f"Počet účtenek ke zpracování: {number_of_receipts}")
st.write(f"Předpokládaný čas zpracování: {expected_processing_time} vteřiny")

if st.button("Zpracuj účtenky"):
    placeholder = st.empty()
    placeholder.text("zpracovávám......")
    MainDataStore().execute_flow()
    placeholder.text("Hotovo!")
    st.write("Data získaná z účtenek jsou zpracována na dalších stránkách aplikace")
    st.write("----------------------------------------------------------------------------------------------------")
    time.sleep(1)

    number_of_missing_objects = ProcessData.number_of_row_items()
    if number_of_missing_objects > 0:
        st.write(f"Počet nezpracovaných položek: {number_of_missing_objects}")
        st.write("Nezpracované položky jsou vygenerovány v souboru 'Nezpracované položky.xlsx' ve složce s touto aplikací.")
        st.write("Pokuď máte zájem o přidání těchto položek do databáze, vyplňte vygenerovaný soubor o odešlete ho na adresu NAPIS@ADRESU.com")

