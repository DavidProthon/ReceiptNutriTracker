"""
This module is used to process receipts from the Billa store. 
Receives the loaded receipt in the form of a formatted string.
It processes and returns individual items and information about name, relative quantity, price, store and item purchase date in the form of a dataframe.
"""

import re    
import os
from pathlib import Path

from receipt_base import Receipts

#TODO 

class BillaReceipts(Receipts):
    def __init__(self, receipt_text):
        super().__init__()
        self.receipt_text = receipt_text

    def split_on_newline(self,text):
        """
        Takes a long formatted string and splits it at places where there is a newline
        """
        
        for item in text:
            split_items = item.split('\n')
            self.lst_with_items.extend(split_items)
    
    def connect_necessary_items(self):
        """
        This function iterates through a list of items and checks whether each item ends with the character "A", "B", "C", "D".
        If an item does not end with "A", it is considered an incomplete item and is appended
        to the previous item in the list. This way, incomplete items are merged with their
        preceding items.
        """

        connected_items = []

        for item in self.lst_with_items:
            if item[-1] not in ["A", "B", "C", "D"]:
                if not connected_items:
                    connected_items.append(item)
                else: 
                    connected_items[-1] += " " + item
            else:
                connected_items.append(item)

        self.lst_with_items = connected_items
                
    def divide_the_quantity_billa(self,mark):
        """
        Duplicates items in a list based on the number found before a specified substring (mark).
        Each item containing the mark is copied (number - 1) times, and all items are returned in a new list.
        """
        new_items = []
        for item in self.lst_with_items:
            new_items.append(item) 
            if mark in item:
                match = re.search(r'(\d+)\s*' + re.escape(mark), item)
                count = int(match.group(1))  
                for _ in range(count - 1):  
                    new_items.append(item)

        self.lst_with_items = new_items
     
    def change_proportional_package_size(self,text,number):
        numbers = self.extract_numbers(text)

        if len(numbers) < number:
            return float(1)
        
        return numbers[1]
    
    def extract_numbers(self,text):
        """
        Extracts all numbers from the text and returns them in the form of a list.
        """

        match = re.findall(r"\d+(?:,\d+)?", text)

        return match
    
    def change_item(self,text,pattern):
        if pattern in text:
            return "1"
        else:
            return text
    
    def change_item_price(self,text,pattern_one,pattern_two):
        """
        If the text contains pattern_one or pattern_two, it returns the 3rd number in the sheet, otherwise it returns the first number
        """
        numbers = self.extract_numbers(text)
        if pattern_one in text or pattern_two in text:
            return numbers[2]
        else:
            return numbers[0]
    
    def items_to_dataframe(self):
        """
        Divides individual items into 2 parts. The first part is the name of the item and the second part is the rest
        """
        
        items = []
        proportions = []
        
        for item in self.lst_with_items:
            match = re.search(r"\b\d{1,2},\d{2}\b", item)
            if match:
                key = item[:match.start()].strip()  
                value = item[match.start():].strip()  

            items.append(key)
            proportions.append(value)

        self.df["Položka"] = items
        self.df["Poměrová_velikost_balení"] = proportions
        
    def add_price_column(self):
        self.df["Cena"] = self.df["Poměrová_velikost_balení"]
    
    def edit_price_column(self):
        """
        For each row in the "price" column, it looks for the price of the item
        """

        self.df["Cena"] = self.df["Cena"].apply(lambda text: self.change_item_price(text,"Kč/ks","Kč/kg"))
    
    def edit_proportional_package_size(self):
        """
        Edit the "Proportional_Package_Size" based on the presence of different substrings.
        """

        self.df["Poměrová_velikost_balení"] = self.df["Poměrová_velikost_balení"].apply(lambda text: self.change_item(text,"Kč/ks"))
        self.df["Poměrová_velikost_balení"] = self.df["Poměrová_velikost_balení"].apply(lambda text: self.change_proportional_package_size(text,2))
            
    def process_billa_receipt(self):
        """
        Functions used for organization and logical processing of individual programmed functions.
        """

        get_text = self.extract_text(self.receipt_text,r"Kč\s*(.*?)\s*K PLATBĚ")
        date = self.extract_date(self.receipt_text,r"\b\d{2}\.\d{2}\.\d{2}\b")
        
        self.split_on_newline(get_text)
        self.connect_necessary_items()
        self.remove_non_food("C")
        self.divide_the_quantity_billa(r"ks")
        
        self.items_to_dataframe() 
        self.add_price_column() 
        self.edit_price_column()
        self.edit_proportional_package_size()
        self.add_shop_column("Billa")
        self.add_date_column(date)
        self.set_correct_data_types()
        self.add_shopname_to_item("Billa")

        return self.df
    
  
if __name__ == "__main__":
    from read_recepits import PngReader
    directory = Path(__file__).parent / "uctenky"
    
    for receipt in os.listdir(directory):
        if receipt.endswith(".png"):
            receipt_path = os.path.join(directory, receipt)
            receipt_text = PngReader(receipt_path).read_png() 
            data = BillaReceipts(receipt_text).process_billa_receipt()

