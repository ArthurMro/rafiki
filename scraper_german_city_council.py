
import pandas as pd
import requests, re
from bs4 import BeautifulSoup

page = requests.get("http://www.staedtetag.de/mitglieder/index.html")
soup = BeautifulSoup(page.content, "html.parser")

cities_link=[]
cities_name=[]

for x in soup.tbody.find_all('td',class_='first'):
    cities_link += [x.find('a').get('href')]
    cities_name += [x.text]

print ("dataframe creation")

list_cities = pd.DataFrame(
    {"cities_name": cities_name,
     "cities_link": cities_link,})

#print (list_cities)
print ("INFO: finished getting list")
print ("take a breath, the funnny part is starting....")


def getSoup(url):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")
  return soup


def findATag(soup):
  # Find a tag with this keyword
  res = soup.find("a", text="Impressum")
  if res == None:
    res = soup.find("a", text = "impressum")
  if res == None:
    res = soup.find("a", text = "IMPRESSUM")
  if res == None:
    allATags = soup.findAll("a")
    for i in allATags:

      if i.text.strip() in ["Impressum", "impressum", "IMPRESSUM"]:
        res = i
  return res

def getEmails(url):
    try:
        soup = getSoup(url)
        text = soup.text
        match = re.findall(r'[\w\.-]+@[\w\.-]+', text)
        return match
    except:
        print("Error while email fetch")
        return []

def makeUrl(cityLink, href):
    #Concat url
    if cityLink[-1] == "/":
        if href[0] == "/":
            finalUrl = cityLink + href[1:]
        else:
            finalUrl = cityLink + href
    else:
        if href[0] == "/":
            finalUrl = cityLink + href[1:]
        else:
            finalUrl = cityLink + "/" + href
    return finalUrl

urls = []
# Iterate over cities dataframe
for i in range(list_cities.shape[0]):
    if i % 5 == 0:
        print(f"Processed {i} urls")
    # Try to get soup for that city link
    try:
        soup = getSoup(list_cities.iloc[i].cities_link)
    except:
        continue

    # Get a tag with Impressum keyword
    res = findATag(soup)
    link  = list_cities.iloc[i].cities_link
    siteTitle = " ".join([a for a in link.split('.')[1].split("-")]).title()

    # If cannot find a tag with that keyword
    if res == None:
        pass
    else:
        # Found a tag with keyowrd
        if res["href"][:4] == "http":
            # if its is simply complete url
            urls.append([siteTitle, link] + getEmails(res["href"]))
        else:
            # We have to create url
            cityLink = list_cities.iloc[i].cities_link
            # Create final url
            finalUrl = makeUrl(cityLink, res["href"])
            # Add to list
            urls.append([siteTitle, link] + getEmails(finalUrl))

finalDF = pd.DataFrame(urls)
print("Here we are!")
finalDF.to_csv("final_emails.csv")
