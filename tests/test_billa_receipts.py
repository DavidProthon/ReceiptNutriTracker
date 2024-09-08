import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from billa_receipts import BillaReceipts

class TestBillaReceipts(unittest.TestCase):

    def test_function_all(self):
        expected_df_1 = pd.DataFrame({
        "Položka": ["Sušenky s krémem_Billa", "Mrkev volná_Billa", "Hrozny tmave 500g_Billa"],
        "Poměrová_velikost_balení": [1.0, 0.686, 1.0],
        "Cena": [42.90, 7.70, 34.90],
        "Obchod": ["Billa"] * 3,
        "Datum_nákupu": ["2024-08-12", "2024-08-12", "2024-08-12"]
        })

        expected_df_2 = pd.DataFrame({
        "Položka": ["Kaiserka cer.XXxL_Billa", "Kaiserka cer.XXxL_Billa", "Kaiserka cer.XXxL_Billa", "Kaiserka cer.XXxL_Billa", "Kaiserka cer.XXxL_Billa",
            "Eidam plátky_Billa", "Eidam plátky_Billa", "Sušenky s krémem_Billa", "Kuř.steaky Piri P._Billa", "Hrozny bílé 500gBS_Billa"],
        "Poměrová_velikost_balení": [1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 0.478, 1.000],
        "Cena": [5.90, 5.90, 5.90, 5.90, 5.90, 21.90, 21.90, 42.90, 189.90, 49.90],
        "Obchod": ["Billa"] * 10,
        "Datum_nákupu": ["2024-08-17"] * 10
        })

        expected_df_3 = pd.DataFrame({
        "Položka": ["Ementál plátk. sýr_Billa", "Čers.mléko 1,5% 11_Billa", "Sušenky s krémem_Billa", "Rajčata keříková_Billa", 
            "Kornbageta_Billa", "Kornbageta_Billa", "Kornbageta_Billa", "Paprika červená_Billa"],
            "Poměrová_velikost_balení": [1.000, 1.000, 1.000, 0.718, 1.000, 1.000, 1.000, 0.662],
        "Cena": [42.90, 21.90, 42.90, 49.90, 6.90, 6.90, 6.90, 49.90],
        "Obchod": ["Billa"] * 8,
        "Datum_nákupu": ["2024-08-15"] * 8
        })

        result_df_1 = BillaReceipts("©\nmL Jednička v čerstvosti\nProvozovna:\nJihlava, Okružní\nKč\nSušenky s krémem 42,90 B\nMrkev volná 5,28 B\nN 0,686 kg x 7,70  Kč/kg\nHrozny tmave 500g 34,90 B\nK PLATBĚ 83,08\nKarta 83,08\nCelková zaplacená částka 83,08\nOhodnoťte svůj obchod\na vyhrajte nový iPhone 15 Pro\nlidl.cz/hodnoceni\n12/08/24 20:45 Účtenka číslo 06614\nTerminál: (LIDL1021-53268102)\nPRODEJ 83.08 Kč\n*kk** *kk*k **k** 5103 / 00 (L) VISA\nA0 00 00 00 03 10 10 Visa Debit\nVisa Contactless\nSEO ID: 001:907:355, Autoriz. kód 187502\nNo Pin *NO REFUND*\n\nB 12% DPH z 83,08 8,90\n0102 226457/020/01 12.08.24 20:44:32\nN = Netto váha\n\nZáruční a další údaje - zadní strana\n\nPrůmyslové zboží je možné vrátit na základě\n\noriginální nebo této elektronické účtenky v\npůvodním (nezávadném) stavu a originálním\nobalu do 30 dní od data nákupu.\nDárkovou kartu není možné vrátit, ani vyměnit.\nLidl Česká republika s.r.o.\nNárožní 1359/11, 158 00 Praha 5\nIČC: 26178541, DIC: CZ2617/8541\nMS Praha, zn. C 392174\nNákup proveden na\nJihlava, Okružní\nOkružní 4967/15\n586 00 Jihlava\nInformace o prodejně").process_billa_receipt()
        result_df_2 = BillaReceipts("©\nmL Jednička v čerstvosti\nProvozovna:\nJihlava, Okružní\nKč\nKaiserka cer.XXxL 29,50 B\n5 ks x 5,90 Kč/ks\n4+1 zdarma Kaiserka -5,90\nCena po slevě 23,60\nEidam plátky 43,80 B\n2 ks x 21,90 Kč/ks\n455180 Psací potř. 49,90 C\nSušenky s krémem 42,90 B\nKuř.steaky Piri P. 90,77 B\nE 0,478 kg x 189,90 Kč/kg\nHrozny bílé 500gBS 49,90 B\nK PLATBĚ 300,87\nKarta 300,87\nCelková zaplacená částka 300,87\n17/08/24 08:40 Účtenka číslo 06255\nTerminál: (LI010281-53268102)\nPRODEJ 300.87 kKč\n*kkk* *kkk kk*k* 5103 / 00 (L) VISA\nA0 00 00 00 03 10 10 Visa Debit\nVisa Contactless\nSEO ID: 001:263:007, Autoriz. kód 516885\nNo Pin *NO REFUND*\nCelková sleva 5,90\nB 12% DPH z 250,97 26,89\nC 21% DPH z 49,90 8,66\n0102 027200/081/81 17.08.24 08:37:17\nE = Váha přenesená z čárového kódu EAN\nZáruční a další údaje - zadní strana\nPrůmyslové zboží je možné vrátit na základě\noriginální nebo této elektronické účtenky v\npůvodním (nezávadném) stavu a originálním\nobalu do 30 dní od data nákupu.\nDárkovou kartu není možné vrátit, ani vyměnit.\nLidl Česká republika s.r.o.\nNárožní 1359/11, 158 00 Praha 5\nIČC: 26178541, DIC: CZ2617/8541\nMS Praha, zn. C 392174\nNákup proveden na\nJihlava, Okružní\nOkružní 4967/15\n586 00 Jihlava\nInformace o prodejně").process_billa_receipt()
        result_df_3 = BillaReceipts("mL Jednička v čerstvosti\nProvozovna:\nJihlava, Okružní\nKč\nEmentál plátk. sýr 42,90 B\nČers.mléko 1,5% 11 21,90 B\nSušenky s krémem 42,90 B\nRajčata keříková 35,83 B\nN 0,718 kg x 49,90 Kč/kg\nPT: 0,002 kg\nKornbageta 20,70 B\n3 ks x 6,90 Kč/ks\nPaprika červená 33,03 B\nN 0,662 kg x 49,90 Kč/kg\nPT: 0,002 kg\nK PLATBĚ 197,26\nKarta 197,26\nCelková zaplacená částka 197,26\n15/08/24 15:28 Účtenka číslo 08018\nTerminál: (LI010282-53268102)\nPRODEJ 197.26 Kč\n*kk** *kk*k **k** 5103 / 00 (L) VISA\nA0 00 00 00 03 10 10 Visa Debit\nVisa Contactless\nSEO ID: 001:261:065, Autoriz. kód 806037\nNo Pin *NO REFUND*\n\nB 12% DPH z 197,26 21,14\n0102 029098/082/82 15.08.24 15:26:23\nPT = Předvolená tára\nN = Netto váha\n\nZáruční a další údaje - zadní strana\n\nPrůmyslové zboží je možné vrátit na základě\n\noriginální nebo této elektronické účtenky v\npůvodním (nezávadném) stavu a originálním\nobalu do 30 dní od data nákupu.\nDárkovou kartu není možné vrátit, ani vyměnit.\nLidl Česká republika s.r.o.\nNárožní 1359/11, 158 00 Praha 5\nIČC: 26178541, DIC: CZ2617/8541\nMS Praha, zn. C 392174\nNákup proveden na\nJihlava, Okružní\nOkružní 4967/15\n586 00 Jihlava\nInformace o prodejně").process_billa_receipt()

        test_cases = [
            (result_df_1, expected_df_1),
            (result_df_2, expected_df_2),
            (result_df_3, expected_df_3)
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