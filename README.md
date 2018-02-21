# APCDOI.py
This is a python program for which you can enter a list of DOIs in a csv file and it will make use of the [Unpaywall API](http://unpaywall.org/api/v2) and a [JSON file of Article Proccessing Charges (APCs)](https://github.com/ryregier/APCPrices) that I have assembled to find out what journal articles are Gold or Hybrid open access and how much the APC for each of these articles are.

## APCDOI.py for those without programming experience

The APICDOI program can be used by those unfamilar with python or programing. Four key steps need to be followed:
  1. [Download Python 3](https://www.python.org/downloads/)
  2. Copy and paste the program code to a [text editor](https://en.wikipedia.org/wiki/Text_editor) (e.g. Notepad) and make sure it is saved as a ".py" program (e.g. APICDOI.py)
  3. Open and edit (e.g. Right click and select "Open with") the firstline of the code in the text editor to add your email. (e.g. email = "ryan@email.com")
  4. Open and run the code with the Python intrepreter (i.e. IDLE)
  
Your email is required so that Unpaywall can keep an idea how their API is being used and can contact you if any overuse or problems. This is a standard practice with most free and public APIs these days.

## Using APCDOI.py
If don't add you email to the first line, the program will not run, so be sure to do this.

Also you will notice on line 2 that the currency defaults to USD. If you want to change the currency, just replace USD with the three letter shortform of the currency you want to use. (e.g. user_currency = "CDN")

Three important things to take note of when importing the csv file:
  1. **Please make sure the DOIs are in the first column**. See the [example_import.csv](https://github.com/ryregier/APCDOI/blob/master/example_import.csv) for an example.
  2. APCDOI also **assumes the first line will be a header**, so it will not include it in the analysis. Do not include a DOI in the top cell.
  3. Make sure the csv file is saved in the **same folder** as APCDOI.py
  
When you run the program, the first line will prompt you to enter the filename. Please make sure to include the ".csv" on the end:
  >Please file name of the DOI csv list. Make sure it is located in same folder as this python program:
  
  > DOIlist.csv

It will then import the APCPrices JSON file for analysis, tell you how many DOIs are found, and give you a time estimate for completion:
  > APCPrices JSON file loaded. Beginning analysis...
  
  > 1345 DOIs found. This should take about 1 minute per 1000 DOIs depending on speed of your computer
  
Currently it is about 1 minute for every 1000 DOIs...but this depends on the speed of your computer!

When completed, it will return the following information and automatically open a csv file with the analysis:
  > 100 out of 110 Gold or Hybrid DOIs were found with APC info.
  
  > The total sum of these being $ 30578 USD
  
  > There were 2 DOI errors
 
 For the format of the exported csv file, please look at [example_export.csv](https://github.com/ryregier/APCDOI/blob/master/example_export.csv)
 
## Potential Issues
My [APCPrices file](https://github.com/ryregier/APCPrices) doesn't have information for all journals unfortunately, so it will miss some of them.

The Gold/Hybrid determination is made based on the Unpaywall data using the below definitions:
- Gold: Published in a fully open access journal.
- Hybrid: Available open access on publisher website AND that has an open copyright statement.
- Bronze: Available open access on publisher website BUT has **no** open copyright statement (i.e. Delayed open access journals)
- Green: Available open access on a non-publisher website

**Please Note**: Some items labelled as Bronze may actually be Hybrid or Gold, unfortunately there is no way to tell for sure based on the metadata available. For more information about the struggles with Bronze OA I suggest reading [this study](https://peerj.com/articles/4375/)

The currency conversion is also based on the current exchange rates of each currency. So if you are looking at an article published in 2006 and the journal's apc is listed in EUR, the exchange rate to USD will not produce the actual cost of item because the exchange rate was likely different back then.
