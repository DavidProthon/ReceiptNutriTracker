import streamlit as st

from process_data import ProcessData

@st.cache_data
def create_folder_if_not_exists():
    ProcessData().create_folder_if_not_exists()

create_folder_if_not_exists()

about_page = st.Page(
    "frontend_pages/about_aplication.py",
    title="O aplikaci",
    default=True,
)
project_1_page = st.Page(
    "frontend_pages/data_initiation.py",
    title="Zpracování_účtenek",
)
project_2_page = st.Page(
    "frontend_pages/prices.py",
    title="Ceny",
)

project_3_page = st.Page(
    "frontend_pages/macronutriens.py",
    title="Makroživiny",
)
project_4_page = st.Page(
    "frontend_pages/amount_of_food.py",
    title="Množství_jídla",
)

pg = st.navigation(pages=[about_page, project_1_page, project_2_page, project_3_page, project_4_page])
pg.run()

#streamlit run app.py --server.port 8503