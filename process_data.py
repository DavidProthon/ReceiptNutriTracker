"""
The module is used to load the necessary data for individual streamlite pages and to process data according to the requirements of the front end.
"""

import sqlite3
import pandas as pd
import openpyxl
from pathlib import Path

#TODO Possible to separate the module obtaining data and processing data

class ProcessData:
    def __init__(self):
        self.project_db = "projekt_data.db"
        self.final_data = "final_data"
        self.connection = None
        self.df = pd.DataFrame()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.project_db)
        except sqlite3.Error as e:
            print(f"Chyba při připojování k databázi: {e}")
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Připojení k databázi bylo uzavřeno.")

    def get_data_from_final_data(self,query):
        if self.connection:
            try:
                # Check if the "final_data" table exists
                table_exists_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='final_data';"
                table_exists = pd.read_sql_query(table_exists_query, self.connection)

                if table_exists.empty:
                    raise Exception("Tabulka 'final_data' neexistuje.")

                # If the "final data" table exists, we check if it contains any data
                data_check_query = "SELECT COUNT(*) as row_count FROM final_data;"
                row_count = pd.read_sql_query(data_check_query, self.connection)

                if row_count["row_count"][0] == 0:
                    raise Exception("Tabulka 'final_data' neobsahuje žádná data.")

                # If the table exists and contains data, we load the data
                self.df = pd.read_sql_query(query, self.connection)

            except Exception as e:
                print(f"Výjimka: {e}")
        else:
            print("Nejprve se připojte k databázi.")

    def data_prices_page(self):
        query = f"""SELECT 
        "Položka",
        "Velikost_balení",
        "Poměrová_velikost_balení", 
        "Cena",
        "Datum_nákupu"
        FROM {self.final_data}"""

        self.get_data_from_final_data(query)

    def data_macronutriens_page(self):
        query = f"""SELECT 
        "Položka",
        "Velikost_balení",
        "Poměrová_velikost_balení", 
        "Datum_nákupu",
        "Energetická_hodnota",
        "Bílkoviny",
        "Sacharidy",
        "Cukry",
        "Tuky",
        "Nasycené_mastné_kyseliny",
        "Vláknina",
        "Sůl"
        FROM {self.final_data}"""

        self.get_data_from_final_data(query)
    
    def data_amount_of_food_page(self):
        query = f"""SELECT 
        "Velikost_balení",
        "Poměrová_velikost_balení", 
        "Datum_nákupu",
        "Druh_potraviny"

        FROM {self.final_data}"""

        self.get_data_from_final_data(query)

    def price_to_grams(self):
        """
        Calculate proportional price per 100g.
        Updates the dataframe with a new column "Proportional_Price".
        """

        self.df["Poměrová_cena"] = self.df.apply(
            lambda row: (row["Cena"] * 100) / (row["Velikost_balení"] * row["Poměrová_velikost_balení"]),
            axis=1
        )

    def get_df_prices_page(self):
        """
        data for the frontend prices_page
        """

        self.connect()
        self.data_prices_page()
        self.close_connection()

        if self.df.empty:
            return self.df
        
        self.price_to_grams()

        return self.df
     
    def get_df_macronutriens_page(self):
        """
        data for the frontend macronutriens_page
        """

        self.connect()
        self.data_macronutriens_page()
        self.close_connection()
        
        return self.df
    
    def get_df_amount_of_food_page(self):
        """
        data for the frontend amount_of_food_page
        """

        self.connect()
        self.data_amount_of_food_page()
        self.close_connection()
        
        return self.df
    
    @staticmethod
    def get_value_items(df,column):
        """
        Converts scraped 100g to the size of the package and divides it by the number of days in the month. This creates an item average for one day
        """

        df[f"{column}[g]_na_den"] = df.apply(
        lambda row: ((row["Poměrová_velikost_balení"] * row["Velikost_balení"] * row[column])/100)/row["Počet_dnů_v_měsíci"],
        axis=1
        )

        return df
    
    @staticmethod
    def get_value_items_in_kj(df,column,type_of_nutient):
        """
        Converts the amount of macronutrient [g] to [kcal]
        """
        if type_of_nutient == "Bílkoviny" or type_of_nutient == "Sacharidy":
            type_of_nutient = 4.1
        else:
            type_of_nutient = 9.02

        df[f"{column}_[kcal]"] = df.apply(
        lambda row: row[column] * type_of_nutient,
        axis=1
        )

        return df
    
    @staticmethod
    def get_quantity_of_selected_type(df,type_of_food):
        """
        The function is used to obtain the average amount of nutrients in [g] per day according to the purchased month
        """
        new_columns = list()
        new_columns.append("Měsíc")
        for food in type_of_food:
            df[f"Množství_{food}_na_den[g]"] = df.apply(
                lambda row: ((row["Poměrová_velikost_balení"] * row["Velikost_balení"]))/row["Počet_dnů_v_měsíci"]
                if row["Druh_potraviny"] == food 
                else None,
                axis=1

            )
            new_columns.append(f"Množství_{food}_na_den[g]")

        return df,new_columns

    @staticmethod
    def add_number_of_days_in_month(df):
        """
        For each item adds the number of days in the purchased month
        """
        df["Počet_dnů_v_měsíci"] = df["Měsíc"].apply(lambda x: pd.Period(x, freq="M").days_in_month)

        return df
    
    @staticmethod
    def get_complex_carbs(df):
        """
        Function add a column with complex carbohydrates per day.
        They find out by subtracting the number of carbohydrates per day from the sugars per day
        """

        df["Komplexní_sacharidy_na_den[g]"] = df.apply(
        lambda row: (row["Sacharidy[g]_na_den"] - row["Cukry[g]_na_den"]),
        axis=1
        )

        return df
    
    @staticmethod
    def get_unsaturated_fatty_acids(df):
        """
        Function add a column with unsaturated_fatty acids per day .
        They find out by subtracting the number of fats per day from the saturated fatty acids per day
        """

        df["Nenasycené_mastné_kyseliny_na_den[g]"] = df.apply(
        lambda row: (row["Tuky[g]_na_den"] - row["Nasycené_mastné_kyseliny[g]_na_den"]),
        axis=1
        )

        return df
    
    @staticmethod
    def number_of_row_items():
        """
        Function is used to go through the file "Nezpracované položky.xlsx" and find the number of records.

        """
        
        path = Path("Nezpracované položky.xlsx")
        
        if not path.exists():

            return 0
        else:
            wb = openpyxl.load_workbook(path)
            sheet = wb.active
            row_count = sheet.max_row - 1
            
            return row_count if row_count > 0 else 0
        
    @staticmethod
    def create_folder_if_not_exists():
        """
        Create the receipt folder if it does not exist
        """

        folder = Path(__file__).parent / "uctenky"
        if folder.exists():
            pass
        else:
            folder.mkdir(parents=True, exist_ok=True)

            
    @staticmethod
    def delete_final_data():
        """
        Temporary function for delete final_data before push to github.
        Will be deprecated after split database.
        """
        with sqlite3.connect("projekt_data.db") as conn:
            conn.execute("DROP TABLE IF EXISTS final_data")


    




