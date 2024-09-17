
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

| Položka                    | Odkaz                                                                              | Velikost_balení  | Druh_potraviny  |
| :-------------------------:| :---------------------------------------------------------------------------------:| :---------------:| :-------------: |
| PAPRIKA ČERVENÁ_Albert     | https://www.kaloricketabulky.cz/potraviny/paprika-cervena                          | 1000             |  zelenina       |
| MLYNÁŘSKÁ VEKA 400G_Albert | https://www.kaloricketabulky.cz/potraviny/mlynarska-zitna-veka-albertovo-pekarstvi | 400              |  obiloviny      |


## Co aplikace nabízí
### V sekci 'Ceny'

Zde vyberete libovolné položky, které vás zajímají.
První graf zobrazuje, kolik stála položka v čase nákupu.
Druhý graf zobrazuje cenu přepočtenou na 100g.
        
![](./images/prices.png)         

### V sekci 'Makroživiny' 

Zde naleznete 3 sloupcové grafy.           
První zobrazuje průměrné množství makroživin za den v gramech pro jednotlivé měsíce.            
Druhý zobrazuje průměrné množství makroživin za den v kcal pro jednotlivé měsíce.            
Třetí zobrazuje procentuální podíl příjmu energie z makroživin za den pro jednotlivé měsíce.

![](./images/macronutriens_1.png)
![](./images/macronutriens_2.png)

### V sekci 'Množství jídla' 
   
Zde vyberete libovolné položky, které vás zajímají.
Graf zobrazuje průměrné množství vybraných druhů potravin na den v jednotlivých měsících[g].         

![](./images/amount_of_food.png)

## Instalace

# Postup pro windows
Nejdříve je potřeba nainstalovat git, pokuď ho nemáte (to si ověříte tak, že do terminálu zadáte příkaz `git --version`)
Pokuď ho nemáte, jděte na oficiální stránku Git `https://git-scm.com/downloads`
Git můžete nainstalvoat kam chcete, ale je důležité zaškrtnout tlačítko `Git from the command line and also from 3rd-party software` při instalaci.

Pomocí příkazu `git clone https://github.com/DavidProthon/ReceiptNutriTracker.git` si naklonujte repozitář do svého počítače.
Přejděte do složky projektu a vytvořte si zde virtuální prostředí. `python -m venv venv` a aktivujte příkazem `.\venv\Scripts\activate`


## Licence

Tento projekt je licencován pod MIT licencí.
 

## Kontakt a pár slov na závěr

Aplikace je momentálně ve vývoji a může obsahovat chyby.
Pokud na nějakou narazíte, nebo máte zájem o přidání nové funkcionality, napište na adresu EMAIL, případně rovnou zašlete Pull Request.
Doufám, že se vám aplikace bude líbit a najdete pro ni využití.
Každý, kdo by se chtěl připojit k vývoji, je vítán.

S pozdravem,            
DavidProthon    
