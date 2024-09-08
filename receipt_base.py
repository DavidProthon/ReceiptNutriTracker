"""
This module contains a base class for receipts with shared functionality between different types of stores
"""

import re    
from datetime import datetime
import pandas as pd 

#TODO 
#add time extract
#add a check if the same receipt is not inserted more than once

class Receipts:
    def __init__(self):
        self.df = pd.DataFrame()
        self.lst_with_items = list()
        self.dct_with_items = dict()

    def extract_text(self,receipt_text,pattern):
        """
        Based on a regular expression, it finds the part of the text where the purchased items are.
        """ 
        text = re.findall(pattern, receipt_text, re.DOTALL)
  
        return text
            
    def extract_date(self,receipt_text,date_pattern):
        """
        Dxtracts the date from the text and converts it into a format that sqlite can work with
        """

        find_buy_date = re.search(date_pattern, receipt_text).group()
        cleaned_buy_date = re.sub(r"\s+", "", find_buy_date) 

        if len(find_buy_date.split(".")[-1]) == 4:
            format_buy_date = datetime.strptime(cleaned_buy_date, "%d.%m.%Y") 
        else:
            format_buy_date = datetime.strptime(cleaned_buy_date, "%d.%m.%y") 

        buy_date = format_buy_date.strftime("%Y-%m-%d")  

        return buy_date
    
    def remove_non_food(self,mark):
        """removes items that are taxed at a rate other than food"""

        self.lst_with_items = [item for item in self.lst_with_items if not re.search(r"\b" + re.escape(mark) + r"\b", item)]
        
    def add_date_column(self,date):
        self.df["Datum_nákupu"] = date
    
    def add_shop_column(self,shop):
        self.df[["Obchod"]] = shop
    
    def replace_comma(self,value):
        if isinstance(value, str):
            return value.replace(",", ".")
        
        return value
    
    def set_correct_data_types(self):
        self.df["Poměrová_velikost_balení"] = self.df["Poměrová_velikost_balení"].apply(self.replace_comma).astype(float)
        self.df["Cena"] = self.df["Cena"].apply(self.replace_comma).astype(float)
        
    def add_shopname_to_item(self,shop_name):
        """
        Adds to each item the name of the store the item came from
        """

        self.df["Položka"] = self.df["Položka"].apply(lambda item: f"{(item)}_{shop_name}")
    
    def reset_dataframe_index(self):
        self.df = self.df.reset_index(drop=True)





