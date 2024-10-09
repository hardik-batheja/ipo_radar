import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
# pip install python-Levenshtein
# pip install fuzzywuzzy
from fuzzywuzzy import fuzz


def extractor(showme = False):
   allot = "https://www.moneycontrol.com/ipo/"
   chrome_options = Options()
   chrome_options.add_argument("--headless")  # Use headless mode
   chrome_options.add_argument("--disable-gpu")
   chrome_options.add_argument("--no-sandbox")  # Required by some cloud services
   chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

   driver = webdriver.Chrome(options=chrome_options)  # Use headless Chrome
   driver.get(allot)

   # Find the button element using its containing div
   for retry in range(10):
      try:
         wait = WebDriverWait(driver, 8)  # Adjust timeout as needed
         parent_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.showmore_showMoreBtnWraps__z9VTS ")))
         # Now, find the button inside the parent div
         button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.showmore_showMoreBtnWraps__z9VTS button.showmore_showMoreBtn__uaC0V")))
         # Click the button
         button.click()
         # Optionally, wait until the button or the parent div becomes invisible
         wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.showmore_showMoreBtnWraps__z9VTS button.showmore_showMoreBtn__uaC0V")))
         break
      except:
         print("retrying.....")
         continue
   page_content = driver.page_source
   driver.quit()
      # Parse the HTML content
   soup = BeautifulSoup(page_content, 'html.parser')
   df1 = pd.DataFrame(columns=['Company', 'Closing', 'Allotment', 'Type', 'Price', 'Qty.', 'QI', 'RI', 'NI', 'Total Subs'])

   for ipo in soup.select('div[class*="OpenUpcomingIpoSec_web_ipoInfoCardHolder"]'):
      ipotype = ipo.select('button[class*="OpenUpcomingIpoSec_web_ipoCatName"]')[0].text[:4].strip()
      title = ipo.select_one('h2').text[:-4].strip(" Ltd").title()
      details = ipo.select_one('div[class*="OpenUpcomingIpoSec_web_ipoInfoBoxWrap"]')
      details =  details.select('td')
      dates = ipo.select('span')
      df1.loc[len(df1)] = [title, details[3].text[:-6], dates[-6].text[:-6], ipotype, details[5].text.split()[-1],
                           details[7].text, details[15].text, details[17].text, details[19].text, details[23].text]
   df1['Closing'] = pd.to_datetime(df1['Closing'], format='%d %b').dt.strftime('%d %b')
   df1 = df1.sort_values(by='Closing')
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
         dfx.loc[len(dfx)] = [comp_temp.title(), row[2].text[1:].strip(), row[1].text, pd.to_numeric(row[3].text[:-1].replace('-','0')), row[4].text, type_temp.rstrip(")")]
      dfx['Type'] = dfx['Type'].replace({"Mainline":"Main","NSE SME":"SME","BSE SME":"SME"})

      rows = tables[1].find_all('tr')
      dfx2 = pd.DataFrame(columns = ['Company', 'Sauda'])
      for row in rows[1:]:
         row = row.find_all('td')
         dfx2.loc[len(dfx2)] = [row[0].text.split(" (")[0].title(), row[2].text]
      
      dfx = pd.merge(dfx, dfx2, on = "Company", how="outer")
      dfx = dfx.sort_values(by=['Type', 'Gain(%)'], ascending=[True, False]).reset_index(drop=True)
      # print (dfx)

      for i,a in enumerate(dfx['Company']):
         for b in df1['Company']:
            if fuzz.partial_ratio(a,b) > 70:
               dfx.at[i,'Company'] = b
      # df1.drop(['Closing'], axis=1, inplace=True)
      dfx = pd.merge(dfx, df1, on = ["Company", 'Type', 'Price'], how = 'outer').drop(['Closing'], axis=1)
      dfx = dfx.sort_values(by=['Type', 'Gain(%)'], ascending=[True, False]).reset_index(drop=True)
      showme and print(dfx)
      # dfx.to_csv('output.csv', encoding='utf-8', index=False)
   else:
      print("Status Code:", response.status_code)
   return dfx

#extractor(True)
