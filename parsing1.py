import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

url = "https://dinamarket.kz/ru/111/produkty/?lim=99999" #?lim=9999
path = 'C:/Users/qwerty/Desktop/парс/my_data.xlsx'
res = requests.get(url)
htmlData = res.content
parsedData = BS(htmlData, "html.parser")

df = pd.DataFrame({'Название': [],  'Цена по скидке': [], 'Цена без скидки': []})
a=parsedData.find_all(class_ = 'cont')
for i in a:
    res = i.find_all(attrs={"class":{"old","new","title"}})
    df = df.append({'Название': res[0].text.rstrip('\n').lstrip('\n'), 'Цена по скидке': res[1].text, 'Цена без скидки': res[2].text}, ignore_index=True)

df.to_excel (path, index= False )



