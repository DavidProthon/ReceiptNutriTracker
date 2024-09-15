
 # Vítejte v aplikaci ReceiptNutriTracker

 ## O aplikaci

Aplikace slouží ke zpracování účtenek ze supermarketů (aktuálně je podpora pro obchody Albert a Lidl). 
Z každé účtenky získá data o nakoupených položkách, množství, ceně a data nákupu. K těmto položkám scrapuje výživové hodnoty ze stránky www.kaloricketabulky.cz.
Aplikace je navržena tak, aby uživatelům pomohla sledovat výživové informace a výdaje na základě položek, které nakoupí.
            
Součástí této volně přístupné verze není možnost scrapování dat. Aplikace již obsahuje data některých položek v databázi projekt_data.db. 
Položky z vašich účtenek, které nejsou v databázi se vygenerují do souboru "Nezpracované položky.xlsx" po zmáčknutí tlačítka "Zpracuj účtenky" v sekci aplikace "Zpracování účtenek". 

Pokud máte zájem o přidání položek do databáze, vyplňte soubor 'Nezpracované položky.xlsx' a zašlete ho na adresu EMAIL. 
K zaslaným položkám získám data pomocí scrapingu a aktualizuji repozitář GitHubu tohoto projektu."

#### Postup pro vyplnění souboru "Nezpracované položky.xlsx"
            
Soubor obsahuje 4 sloupce.             
V prvním sloupci je vygenerovaný název položky z účtenek, tento sloupec neměňte.           
Do druhého sloupce přidejte url odkaz na položku ze stránky "www.kaloricketabulky.cz"          
Do třetího sloupce přidejte velikost balení v gramech. Pokuď je velikost balení různorodá (např. u potravin, které jdou při nákupu na váhu), tak do kolonky napiště 1000.
Do čtvrtého sloupce vyberte a napište druh potraviny z tohoto výběru:
maso, masné výrobky, ryby, vejce, mléko a mléčné výrobky, obiloviny, ovoce, zelenina, průmyslově zpracované potraviny, ostatní

#### Příklad vyplněné tabulky:

sample_data = [
    {"Položka": "PAPRIKA ČERVENÁ_Albert", "Odkaz": "https://www.kaloricketabulky.cz/potraviny/paprika-cervena", "Velikost_balení": 1000,"Druh_potraviny": "zelenina"},
    {"Položka": "MLYNÁŘSKÁ VEKA 400G_Albert", "Odkaz": "https://www.kaloricketabulky.cz/potraviny/mlynarska-zitna-veka-albertovo-pekarstvi", "Velikost_balení": 400,"Druh_potraviny": "obiloviny"},
]

df = pd.DataFrame(sample_data)
html_table = df.to_html(index=False)
st.markdown(html_table, unsafe_allow_html=True)

## Co aplikace nabízí
### V sekci 'Ceny'

Zde vyberete libovolné položky, které vás zajímají.
První graf zobrazuje, kolik stála položka v čase nákupu.
Druhý graf zobrazuje cenu přepočtenou na 100g.
        
![Ukázka aplikace](./images/prices.png)         

### V sekci 'Makroživiny' 

Zde naleznete 3 sloupcové grafy.           
První zobrazuje průměrné množství makroživin za den v gramech pro jednotlivé měsíce.            
Druhý zobrazuje průměrné množství makroživin za den v kcal pro jednotlivé měsíce.            
Třetí zobrazuje procentuální podíl příjmu energie z makroživin za den pro jednotlivé měsíce.
      
st.image('./images/macronutriens_1.png', use_column_width=True)
st.image('./images/macronutriens_2.png', use_column_width=True)

### V sekci 'Množství jídla' 
   
Zde vyberete libovolné položky, které vás zajímají.
Graf zobrazuje průměrné množství vybraných druhů potravin na den v jednotlivých měsících[g].         
     
st.image('./images/amount_of_food.png', use_column_width=True)

## Instalace

## License

Tento projekt je licencován pod MIT licencí.
 

## Kontakt a pár slov na závěr

Aplikace je momentálně ve vývoji a může obsahovat chyby.
Pokud na nějakou narazíte, nebo máte zájem o přidání nové funkcionality, napište na adresu EMAIL, případně rovnou zašlete Pull Request.
Doufám, že se vám aplikace bude líbit a najdete pro ni využití.
Každý, kdo by se chtěl připojit k vývoji, je vítán.

S pozdravem,            
DavidProthon    
