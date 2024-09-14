"""
Module that takes the data from the receipts, matches them with the data from the food database and creates the final data for the application.
"""

import sqlite3
import pandas as pd
from pathlib import Path

class MainDataStore:
    def __init__(self):
        self.project_db = "projekt_data.db"
        self.food_table = "food_data"
        self.receipts_table = "receipts_table"
        self.final_data = "final_data"
        self.directory = Path(__file__).parent / "uctenky"

    def make_logfile(self):
        """
        Creates an xlsx file that contains items from receipts that are not in the database.
        """

        query = f'''
        SELECT DISTINCT
            {self.receipts_table}."Položka",
            {self.food_table}."Odkaz",
            {self.food_table}."Velikost_balení",
            {self.food_table}."Druh_potraviny"
        FROM {self.receipts_table} 
        LEFT JOIN {self.food_table} 
        ON {self.receipts_table}."Položka" = {self.food_table}."Položka"
        WHERE
            {self.food_table}."Odkaz" IS NULL 
            AND {self.food_table}."Velikost_balení" IS NULL;
        '''
        
        with sqlite3.connect(self.project_db) as conn:
            df = pd.read_sql_query(query, conn)
        
        df.to_excel("Nezpracované položky.xlsx", index=False, engine="openpyxl")

    def make_final_database(self):
        """
        Joins the table with the data from the receipts with the data from the food table to create a final table that serves as the data for the application.
        """

        query = f'''
        CREATE TABLE {self.final_data} AS
        SELECT
            {self.receipts_table}."Položka",
            {self.food_table}."Skutečné_jméno",
            {self.food_table}."Odkaz",
            {self.food_table}."Velikost_balení",
            {self.receipts_table}."Poměrová_velikost_balení",
            {self.receipts_table}."Cena",
            {self.receipts_table}."Obchod",
            {self.receipts_table}."Datum_nákupu",
            {self.food_table}."Druh_potraviny",
            {self.food_table}."Energetická_hodnota",
            {self.food_table}."Bílkoviny",
            {self.food_table}."Sacharidy",
            {self.food_table}."Cukry",
            {self.food_table}."Tuky",
            {self.food_table}."Nasycené_mastné_kyseliny",
            {self.food_table}."Trans_mastné_kyseliny",
            {self.food_table}."Mononenasycené",
            {self.food_table}."Polynenasycené",
            {self.food_table}."Vláknina",
            {self.food_table}."Sůl",
            {self.food_table}."Vápník"

        FROM {self.receipts_table} LEFT JOIN food_data ON {self.receipts_table}."Položka" = {self.food_table}."Položka"
        WHERE
            {self.food_table}."Odkaz" IS NOT NULL AND {self.food_table}."Velikost_balení" IS NOT NULL;
        '''

        with sqlite3.connect(self.project_db) as conn:
            conn.execute(f"DROP TABLE IF EXISTS {self.final_data};")
            conn.execute(query)
    
    def delete_receipts_data(self):
        """
        Removes tables with data from receipts
        """

        with sqlite3.connect(self.project_db) as conn:
            conn.execute(f"DROP TABLE IF EXISTS {self.receipts_table};")
    
    def execute_flow(self):
        """
        Functions used for organization and logical processing of individual programmed functions.
        """

        from receipts_manager import ReceiptsManager
        
        try:
            from scrape_nutriens import ScrapeNutriens
            from food_for_scraping import FoodForScraping

            item_for_scraping = FoodForScraping().food_for_scraping()
            ScrapeNutriens(item_for_scraping).execute_flow()
        except ModuleNotFoundError:
            pass

        ReceiptsManager().execute_flow()
        self.make_final_database()
        self.make_logfile()
        self.delete_receipts_data()

if __name__ == "__main__":
    MainDataStore().execute_flow()
