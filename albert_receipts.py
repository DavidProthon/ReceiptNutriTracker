"""
This module is used to process receipts from the Albert store. 
Receives the loaded receipt in the form of a formatted string.
It processes and returns individual items and information about name, relative quantity, price, store and item purchase date in the form of a dataframe.
"""

import re    
import os
from pathlib import Path
import pandas as pd 

from receipt_base import Receipts

#TODO 
#Complete the support for a tax rate other than A and B

class AlbertReceipts(Receipts):
    def __init__(self, receipt_text):
        super().__init__()
        self.receipt_text = receipt_text

    def clear_items(self,buy_items):
        """
        Removes redundant text that gives information about earned credits.
        """

        credit_pattern = r"\nZískané kredity: \d+ kredit(y|ů)" 
        self.lst_with_items = [re.sub(credit_pattern, "", item) for item in buy_items]
    
    def get_individual_items(self):
        """
        First it finds the positions of all "KčA" and "KčB".
        (These are strings that are always at the end of each receipt item).
        And then divides them according to these positions.
        """

        pozice = [] 
        for item in self.lst_with_items:

            pozice.extend([i for i in range(len(item)) if item.startswith("KčA", i) or item.startswith("KčB", i)])

        individual_items = []
        for i in range(len(pozice)):
            if i == 0:
                individual_items.append(self.lst_with_items[0][:pozice[i]+3])
            else:
                individual_items.append(self.lst_with_items[0][pozice[i-1]+4:pozice[i]+3])


        self.lst_with_items = individual_items
           
    def items_to_dict(self):
        """
        Splits each item into 2 parts. 
        The first part will be the name of the item. 
        The second part will have information about the quantity and price.
        """

        for string in self.lst_with_items:
            key, value = string.split("\n", 1)
            self.dct_with_items[key] = value

    def clear_items_to_dict(self):
        """
        Removes formate \n from items.
        """

        for key in self.dct_with_items:
            self.dct_with_items[key] = self.dct_with_items[key].replace("\n", " ")
    
    def dict_to_df(self): 
        """
        Turns the dictionary into a dataframe. 
        Then makes a copy of the item's price and relative size. Both items will then be modified.
        """

        self.df = pd.DataFrame(self.dct_with_items.items(), columns=["Položka", "Poměrová_velikost_balení"])
        self.df["Cena"] = self.df["Poměrová_velikost_balení"]
        self.df["Poměrová_velikost_balení"] = self.df["Poměrová_velikost_balení"].str.split(" x ").str[0]
        self.df["Cena"] = self.df["Cena"].str.extract(r"(\d+\.\d+) KčA")

    def divide_the_quantity_albert(self):
        """
        Items for which more than 1 piece is purchased are divided into individual pieces and the obtained price per piece.
        """
    
        new_rows = []

        for _ , row in self.df.iterrows():
            if row["Poměrová_velikost_balení"] > 1:
                if row["Poměrová_velikost_balení"] % 1 == 0:
                    for _ in range(int(row["Poměrová_velikost_balení"])):
                        new_row = row.copy()
                        new_row["Poměrová_velikost_balení"] = 1
                        new_row["Cena"] = row["Cena"] / row["Poměrová_velikost_balení"]
                        new_rows.append(new_row)
                else:
                    new_rows.append(row)
            else:
                new_rows.append(row)

        self.df = pd.DataFrame(new_rows)

    def process_albert_receipt(self):
        """
        Functions used for organization and logical processing of individual programmed functions.
        """

        get_text = self.extract_text(self.receipt_text,r"Položka Cena\n(.*?)\nCelkem")
        date = self.extract_date(self.receipt_text,r"\b(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{2})\b")    
        self.clear_items(get_text)
        self.get_individual_items()
        self.remove_non_food("KčB")
        self.items_to_dict()
        self.clear_items_to_dict()
        self.dict_to_df()

        self.set_correct_data_types()
        self.divide_the_quantity_albert()
        self.set_correct_data_types()
        self.add_shop_column("Albert")
        self.add_date_column(date)
        self.add_shopname_to_item("Albert")
        self.reset_dataframe_index()

        return self.df
        
if __name__ == "__main__":
    from read_recepits import PdfReader
    directory = Path(__file__).parent / "uctenky"
    
    for receipt in os.listdir(directory):
        if receipt.endswith(".pdf"):
            receipt_path = os.path.join(directory, receipt)
            receipt_text = PdfReader(receipt_path).read_pdf() 
            data = AlbertReceipts(receipt_text).process_albert_receipt()

