import requests
import re
from bs4 import BeautifulSoup as BS
import pandas as pd
from requests.exceptions import Timeout
import chime
import time

def get_clean_word(word: str) -> str:
    word = re.sub('[^0-9a-zA-Zа-яА-ЯёЁ]', ' ', word, flags=re.IGNORECASE)
    word = word.strip('-')
    return word

urls = [
        'http://detmir.kz/catalog/index/name/slides_swimming/',
        'http://detmir.kz/catalog/index/name/towels/',
        'http://detmir.kz/catalog/index/name/angles_sets_swimming/',
        'http://detmir.kz/catalog/index/name/seats_hammocks_swimming/',
        'http://detmir.kz/catalog/index/name/sponges_washcloths/',
        'http://detmir.kz/catalog/index/name/toys_tub_accessories/',
        'http://detmir.kz/catalog/index/name/circles_vests_mattresses_swimming/',
        'http://detmir.kz/catalog/index/name/aspirators/',
        'http://detmir.kz/catalog/index/name/bathing_cosmetics/',
        'http://detmir.kz/catalog/index/name/sun_cream/',
        'http://detmir.kz/catalog/index/name/insects_protection/',
        'http://detmir.kz/catalog/index/name/cotton_products/',
        'http://detmir.kz/catalog/index/name/care_babys_skin/',
        'http://detmir.kz/catalog/index/name/manicure_sets/',
        'http://detmir.kz/catalog/index/name/winter_cosmetics/',
        'http://detmir.kz/catalog/index/name/soaps/',
        'http://detmir.kz/catalog/index/name/dental_care/',
        'http://detmir.kz/catalog/index/name/atopic_skin/',
        'http://detmir.kz/catalog/index/name/household_chemicals/',
        'http://detmir.kz/catalog/index/name/podguzniki/',
        'http://detmir.kz/catalog/index/name/diapers_pants/',
        'http://detmir.kz/catalog/index/name/diapers_swimming/',
        'http://detmir.kz/catalog/index/name/disposable_diapers/',
        'http://detmir.kz/catalog/index/name/napkin_paper/',
        'http://detmir.kz/catalog/index/name/toilet_paper_wet_dry/',
        'http://detmir.kz/catalog/index/name/powder_cream_diaper/',
        'http://detmir.kz/catalog/index/name/cases_dummies/',
        'http://detmir.kz/catalog/index/name/teethers/',
        'http://detmir.kz/catalog/index/name/holders_pacifiers/',
        'http://detmir.kz/catalog/index/name/dummy/',
        'http://detmir.kz/catalog/index/name/nimbler_tips/',
        'http://detmir.kz/catalog/index/name/slunyavchiki/',
        'http://detmir.kz/catalog/index/name/aksessuary_dlya_kormleniya/',
        'http://detmir.kz/catalog/index/name/brushes_brushes/',
        'http://detmir.kz/catalog/index/name/replaceable_accessories_drinking_bowls/',
        'http://detmir.kz/catalog/index/name/baby_bottles/',
        'http://detmir.kz/catalog/index/name/drinking_bowl/',
        'http://detmir.kz/catalog/index/name/baby_dishes_cutlery/',
        'http://detmir.kz/catalog/index/name/bottles_cups/',
        'http://detmir.kz/catalog/index/name/baby_dishes_cutlery/',
        "http://detmir.kz/catalog/index/name/pure/",
        "http://detmir.kz/catalog/index/name/chai/",
        "http://detmir.kz/catalog/index/name/fruchtgetranke/",
        "http://detmir.kz/catalog/index/name/grocery/",
        "http://detmir.kz/catalog/index/name/suhie_smesi_i_zameniteli_moloka/",
        "http://detmir.kz/catalog/index/name/kashi/",
        "http://detmir.kz/catalog/index/name/milk_shakes/",
        "http://detmir.kz/catalog/index/name/deserty/",
        "http://detmir.kz/catalog/index/name/pravilnoe_pitanie/"]

df = pd.DataFrame({'name': [], 'priceDM': [], 'sale_price': [],'sku': []})
page_lst = []
path = 'C:/Users/Jean/Desktop/test/detskiy_mir_data.xlsx'  # 37 symbol
for url in urls:
    start_url = f"{url}page/1/?filter=price:1%2C999999;stores:3107%2C3396"
    res = requests.get(url,cookies={'geoCityDMIso':'KZ-AKT'})
    htmlData = res.content
    parsedData = BS(htmlData, "html.parser")
    print('start URL =>',start_url)

    group = parsedData.find_all('li',class_='Lp')
    group_name = ''
    for i in group:
        group_name += i.text + '>'
    group_name = group_name.rstrip('>')

    k = 1
    while not parsedData.find_all('p',class_='Wb'):
        cycle_url = url + "page/" + str(k) + "/?filter=price:1%2C999999;stores:3107%2C3396"
        print('page',str(k),'=>',cycle_url)
        k += 1
        res = requests.get(cycle_url,cookies={'geoCityDMIso':'KZ-AKT'})
        htmlData = res.content
        parsedData = BS(htmlData,"html.parser")
        lst = []
        a = parsedData.find_all(class_='Ju Jy x_0')
        for i in a:
            href = i.find('a')
            picture = i.find('img',class_='lM lO lN')
            desc_url = href['href']
            print(desc_url)
            for retry in range(3):
                try:
                    res = requests.get(desc_url, cookies={'geoCityDMIso':'KZ-AKT'}, timeout=10)
                    htmlData = res.content
                    parsedData = BS(htmlData, "html.parser")
                    desc = parsedData.find_all('div', class_='_0a')
                    try:
                        desc = desc[0].text
                    except IndexError:
                        print('No description exists')
                        desc = '-'
                        break
                    break
                except Timeout:
                    print(f'Error. Retry # {retry + 1}')

            sku = re.sub('[^0-9]', ' ', href['href']).rstrip().lstrip()
            res = i.find_all(attrs={"class":{"biJ","biH","Jw"}})

            if len(res) == 3:
                lst.append({'name': get_clean_word(res[2].text),
                            'priceDM': get_clean_word(res[1].text),
                            'sale_price': get_clean_word(res[0].text),
                            'picture': picture['src'],
                            'product_category': group_name,
                            'sku': sku,
                            'description': desc})
            elif len(res) == 2:
                lst.append({'name': get_clean_word(res[1].text),
                            'priceDM': get_clean_word(res[0].text),
                            'sale_price': '-',
                            'picture': picture['src'],
                            'product_category': group_name,
                            'sku': sku,
                            'description': desc})
            else:
                break

        page_df = pd.DataFrame(lst)
        df = pd.concat([df,page_df])

df.to_excel(path, index=False,engine='xlsxwriter')

chime.success()
time.sleep(2)
