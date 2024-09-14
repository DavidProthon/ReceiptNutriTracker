"""
Module that is used to control the processing of receipts and stores data from them in a database
"""

import pandas as pd
import os
import sqlite3
from pathlib import Path

from read_recepits import PngReader
from read_recepits import PdfReader
from albert_receipts import AlbertReceipts
from billa_receipts import BillaReceipts
from main_data_store import MainDataStore

#TODO 

class ReceiptsManager(MainDataStore):
    receipts_data_template = [
        ("Položka", "TEXT"), 
        ("Poměrová_velikost_balení", "REAL"), 
        ("Cena", "REAL"), 
        ("Obchod", "TEXT"), 
        ("Datum_nákupu", "TEXT"), 
    ]
    
    def __init__(self):
        super().__init__()

    def sort_receipt(self):
        """
        The function first goes through the receipts, reads them and finds out what type and store they are from.
        Based on this, it sends a formatted string of receipts for the processing of a certain class. 
        In this way, it processes all the items in the folder and returns a dataframe with main information about receipts.
        """

        df = pd.DataFrame(columns=[item[0] for item in self.receipts_data_template])
        
        for receipt in os.listdir(self.directory):
            if receipt.endswith(".pdf"):
                receipt_path = os.path.join(self.directory, receipt)
                receipts_text = PdfReader(receipt_path).read_pdf() 
                
                if "Albert" in receipts_text:
                    process_receipt = AlbertReceipts(receipts_text).process_albert_receipt()
                    df = pd.concat([df, process_receipt], ignore_index=True)

            if receipt.endswith(".png"):
                receipt_path = os.path.join(self.directory, receipt)
                receipts_text = PngReader(receipt_path).read_png() 

                if "Lidl" in receipts_text:
                    process_receipt = BillaReceipts(receipts_text).process_billa_receipt()
                    df = pd.concat([df, process_receipt], ignore_index=True)

        return df
    
    def create_table(self):
        """
        Creates a table for data from receipts
        """
        with sqlite3.connect(self.project_db) as conn:
            cursor = conn.cursor()
            columns_with_types = [f"[{column_name}] {column_type}" for column_name, column_type in self.receipts_data_template]
            create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS {self.receipts_table} (
                {", ".join(columns_with_types)}
            );
            '''
            cursor.execute(create_table_sql)
            conn.commit()
    
    def data_to_db(self,df):
        """
        Inserts data from receipts in the dataframe into a sql table.
        """
        with sqlite3.connect(self.project_db) as conn:
            df.to_sql(self.receipts_table, conn, if_exists="append", index=False)

    @staticmethod
    def basic_processing_information():
        """
        Calculation of the number of receipts to be processed and the required calculation time.
        """

        directory = Path(__file__).parent / "uctenky"
        pdf_count = 0
        png_count = 0
        processing_time_pdf = 0.07
        processing_time_png = 3
        other_processing_time = 1

        for file in os.listdir(directory):
            if file.endswith(".pdf"):
                pdf_count += 1
            elif file.endswith(".png"):
                png_count += 1
        
        number_of_receipts = pdf_count + png_count 
        expected_processing_time = round(float((pdf_count*processing_time_pdf) + (png_count*processing_time_png) + (other_processing_time)), 1)

        return  number_of_receipts, expected_processing_time
    
    def execute_flow(self):
        """
        Functions used for organization and logical processing of individual programmed functions.
        """

        df = self.sort_receipt()
        df.sort_values(by="Datum_nákupu", inplace=True)
        self.create_table()
        self.data_to_db(df)
        
if __name__ == "__main__":
    food_data = ReceiptsManager().execute_flow()
