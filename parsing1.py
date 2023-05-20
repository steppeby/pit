import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

urls = ['https://dinamarket.kz/ru/111/produkty/','https://dinamarket.kz/ru/111/Sredstva_gigiyeny_i_krasota/',
        'https://dinamarket.kz/ru/111/Bytovaya_khimiya/','https://dinamarket.kz/ru/111/tovary_dlya_doma/',
        'https://dinamarket.kz/ru/111/posuda_i_prinadlezhnosti/', 'https://dinamarket.kz/ru/111/avtotovary/',
        'https://dinamarket.kz/ru/111/zootovary/','https://dinamarket.kz/ru/111/Igrushki_prazdniki/',
        'https://dinamarket.kz/ru/111/kantstovary/','https://dinamarket.kz/ru/111/Odezhda_obuv_tekstil/',
        'https://dinamarket.kz/ru/111/Sad_i_dacha/','https://dinamarket.kz/ru/111/sport_i_otdykh/',
        'https://dinamarket.kz/ru/111/elektronika_i_tekhnika/'
        ]
for url in urls:
    path = 'C:/******/*****' + url[29:-1] + '.xlsx'
    url += '?lim=99999' #?lim=9999
    res = requests.get(url)
    htmlData = res.content
    parsedData = BS(htmlData, "html.parser")

    df = pd.DataFrame({'Название': [],  'Цена по скидке': [], 'Цена без скидки': []})
    a=parsedData.find_all(class_ = 'cont')
    for i in a:
        res = i.find_all(attrs={"class":{"old","new","title"}})
        df = df.append({'Название': res[0].text.rstrip('\n').lstrip('\n'), 'Цена по скидке': res[1].text, 'Цена без скидки': res[2].text}, ignore_index=True)

    df.to_excel (path, index= False )



