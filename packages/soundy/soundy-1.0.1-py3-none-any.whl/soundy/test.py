import requests
import re
from bs4 import BeautifulSoup

url = "https://soundcloud.com/leagueoflegends/kda-popstars-ft-madison-beer-gi-dle-jaira-burns"
html = requests.get(url)
soup = BeautifulSoup(html.content, 'html.parser')
soup.find_all('')
print(html.text)
try:
    print(re.search(r'soundcloud://sounds:(.+?)"', html.text).group(1))
except AttributeError:
    print("Invalid SoundCloud track check your connection and/or if you have access to the track!")

# title1= soup.title.string[:-31]

# forbidden_chars = ['<', '>', ':', '"', '/', '\\', '?', '*', '|']
# titles =[]
# titles.append(title1)

# for title in titles:
#     for char in forbidden_chars:
#         if char in title:
#             print("Title got A symbol that will ruin your download...cleaning them up for you wait a second!")
#             titles.append(titles[-1].replace(char ,''))
# print(title1)        
# print(titles[-1])


# img = soup.find('img')
# print(type(img['alt']))
# print(img['alt'])
# print(img['src'])


