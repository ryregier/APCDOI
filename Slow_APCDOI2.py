email = "" #Please entry your email here in between the quotes. This is so the Crossref and OADOI know who is making use of their APIs.
user_currency = "USD"

import urllib.request, urllib.parse, urllib.error
import json
import ssl
import re
import csv
from datetime import datetime
import os

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def grab(x): #returning values and returning "unknown" if value error
    if x is False or x == " " or x == "" or x == "No Information" or x is None:
        return "unknown"
    else:
        try:
            return x
        except:
            return "unknown"

def time(x):
    if x/80 < 1:
        return 1
    else:
        a = int(x/80)
        return a

#fh = open("DOIlist.csv",encoding="utf8")
while True: #opening DOI list
    filename = input("Please file name of the DOI csv list. Make sure it is located in same folder as this python program:\n")
    #filename = "DOIlisttest"
    if len(filename) < 1:
        quit()
    try:
        fh = open(filename,encoding="ISO-8859-1")
        break
    except:
        print ("Can't find the file")
        continue

#print(datetime.now())

doi_list = list() #DOI list to append found dois
Dcount = 0
for item in fh:
    word = item.rstrip()
    word = word.split(",")
    if len(word[0]) > 1: Dcount = Dcount + 1 #counting DOIs
    if Dcount == 1:continue #Skipping first Line which is heading
    if len(word[0]) < 1: word[0] = "No DOI listed"
    doi_list.append(word[0]) #adding DOIs to a DOI list

APCurl = 'https://raw.githubusercontent.com/ryregier/APCPrices/master/APCPrices'

serviceurl = 'https://api.unpaywall.org/v2/'

print (Dcount,"DOIs found. Loading APCprices JSON file for analysis...")
try:
    uh = urllib.request.urlopen(APCurl)
    data = uh.read().decode()
    APCdata = json.loads(data) #loading APCprices json file
    print ("APCPrices JSON file loaded. Beginning analysis. This will likely take around", time(Dcount), "minutes...")
except:
    print ("Error with pulling JSON file from Github")

#doi_list = map(lambda s: s.strip(), doi_list) #Removing \n from DOI list
broken_doi = list()
doi_data = list()

count = 0

for doi in doi_list:
    if count == int(len(doi_list)*0.25): #Giving updates how much longer to go
        print ("25% processed....")
    if count == int(len(doi_list)*0.50):
        print ("50% processed...")
    if count == int(len(doi_list)*0.75):
        print ("75% processed...")
    count = count + 1

    #if count > 5: break
    #print (doi)

    if doi == "No DOI listed": #keeping track of blank DOIs
        doi_dict = {
            "DOI":"No DOI listed",
            "oa_type":"",
            "Document Type":"",
            "Journal":"",
            "publisher":"",
            "Year":"",
            "Source": "",
            "Last Updated":"",
            "currency":"",
            "apc": "",
            "apc_price": "",
            "best_oa_link":"",
            }
        doi_data.append(doi_dict)
        continue

    try:
        unpaywallurl = serviceurl + urllib.parse.quote(doi) + "?email=" + email
        #print('Retrieving', url)
        uh = urllib.request.urlopen(unpaywallurl)
        data = uh.read().decode()
        info = json.loads(data)
        #print ("This article is OA:",info["is_oa"])
        #print ("The article title is:",info["title"])
        #print ("Retrieving", url)
    except:
        #print ("URL Retrieving error")
        broken_doi.append(doi)
        doi_dict = { #returning blank info if DOI can't be found
            "DOI":doi,
            "oa_type":"DOI Error",
            "Document Type":"",
            "Journal":"",
            "publisher":"",
            "Year":"",
            "Source": "",
            "Last Updated":"",
            "currency":"",
            "apc": "",
            "apc_price": "",
            "best_oa_link": ""
            }
        doi_data.append(doi_dict)
        continue

    #print (info['is_oa'])
    #try:
    if info['is_oa'] == True:
        cboolean = grab(info['best_oa_location']["license"])
        #print (cboolean[0:2])
        hboolean = grab(info['best_oa_location']["host_type"])
        #print (hboolean)
        if (cboolean[0:2] == "cc" or cboolean == "implied-oa") and hboolean== "publisher":
            if info["journal_is_oa"] == True:
                oa_type = "Gold"
                process_APC = True
            elif info["journal_is_oa"] == False:
                oa_type = "Hybrid"
                process_APC = True
            else:
                oa_type = "Gold or Hybrid"
                process_APC = True

        elif info['best_oa_location']["host_type"] == "publisher":
            oa_type = "Bronze?"
            process_APC = False
        elif info['best_oa_location']["host_type"] == "repository":
            oa_type = "Green"
            process_APC = False
        else:
            oa_type = "OA, but status unknown"
            process_APC = False

        oa_link = grab(info["best_oa_location"]["url"])


    elif info['is_oa'] == False:
        oa_type = "No OA found"
        oa_link =""
        process_APC = False

    else:
        oa_type = "No OA found"
        oa_link =""
        process_APC = False

    #print(oa_type)

    match = None

    if process_APC is True:
        #print ("process_APC=True")
        for item in APCdata:
            title_match = False
            ISSN_match = False
            if info["journal_name"] == item["journal_title"]:
                title_match = True
                #print ("title_match=true")
            if title_match is not True:
                for APCISSN in item["issn"]:
                    if ISSN_match is True: break
                    if info["journal_issns"] == None: break
                    for DOIISSN in info["journal_issns"].split(","):
                        if APCISSN == DOIISSN:
                            ISSN_match = True
                            #print ("ISSN_match=True")
            if title_match is False and ISSN_match is False:
                match = False
                continue
            elif title_match is True or ISSN_match is True:
                match = True
                Source = item["source_of_apc"]
                Lastupdated = item["last_update"]
                currency = item["currency"]
                apc = item["apc"]
                apc_price = item["apc_price"]
                break

    elif process_APC is False:
                Source = ""
                Lastupdated = ""
                currency = ""
                apc = ""
                apc_price = ""

    if match != False:
        doi_dict = {
            "DOI":doi,
            "oa_type":oa_type,
            "Document Type": grab(info["genre"]),
            "Journal": grab(info["journal_name"]),
            "publisher": grab(info["publisher"]),
            "Year":grab(info["year"]),
            "Source":Source,
            "Last Updated":Lastupdated,
            "currency":currency,
            "apc": apc,
            "apc_price": apc_price,
            "best_oa_link": oa_link
            }
        doi_data.append(doi_dict)

    elif match == False:
        doi_dict = {
            "DOI":doi,
            "oa_type":oa_type,
            "Document Type": grab(info["genre"]),
            "Journal": grab(info["journal_name"]),
            "publisher": grab(info["publisher"]),
            "Year":grab(info["year"]),
            "Source": "No details found",
            "Last Updated":"",
            "currency":"",
            "apc": "",
            "apc_price": "",
            "best_oa_link": oa_link
            }
        doi_data.append(doi_dict)
        #print (count)

#print (doi_data)

currency_fixer = "https://api.fixer.io/latest?base="+user_currency #Calling fixer api to find the right currency
uh = urllib.request.urlopen(currency_fixer)
data = uh.read().decode()
curr_info = json.loads(data)

curr_info = curr_info['rates']

#print (curr_info)

 #t = {'AUD': 1.2592, 'BGN': 1.5692, 'BRL': 3.2344, 'CAD': 1.2506, 'CHF': 0.92434, 'CNY': 6.3444, 'CZK': 20.331, 'DKK': 5.9757, 'EUR': 0.80231, 'GBP': 0.71248, 'HKD': 7.8208, 'HRK': 5.9676, 'HUF': 249.74, 'IDR': 13517.0, 'ILS': 3.5471, 'INR': 64.22, 'ISK': 100.45, 'JPY': 106.18, 'KRW': 1064.9, 'MXN': 18.504, 'MYR': 3.8945, 'NOK': 7.7672, 'NZD': 1.3521, 'PHP': 52.247, 'PLN': 3.3374, 'RON': 3.7408, 'RUB': 56.393, 'SEK': 7.9541, 'SGD': 1.3107, 'THB': 31.29, 'TRY': 3.7535, 'ZAR': 11.66}


def curr_transform(x,y): #changing APC pricing info to the correct currency
    if x == "None" or x == None or x == "" or x == user_currency:
        return y
    else:
        cost = int(y)/curr_info[x]
        return int(cost)

for item in doi_data: #Finding cost in user currency
    item['price_in_user_currency'] = curr_transform(item["currency"],item["apc_price"])


csv_name = "APCDOI - "+filename

myFile = open(csv_name,'w',newline='')
with myFile:
    writer = csv.writer(myFile)
    writer.writerow(['DOI', 'OA Type', 'Journal', 'Publisher', 'Year', 'Source', 'Journal APC', 'Journal Currency', 'APC in '+user_currency,'Last Updated', 'Best OA link'])
    for a in doi_data:
        data2 = [a["DOI"], a["oa_type"], a["Journal"], a["publisher"], a["Year"], a["Source"], a["apc_price"], a["currency"], a['price_in_user_currency'], a["Last Updated"], a["best_oa_link"]]
        writer.writerow(data2)

no_info_count = 0
goldhybrid_count = 0
total_price = 0

for item in doi_data:
    if item["Source"] == "No details found":
        no_info_count = no_info_count + 1
        continue
    if item["oa_type"] == "Gold" or item["oa_type"] == "Hybrid":
        goldhybrid_count = goldhybrid_count + 1
        total_price =total_price + int(item['price_in_user_currency'])

print (goldhybrid_count,"out of", no_info_count+goldhybrid_count,"Gold or Hybrid DOIs were found with APC info.")
print ("The total sum of these being $",total_price,user_currency)
print ("There were",len(broken_doi),"DOI errors")
print (csv_name,"exported with the data.")
os.startfile(csv_name)
#print(datetime.now())
