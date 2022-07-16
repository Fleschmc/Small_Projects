import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

def run_scraping():

    """
    Link Scraping
    """

    rust_labs_building = 'https://rustlabs.com/group=building-blocks'
    soup = BeautifulSoup(requests.get(rust_labs_building).content, 'html.parser')

    build_links = ['https://rustlabs.com' + soup.find_all('td', class_ = 'left')[_].next['href'] + '#tab=destroyed-by;filter=0,0,1,0,0,0;sort=4,0,2' for _ in range(len(soup.find_all('td', class_ = 'left')))]

    time.sleep(3)
    
    soup = BeautifulSoup(requests.get('https://rustlabs.com/group=build').content, 'html.parser')

    construction_links = ['https://rustlabs.com' + soup.find('div', class_ = 'info-block group').find_all('a')[_]['href'] + '#tab=destroyed-by;filter=0,0,1,0,0,0;sort=4,0,2' for _ in range(len(soup.find('div', class_ = 'info-block group').find_all('a')))]
    
    time.sleep(3)

    soup = BeautifulSoup(requests.get('https://rustlabs.com/group=items').content, 'html.parser')

    item_links = ['https://rustlabs.com' + soup.find('div', class_ = 'info-block group').find_all('a')[_]['href'] + '#tab=destroyed-by;filter=0,0,1,0,0,0;sort=4,0,2' for _ in range(len(soup.find('div', class_ = 'info-block group').find_all('a')))]
    
    time.sleep(3)

    soup = BeautifulSoup(requests.get('https://rustlabs.com/group=traps').content, 'html.parser')

    item_links = ['https://rustlabs.com' + soup.find('div', class_ = 'info-block group').find_all('a')[_]['href'] + '#tab=destroyed-by;filter=0,0,1,0,0,0;sort=4,0,2' for _ in range(len(soup.find('div', class_ = 'info-block group').find_all('a')))]
    
    time.sleep(3)

    soup = BeautifulSoup(requests.get('https://rustlabs.com/group=electrical').content, 'html.parser')

    item_links = ['https://rustlabs.com' + soup.find('div', class_ = 'info-block group').find_all('a')[_]['href'] + '#tab=destroyed-by;filter=0,0,1,0,0,0;sort=4,0,2' for _ in range(len(soup.find('div', class_ = 'info-block group').find_all('a')))]
    
    time.sleep(3)
    """
    Data Scraping
    """
    
    session = requests.Session()

    master = []
    for link_group in [build_links, construction_links, item_links]:

        for link in link_group:
            soup = BeautifulSoup(session.get(link, timeout = (12, 27)).content, 'html.parser')
            
            for explosive in soup.find_all('tr', {'data-group' : 'explosive'}):
                data_dict = {}
                data_dict['Object']   = soup.find('h1').text
                data_dict['tool']     = explosive.find('td', class_ = 'left padding').text.strip().replace('Semi-Automatic Rifle', '').replace('(right click)', '').replace('Stuck', '').replace('Hunting Bow', '')
                data_dict['quantity'] = int(explosive.find('td', class_ = 'no-padding').text.replace('~', '').replace(',', '').strip())
                data_dict['time']     = explosive.find_all('td')[3].text
                data_dict['type']     = 'Explosive'
                data_dict['link']     = link

                master.append(data_dict)
                
            for explosive in soup.find_all('tr', {'data-group' : 'melee'}):
                data_dict = {}
                data_dict['Object']   = soup.find('h1').text
                data_dict['tool']     = explosive.find('td', class_ = 'left padding').text.strip().replace('Semi-Automatic Rifle', '').replace('(right click)', '').replace('Stuck', '').replace('Hunting Bow', '')
                data_dict['quantity'] = int(explosive.find('td', class_ = 'no-padding').text.replace('~', '').replace(',', '').strip())
                data_dict['time']     = explosive.find_all('td')[3].text
                data_dict['type']     = 'Melee'
                data_dict['link']     = link

                master.append(data_dict)

    return pd.DataFrame(master)

if __name__ == '__main__':
    run_scraping().to_csv('./raiding.csv')
