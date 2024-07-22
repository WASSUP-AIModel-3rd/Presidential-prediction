# !pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm, trange
import pandas as pd
import argparse



# parser = argparse.ArgumentParser()
# parser.add_argument('--url',help="url from which to crawl")
# parser.add_argument('--out','--output','--outfile',help='filename to save results in ')

def crawl_nomination_speech(url="https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/party-platforms-and-nominating-conventions-2", save=False, save_path='./speech.csv'):
    main_url = url
    html = requests.get(main_url)

    soup = BeautifulSoup(html.text, 'lxml')

    speech_list = {'name': [], 'date': [], 'speech': []}
    page_list = soup.select_one("#block-system-main > div > div > div > div.field-body > table")

    for link in tqdm(page_list.find_all('a', href=True)):
        if link['href'] == main_url:
            continue
        
        page = requests.get(link['href'])
        page_soup = BeautifulSoup(page.text,'lxml')
        date = page_soup.select_one('#block-system-main > div > div > div.col-sm-8 > div.field-docs-start-date-time > span')
        content = page_soup.select_one('#block-system-main > div > div > div.col-sm-8 > div.field-docs-content')
        
        speech = [t.text for t in content.find_all('p')]
        speech_list['name'].append(link.text)
        speech_list['date'].append(date.text)
        speech_list['speech'].append(speech)
    
    speech_df = pd.DataFrame(speech_list)

    if save:
        speech_df.to_csv(save_path)
        
    return speech_df

def crawl_campaign_speech(url="https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/documents-related-to-presidential-elections/2016/report/200320/all/63/205", year=2024, save=False, save_path='./campaign_speech.csv'):
    main_url = url
    speech_list = {'name': [], 'date': [], 'speech': []}

    while main_url:
        html = requests.get(main_url)

        soup = BeautifulSoup(html.text, 'lxml')

        page_list = soup.select_one("#block-system-main > div > div.view-content > div > table").find('tbody')

        for row in tqdm(page_list.find_all('tr')):
            name = row.find('td', 'views-field views-field-title-1 nowrap').text
            name = name.replace('\n','')
            date = row.find('td', 'nowrap').find('span').text.rstrip()
            if (year - int(date[-4:])) < 0 or (year - int(date[-4:]) >= 4):
                continue

            link = row.find('a', href=True)
            if 'Press Release' in link.text:
                continue

            link = "https://www.presidency.ucsb.edu" + link["href"]
            if link == main_url:
                continue
            
            page = requests.get(link)
            page_soup = BeautifulSoup(page.text,'lxml')
            date = page_soup.select_one('#block-system-main > div > div > div.col-sm-8 > div.field-docs-start-date-time > span')
            content = page_soup.select_one('#block-system-main > div > div > div.col-sm-8 > div.field-docs-content')
            
            speech = [t.text for t in content.find_all('p')]
            speech_list['name'].append(name)
            speech_list['date'].append(date.text)
            speech_list['speech'].append(speech)
        
        pages = soup.select_one("#block-system-main > div > div.text-center > ul")
        main_url = None
        if pages:
            active_page = pages.find('li','active').find('span').text
            for page in pages.find_all('a', href=True):
                if page.text.isnumeric() and (int(page.text) == int(active_page)+1):
                    main_url = "https://www.presidency.ucsb.edu" + page["href"]
                    break

    speech_df = pd.DataFrame(speech_list)

    if save:
        speech_df.to_csv(save_path)
        
    return speech_df

def crawl_campaign_speech_from_search(url="https://www.presidency.ucsb.edu/advanced-search?field-keywords=&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=200299&items_per_page=25&f%5B0%5D=field_docs_attributes%3A205", year=2024, save=False, save_path='./campaign_speech.csv'):
    main_url = url
    speech_list = {'name': [], 'date': [], 'speech': []}

    while main_url:
        html = requests.get(main_url)

        soup = BeautifulSoup(html.text, 'lxml')
        
        page_list = soup.select_one("#block-system-main > div > div.view-content > table").find('tbody')

        for row in tqdm(page_list.find_all('tr')):
            name = row.find('td', 'views-field views-field-field-docs-person text-nowrap').text
            name = name.replace('\n','')
            date = row.find('td', 'views-field views-field-field-docs-start-date-time-value text-nowrap').text.rstrip()
            if (year - int(date[-4:])) < 0 or (year - int(date[-4:]) >= 4):
                continue

            link = row.find('td', 'views-field views-field-title').find('a', href=True)
            if 'Press Release' in link.text:
                continue


            # print(link.text)
            link = "https://www.presidency.ucsb.edu" + link["href"]
            if link == main_url:
                continue
            
            page = requests.get(link)
            page_soup = BeautifulSoup(page.text,'lxml')
            date = page_soup.select_one('#block-system-main > div > div > div.col-sm-8 > div.field-docs-start-date-time > span')
            content = page_soup.select_one('#block-system-main > div > div > div.col-sm-8 > div.field-docs-content')
            
            speech = [t.text for t in content.find_all('p')]
            speech_list['name'].append(name)
            speech_list['date'].append(date.text)
            speech_list['speech'].append(speech)
        
        pages = soup.select_one("#block-system-main > div > div.text-center > ul")
        main_url = None
        if pages:
            active_page = pages.find('li','active').find('span').text
            for page in pages.find_all('a', href=True):
                if page.text.isnumeric() and (int(page.text) == int(active_page)+1):
                    main_url = "https://www.presidency.ucsb.edu" + page["href"]
                    break

    speech_df = pd.DataFrame(speech_list)

    if save:
        speech_df.to_csv(save_path)
        
    return speech_df


def crawl_debate(url="https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/presidential-campaigns-debates-and-endorsements-0", save=False, save_path="./data/Debates.csv"):
    main_url = url
    html = requests.get(main_url)

    soup = BeautifulSoup(html.text, 'lxml')
    speech_list = {'date': [], 'speech': []}

    table = soup.select_one("#block-system-main > div > div > div > div.field-body > table").find("tbody")

    crawl = False
    for row in table.find_all('tr'):
        data = row.find_all('td')
        if len(data) != 2:
            continue
        if not crawl and ("General" in data[1].text):
            crawl = True
            continue
        if crawl and ("Primary" in data[1].text):
            crawl = False
            continue

        if crawl:
            if "Vice" in data[1].text:
                continue
            link = data[1].find('a',href=True)
            if link:
                page = requests.get(link["href"])
                page_soup = BeautifulSoup(page.text, 'lxml')

                date = page_soup.select_one("#block-system-main > div > div > div.col-sm-8 > div.field-docs-start-date-time > span").text
                content = page_soup.select_one("#block-system-main > div > div > div.col-sm-8 > div.field-docs-content")

                speech = [t.text for t in content.find_all('p')]
                speech_list['date'].append(date)
                speech_list['speech'].append(speech)

    speech_df = pd.DataFrame(speech_list)

    if save:
        speech_df.to_csv(save_path)
        
    return speech_df