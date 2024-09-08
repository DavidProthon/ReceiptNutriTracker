import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from albert_receipts import AlbertReceipts

class TestAlbertReceipts(unittest.TestCase):

    def test_function_all(self):
        expected_df_1 = pd.DataFrame({
        "Položka": [
            "LUČINA JARNÍ PAŽITKA_Albert", "RT LOSOS KETA MSC_Albert", "*GOUDA 48% PLATKY 20_Albert", 
            "PREMIUM PAPRIKÁŠ_Albert", "CHLÉB VESNICKÝ 400G_Albert", "OKURKY HADOVKY KS_Albert", 
            "OKURKY HADOVKY KS_Albert"
        ],
        "Poměrová_velikost_balení": [1.000, 0.216, 1.000, 0.206, 1.000, 1.000, 1.000],
        "Cena": [38.9, 68.9, 40.8, 53.8, 35.9, 16.9, 16.9],
        "Obchod": ["Albert"] * 7,
        "Datum_nákupu": ["2024-02-19"] * 7
        })

        expected_df_2 = pd.DataFrame({
        "Položka": ["TCHIBO BAR.ZR.K.1KG_Albert", "*HROZNY BÍLÉ BEZSE_Albert", "MLYNÁŘSKÁ VEKA 400G_Albert", 
            "ALB EIDAM 45%PL.200G_Albert"
        ],
        "Poměrová_velikost_balení": [1.0, 1.0, 1.0, 1.0],
        "Cena": [629.0, 44.9, 38.9, 47.6],
        "Obchod": ["Albert"] * 4 ,
        "Datum_nákupu": ["2024-02-25"] * 4
        })

        expected_df_3 = pd.DataFrame({
        "Položka": ["MLYNÁŘSKÁ VEKA 400G_Albert", "*HROZNY BÍLÉ BEZSE_Albert", "RAJČATA KOKTEJL.400G_Albert", 
            "JČ NIVA 45% POR.100G_Albert", "LUČINA PAŽITKA 180G_Albert", "LUČINA PAŽITKA 180G_Albert", 
            "PREMIUM PAPRIKÁŠ_Albert"
        ],
        "Poměrová_velikost_balení": [1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 0.218],
        "Cena": [38.9, 76.9, 34.9, 29.1, 38.8, 38.8, 74.1],
        "Obchod": ["Albert"] * 7 ,
        "Datum_nákupu": ["2024-02-29"] * 7
        })

        expected_df_4 = pd.DataFrame({
        "Položka": ["MLYNÁŘSKÁ VEKA 400G_Albert", "ALB NITĚ UZENÉ 250G_Albert", "ALB EIDAM 45%PL.200G_Albert", 
            "LUČINA PAŽITKA 180G_Albert", "RAJČATA KOKTEJL.400G_Albert", "RAJČATA KOKTEJL.400G_Albert", 
            "*HROZNY BÍLÉ BEZSE_Albert", "PRINC SALÁM_Albert"
        ],
        "Poměrová_velikost_balení": [1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 0.206],
        "Cena": [38.9, 77.8, 47.6, 38.8, 34.9, 34.9, 76.9, 88.2],
        "Obchod": ["Albert"] * 8 ,
        "Datum_nákupu": ["2024-03-04"] * 8 
        })


        result_df_1 = AlbertReceipts("272.10 Kč •0 kreditů •1 bod 19. 2. 2024\nPoložka Cena\nLUČINA JARNÍ PAŽITKA\n1 x 38.90 Kč 38.90 KčA\nRT LOSOS KETA MSC\n0.216 x 319.00 KčE\n68.90 KčA\n*GOUDA 48% PLATKY 20\n1 x 40.80 Kč 40.80 KčA\nPREMIUM PAPRIKÁŠ\n0.206 x 261.00 KčE\n53.80 KčA\nCHLÉB VESNICKÝ 400G\n1 x 35.90 Kč 35.90 KčA\nOKURKY HADOVKY KS\n2 x 16.90 Kč 33.80 KčA\nCelkem 272.10 Kč\nZískané kredity 0 kreditů\nZískané body 1 bod\nPRODEJNA\nJihlava, Brtnická\nBrtnická 4030/7, JihlavaKLIENT\n+420\nPlatební metoda Hodnota\nPlatební karty 272.10 Kč\nKód Sazba Základ DPH Výše DPH\nA 12 % 242.95 Kč 29.15 Kč\nDatum Čas Obch Pokl Obsl Trans\n19. 02. 24 16:42 155 103 103 85473\nDíky akcím jste ušetřili 34.00 Kč\n19/02/24 16:44 Účtenka číslo 02823\nTerminál: (PVTC1063-56406155)\nPRODEJ 272.10 Kč\n**** **** **** 5103 / 00 (L) VISA\nA0 00 00 00 03 10 10 Visa Debit\nVisa Contactless\nSEQ ID: 004:743:125, Autoriz. kód 044362\nNo Pin *NO REFUND*\nID účtu: 01552402191035473\nAlbert Česká republika, s.r.o.\nRadlická 520/117, 158 00 Praha 5\nIČO: 44012373, DIČ: CZ44012373\nLegenda způsobu vážení položek:\n“M” - Ruční zadání, “P” - Váženo na pokladně, “E” - Váženo etiketovací váhou\n660000155001030008547320240219164254").process_albert_receipt()
        result_df_2 = AlbertReceipts("760.40 Kč •7 kreditů •3 body 25. 2. 2024\nZískané kredity 7\n• Produkty z nabídky zdravá inspirace 4\n• Kupóny 3\nPoložka Cena\nTCHIBO BAR.ZR.K.1KG\n1 x 629.00 Kč 629.00 KčA\n*HROZNY BÍLÉ BEZSE\n1 x 44.90 Kč 44.90 KčA\nZískané kredity: 3 kredity\nMLYNÁŘSKÁ VEKA 400G\n1 x 38.90 Kč 38.90 KčA\nZískané kredity: 4 kredity\nALB EIDAM 45%PL.200G\n1 x 47.60 Kč 47.60 KčA\nCelkem 760.40 Kč\nZískané kredity 7 kreditů\nZískané body 3 body\nPRODEJNA\nJihlava, Brtnická\nBrtnická 4030/7, JihlavaKLIENT\n+420\nPlatební metoda Hodnota\nPlatební karty 760.40 Kč\nKód Sazba Základ DPH Výše DPH\nA 12 % 678.93 Kč 81.47 Kč\nDatum Čas Obch Pokl Obsl Trans\n25. 02. 24 13:38 155 101 101 25170\nDíky akcím jste ušetřili 32.00 Kč\n25/02/24 13:40 Účtenka číslo 00705\nTerminál: (PVTC1064-56406155)\nPRODEJ 760.40 Kč\n**** **** **** 5103 / 00 (L) VISA\nA0 00 00 00 03 10 10 Visa Debit\nVisa Contactless\nSEQ ID: 015:888:061, Autoriz. kód 700702\nPin zadán *NO REFUND*\nID účtu: 01552402251015170\nAlbert Česká republika, s.r .o.\nRadlická 520/117, 158 00 Praha 5\nIČO: 44012373, DIČ: CZ44012373\nLegenda způsobu vážení položek:\n“M” - Ruční zadání, “P” - Váženo na pokladně, “E” - Váženo etiketovací váhou\n660000155001010002517020240225133835").process_albert_receipt()
        result_df_3 = AlbertReceipts("411.40 Kč •5 kreditů •2 body 29. 2. 2024\nZískané kredity 5\n• Produkty z nabídky zdravá inspirace 5\nPoložka Cena\nZP COLG.MAX WHITE 75\n1 x 79.90 Kč 79.90 KčB\nMLYNÁŘSKÁ VEKA 400G\n1 x 38.90 Kč 38.90 KčA\nZískané kredity: 5 kreditů\n*HROZNY BÍLÉ BEZSE\n1 x 76.90 Kč 76.90 KčA\nRAJČATA KOKTEJL.400G\n1 x 34.90 Kč 34.90 KčA\nJČ NIVA 45% POR.100G\n1 x 29.10 Kč 29.10 KčA\nLUČINA PAŽITKA 180G\n2 x 38.80 Kč 77.60 KčA\nPREMIUM PAPRIKÁŠ\n0.218 x 340.00 KčE\n74.10 KčA\nCelkem 411.40 Kč\nZískané kredity 5 kreditů\nZískané body 2 body\nPRODEJNA\nJihlava, Kollárova\nKollárova 2762/17, JihlavaKLIENT\n+420\nPlatební metoda Hodnota\nPlatební karty 411.40 Kč\nKód Sazba Základ DPH Výše DPH\nA 12 % 295.98 Kč 35.52 Kč\nB 21 % 66.03 Kč 13.87 Kč\nDatum Čas Obch Pokl Obsl Trans\n29. 02. 24 15:32 731 102 102 40634\nDíky akcím jste ušetřili 69.00 Kč\n29/02/24 15:38 Účtenka číslo 08537\nTerminál: (PVTC3578-56406731)\nPRODEJ 411.40 Kč\n**** **** **** 5103 / 00 (L) VISA\nA0 00 00 00 03 10 10 Visa Debit\nVisa Contactless\nSEQ ID: 001:503:066, Autoriz. kód 029532\nNo Pin *NO REFUND*\nID účtu: 07312402291020634\nAlbert Česká republika, s.r .o.\nRadlická 520/117, 158 00 Praha 5\nIČO: 44012373, DIČ: CZ44012373\nLegenda způsobu vážení položek:\n“M” - Ruční zadání, “P” - Váženo na pokladně, “E” - Váženo etiketovací váhou\n660000731001020004063420240229153230").process_albert_receipt()
        result_df_4 = AlbertReceipts("438.00 Kč •5 kreditů •2 body 4. 3. 2024\nZískané kredity 5\n• Produkty z nabídky zdravá inspirace 5\nPoložka Cena\nMLYNÁŘSKÁ VEKA 400G\n1 x 38.90 Kč 38.90 KčA\nZískané kredity: 5 kreditů\nALB NITĚ UZENÉ 250G\n1 x 77.80 Kč 77.80 KčA\nALB EIDAM 45%PL.200G\n1 x 47.60 Kč 47.60 KčA\nLUČINA PAŽITKA 180G\n1 x 38.80 Kč 38.80 KčA\nRAJČATA KOKTEJL.400G\n2 x 34.90 Kč 69.80 KčA\n*HROZNY BÍLÉ BEZSE\n1 x 76.90 Kč 76.90 KčA\nPRINC SALÁM\n0.206 x 428.00 KčE\n88.20 KčA\nCelkem 438.00 Kč\nZískané kredity 5 kreditů\nZískané body 2 body\nPRODEJNA\nJihlava, Kollárova\nKollárova 2762/17, JihlavaKLIENT\n+420\nPlatební metoda Hodnota\nPlatební karty 438.00 Kč\nKód Sazba Základ DPH Výše DPH\nA 12 % 391.07 Kč 46.93 Kč\nDatum Čas Obch Pokl Obsl Trans\n04. 03. 24 16:11 731 103 103 16765\nDíky akcím jste ušetřili 79.00 Kč\n04/03/24 16:19 Účtenka číslo 04677\nTerminál: (PVTC3579-56406731)\nPRODEJ 438.00 Kč\n**** **** **** 5103 / 00 (L) VISA\nA0 00 00 00 03 10 10 Visa Debit\nVisa Contactless\nSEQ ID: 001:516:078, Autoriz. kód 195159\nNo Pin *NO REFUND*\nID účtu: 07312403041036765\nAlbert Česká republika, s.r.o.\nRadlická 520/117, 158 00 Praha 5\nIČO: 44012373, DIČ: CZ44012373\nLegenda způsobu vážení položek:\n“M” - Ruční zadání, “P” - Váženo na pokladně, “E” - Váženo etiketovací váhou\n660000731001030001676520240304161118").process_albert_receipt()

        test_cases = [
            (result_df_1, expected_df_1),
            (result_df_2, expected_df_2),
            (result_df_3, expected_df_3),
            (result_df_4, expected_df_4)
        ]

        for i, (result_df, expected_df) in enumerate(test_cases, start=1):
            try:
                assert_frame_equal(result_df, expected_df)
                print(f"OK test for case {i}")
            except AssertionError as e:
                print(f"Fail test for case {i}: {e}")
                raise

if __name__ == "__main__":
    unittest.main()