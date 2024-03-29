import socket

import requests
import re
from bs4 import BeautifulSoup as BS
import pandas as pd
from requests.exceptions import Timeout


def clean(word: str) -> str:
    word = re.sub('[^0-9]', ' ', word)
    return word

urls = [
    'https://koko.kz/catalog/litso/gidrofilnye_masla_i_shcherbety/',
         'https://koko.kz/catalog/litso/glaza/',
         'https://koko.kz/catalog/litso/krema_dlya_litsa/',
         'https://koko.kz/catalog/litso/maski/',
         'https://koko.kz/catalog/litso/penki_i_geli_dlya_umyvaniya/',
         'https://koko.kz/catalog/litso/skraby_i_pilingi/',
         'https://koko.kz/catalog/litso/solntsezashchitnye_krema/',
         'https://koko.kz/catalog/litso/tonery/',
         'https://koko.kz/catalog/litso/emulsii/',
         'https://koko.kz/catalog/litso/essentsii_i_syvorotki_dlya_litsa/',
         'https://koko.kz/catalog/telo/geli_dlya_dusha/',
         'https://koko.kz/catalog/telo/dezodoranty/',
         'https://koko.kz/catalog/telo/losony/',
         'https://koko.kz/catalog/telo/nogi/',
         'https://koko.kz/catalog/telo/ruki/',
         'https://koko.kz/catalog/telo/skraby_dlya_tela/',
         'https://koko.kz/catalog/telo/universalnye_geli/',
         'https://koko.kz/catalog/telo/ukhod_za_polostyu_rta/',
         'https://koko.kz/catalog/volosy/balzamy_i_konditsionery_dlya_volos/',
         'https://koko.kz/catalog/volosy/kraski_dlya_volos/',
         'https://koko.kz/catalog/volosy/maski_dlya_volos/',
         'https://koko.kz/catalog/volosy/sprei_dlya_volos/',
         'https://koko.kz/catalog/volosy/shampuni/',
         'https://koko.kz/catalog/aksessuary/sponzhi_dlya_bb_kremov/',
         'https://koko.kz/catalog/dekorativnaya_kosmetika/bb_cc_krema/',
         'https://koko.kz/catalog/dekorativnaya_kosmetika/kushony/',
         'https://koko.kz/catalog/dekorativnaya_kosmetika/tinty_dlya_gub/',
         'https://koko.kz/catalog/nabory/']

df = pd.DataFrame({'name': [], 'priceDM': [], 'sale_price': [],'sku': [], 'category': [], 'img': [], 'desc': []})
page_lst = []
path = 'C:/Users/Jean/Desktop/test/koko_parsed_prices.xlsx'  # 37 symbol
for url in urls:
    start_url = f"{url}?PAGEN_1=1"
    category = url[23:]
    res = requests.get(url,cookies={'current_region':'6277'})
    htmlData = res.content
    parsedData = BS(htmlData, "html.parser")
    print('start URL =>',start_url)
    pages = parsedData.find_all(class_='nums')
    if pages:
        pages = pages[0].text.split()
        pages = int(pages[-1])
    else:
        #print(pages)
        pages = 1

    k = 1
    while k <= pages:
        cycle_url = url + "?PAGEN_1=" + str(k)
        print('page', str(k), '=>', cycle_url)
        k += 1
        res = requests.get(cycle_url, cookies={'current_region': '6277'})
        htmlData = res.content
        parsedData = BS(htmlData, "html.parser")
        lst = []
        a = parsedData.find_all(class_='inner_wrap TYPE_1')
        for i in a:
            href = i.find('a')
            #print(href['href'])
            desc_url = 'https://koko.kz' + href['href']
            print(desc_url)
            for retry in range(3):
                try:
                    res = requests.get(desc_url, cookies={'current_region': '6277'}, timeout=10)
                    htmlData = res.content
                    parsedData = BS(htmlData, "html.parser")
                    desc = parsedData.find_all('div',class_='content')
                    try:
                        desc = desc[0].text
                    except IndexError:
                        print('No description exists')
                        desc = '-'
                        break

                    break
                except Timeout:
                    print(f'Error. Retry # {retry+1}')

            img = i.find('img').get('data-src')
            img = 'https://koko.kz' + img
            sku = re.sub('[^0-9]', ' ', href['href']).rstrip().lstrip()
            #print(href['href'])
            res = i.find_all(attrs={"class": {"item-title", "price_value"}})
            lst.append({'name': res[0].text.rstrip().lstrip(),
                        'priceDM': re.sub('[^0-9]', ' ', res[1].text),
                        'sale_price': '-',
                        'sku': sku,
                        'category': category,
                        'img': img,
                        'desc': desc})

        page_df = pd.DataFrame(lst)
        df = pd.concat([df, page_df])

df.to_excel(path, index=False)
