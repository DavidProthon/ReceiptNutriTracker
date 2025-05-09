"""
The module that contains classes for reading pdf and png files.
"""

from PIL import Image
import pytesseract
import os
import PyPDF2  
from pathlib import Path

#TODO add pyteseract to the program folder

class PngReader:
    """
    A class that is used to convert a receipt in the form of png to a formatted string
    """
    
    pytesseract.pytesseract.tesseract_cmd = Path(__file__).parent / "Tesseract-OCR" / "tesseract.exe"
    language_code = "ces"

    def __init__(self,receipt_path):
        self.receipt_path = receipt_path
    
    
    def is_language_model_available(self,language_code):
        """
        Function to check the availability of the language model
        """

        tessdata_prefix = os.path.join(os.path.dirname(pytesseract.pytesseract.tesseract_cmd), "tessdata")
        lang_file = os.path.join(tessdata_prefix, f"{language_code}.traineddata")
        return os.path.isfile(lang_file)

    def read_png(self):
        try:
            if not self.is_language_model_available(self.language_code):
                raise FileNotFoundError(f"Jazykový model '{self.language_code}' nebyl nalezen. Prosím stáhni jej z [Tesseract GitHub](https://github.com/tesseract-ocr/tessdata) a ulož do adresáře 'tessdata'.")

            image = Image.open(self.receipt_path)
            text = pytesseract.image_to_string(image, lang=self.language_code, config="--psm 6") #psm must be 6 because it takes the receipt as one block

            return text

        except FileNotFoundError as e:
            print(e)
        except pytesseract.pytesseract.TesseractError as e:
            print(f"Chyba při zpracování obrázku: {e}")
        except Exception as e:
            print(f"Došlo k neznámé chybě: {e}")

class PdfReader:
    """
    A class that is used to convert a receipt in the form of pdf to a formatted string
    """
    def __init__(self,receipt_path):
        self.receipt_path = receipt_path

    def read_pdf(self):
        reader = PyPDF2.PdfReader(self.receipt_path)
        text = reader.pages[0].extract_text()

        return text