import streamlit as st
import time

from main_data_store import MainDataStore
from receipts_manager import ReceiptsManager
from process_data import ProcessData

#TODO
#adding a function to the final_data extension (currently it is deleted before each receipt processing.)
#Procedure:
#1) Add time scraping from receipts
#2) Add a check to see if the receipt has already been processing
#3) Add the option to add receipts to final_data, or delete final_data before processing new receipts

data_in_final_database = True
number_of_receipts, expected_processing_time = ReceiptsManager.basic_processing_information()

st.title("Zpracování účtenek")


st.write("Pokuď si přejete odstranit data vašich již zpracovaných účtenek, zmáčkněte tlačítko 'Smazat data'.")
if st.button("Smazat data"):
    ProcessData.delete_user_data()
    st.write("Data smazána")

st.write("V případě zmáčknutí tlačítka 'Zpracuj účtenky' dojde ke zpracování účtenek uložených ve složce 'uctenky' ")

st.write(f"Počet účtenek ke zpracování: {number_of_receipts}")

if number_of_receipts < 1:
    st.write("Nejdříve musíte vložit vaše účtenky do složky 'uctenky'")

else:
    st.write(f"Předpokládaný čas zpracování: {expected_processing_time} vteřiny")
    if st.button("Zpracuj účtenky"):
        placeholder = st.empty()
        placeholder.text("Zpracovávám......")
        MainDataStore().execute_flow()
        placeholder.text("Hotovo!")
        st.write("Data získaná z účtenek jsou zpracována na dalších stránkách aplikace")
        st.write("----------------------------------------------------------------------------------------------------")
        time.sleep(1)

        number_of_missing_objects = ProcessData.number_of_row_items()
        if number_of_missing_objects > 0:
            st.write(f"Počet nezpracovaných položek: {number_of_missing_objects}")
            st.write("Termín 'nezpracované položky' označuje položky, které nejsou obsaženy v databázi, nedošlo k jejich zpracování a aplikace s nimi nepracuje.")
            st.write("Najdete je vygenerovány v souboru 'Nezpracované položky.xlsx' ve složce této aplikace.")
            st.write("Pokuď máte zájem o přidání těchto položek do databáze, vyplňte vygenerovaný soubor o odešlete ho na adresu receiptnutritracker@gmail.com. Postup pro vyplnění vygenerovaného souboru najdete na úvodní stránce aplikace.")


