import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
# pip install python-Levenshtein
# pip install fuzzywuzzy
from fuzzywuzzy import fuzz


def extractor(showme = False):
   subs = "https://www.investorgain.com/report/ipo-subscription-live/333/"
   page_content = requests.get(subs).text
   # Parse the HTML content
   soup1 = BeautifulSoup(page_content, 'html.parser')
   table = soup1.find_all('table', class_ = 'table')[0]
   rows = table.find_all('tr')
   df1 = pd.DataFrame(columns = ['Company', 'Price', 'Qty', 'P/E', 'QIB', 'SHNI', 'BHNI', 'NII', 'RII', 'Total', 'Closing', 'Type'])
   for row in rows[1:]:
      row = row.find_all('td')
      c = row[0].text.split("GMP")[0]
      df1.loc[len(df1)] = [c[:-4], row[3].text, row[4].text, row[5].text, row[6].text, row[7].text,
                            row[8].text, row[9].text, row[10].text, row[11].text, row[12].text, "Main" if c[-3:] == "IPO" else c[-3:]]
   # print(df1)

   gmp = "https://ipowatch.in/ipo-grey-market-premium-latest-ipo-gmp/"
   response = requests.get(gmp)

   if response.status_code == 200:
      soupg = BeautifulSoup(response.text, 'html.parser')
      tables = soupg.find_all('figure', class_ = 'wp-block-table')

      rows = tables[0].find_all('tr')
      dfx = pd.DataFrame(columns = ['Company', 'Price', 'GMP', 'Gain(%)', 'Date', 'Type'])
      for row in rows[1:]:
         row = row.find_all('td')
         comp_temp,type_temp = row[0].text.split(" (")
         dfx.loc[len(dfx)] = [comp_temp.title(), row[2].text[1:].strip(), row[1].text, pd.to_numeric(row[3].text[:-1].replace('-','0')), row[5].text, type_temp.rstrip(")")]
      dfx['Type'] = dfx['Type'].replace({"Mainline":"Main","NSE SME":"SME","BSE SME":"SME"})

      rows = tables[1].find_all('tr')
      dfx2 = pd.DataFrame(columns = ['Company', 'Sauda'])
      for row in rows[1:]:
         row = row.find_all('td')
         dfx2.loc[len(dfx2)] = [row[0].text.split(" (")[0].title(), row[2].text]
      # print (dfx2)
      
      dfx = pd.merge(dfx, dfx2, on = "Company", how="outer")
      dfx = dfx.sort_values(by=['Type', 'Gain(%)'], ascending=[True, False]).reset_index(drop=True)
      # print (dfx)

      for i,a in enumerate(dfx['Company']):
         for b in df1['Company']:
            if fuzz.partial_ratio(a,b) > 70:
               dfx.at[i,'Company'] = b
      dfx = pd.merge(dfx, df1, on = ["Company", 'Type', 'Price'], how = 'outer')
      dfx = dfx.sort_values(by=['Type', 'Gain(%)'], ascending=[True, False]).reset_index(drop=True)
      showme and print(dfx)
      # dfx.to_csv('output.csv', encoding='utf-8', index=False)
   else:
      print("Status Code:", response.status_code)
   return dfx

#extractor(True)
