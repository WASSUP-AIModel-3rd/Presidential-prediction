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

def crawl_campaign_speech(url="https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/documents-related-to-presidential-elections/2016/report/200320/all/63/205", save=False, save_path='./campaign_speech.csv'):
    main_url = url
    html = requests.get(main_url)

    soup = BeautifulSoup(html.text, 'lxml')

    speech_list = {'name': [], 'date': [], 'speech': []}
    page_list = soup.select_one("#block-system-main > div > div.view-content > div > table").find('tbody')

    for row in tqdm(page_list.find_all('tr')):
        name = row.find('td', 'views-field views-field-title-1 nowrap').text
        name = name.replace('\n','')
        link = row.find('a', href=True)["href"]
        link = "https://www.presidency.ucsb.edu" + link
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
    
    speech_df = pd.DataFrame(speech_list)

    if save:
        speech_df.to_csv(save_path)
        
    return speech_df