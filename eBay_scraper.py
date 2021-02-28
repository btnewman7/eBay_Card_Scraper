# Steps:
# Make a request to eBay.com and get page
# Collect data from each detail page
# Collect all links to detail pages of each product
# Write scraped data to CSV file
import requests
import csv
import re
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url, timeout=5)
    
    if not response.ok:
        print('Server sponded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_detail_data(soup):
    #title
    try:
        title = soup.find('span', class_='u-dspn').get_text()
    except:
        title = ''
    
    #soldprice
    try:
        try:
            p = soup.find('span', id='prcIsum').text.strip()
        except:
            p = soup.find('span', class_='vi-VR-cvipPrice').text.strip()
        currency, price = p.split(' ')
    except:
        price = ''
        currency = ''
    
    #date
    try:
        date = soup.find('span', id='bb_tlft').text.strip()
    except:
        date = ''

    #sport 
    try:
        item_specs_table = soup.find('div', id="vi-desc-maincntr").find('div', class_="itemAttr").find_all('div', class_="section")[0]
        sport = item_specs_table.find_all("td", string=re.compile("Sport:"))[0].findNext('td').text.strip()
    except:
        sport= ''

    #card_manufacturer
    try:
        card_manufacturer = item_specs_table.find_all("td", string=re.compile("Card Manufacturer:"))[0].findNext('td').text.strip()
    except:
        card_manufacturer= ''
    
    #team
    try:
        team = item_specs_table.find_all("td", string=re.compile("Team:"))[0].findNext('td').text.strip()
    except:
        team= ''

    #player
    try:
        player_name = item_specs_table.find_all("td", string=re.compile("Player:"))[0].findNext('td').text.strip()
    except:
        player_name= ''

    #year
    try:
        year = item_specs_table.find_all("td", string=re.compile("Year:"))[0].findNext('td').text.strip()
    except:
        year= ''

    #season_year
    try:
        season = item_specs_table.find_all("td", string=re.compile("Season:"))[0].findNext('td').text.strip()
    except:
        season= ''

    #grade
    try:
        grade = item_specs_table.find_all("td", string=re.compile("Grade:"))[0].findNext('td').text.strip()
    except:
        grade= ''
    
    #card_attributes
    try:
        card_attributes = item_specs_table.find_all("td", string=re.compile("Card Attributes:"))[0].findNext('td').text.strip()
    except:
        card_attributes= ''

    #grader
    try:
        grader = item_specs_table.find_all("td", string=re.compile("Professional Grader:"))[0].findNext('td').text.strip()
    except:
        grader= ''

    data = {
        'title': title,
        'player_name': player_name,
    #    'currency': currency,
        'price': price,
        'date': date,
        'sport': sport,
        'team': team,
        'year': year,
    #    'season': season,
        'card_manufacturer': card_manufacturer,
        'grade': grade,
        'grader': grader,
        'card_attributes': card_attributes
    }

    return data
    
def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = ''
    
    urls = [item.get('href') for item in links]
    
    return urls

def write_csv(data, url):
    with open('output1.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        
        row = [data['title'],
            data['player_name'], 
        #    data['currency'], 
            data['price'],
            data['date'],
            data['sport'],
            data['team'],
            data['year'],
        #    data['season'],
            data['card_manufacturer'],
            data['grade'],
            data['grader'],
            data['card_attributes'],
             url]

        writer.writerow(row)


def main():
    #url = 'https://www.ebay.com/itm/1969-TOPPS-BASEBALL-380-STAN-BAHNSEN-EX-MINT-YANKEES/154005822797?hash=item23db765d4d:g:etIAAOSwwOhfC~cu'
    #get_detail_data(get_page(url))
    for num in range(1,20):
        url = f'https://www.ebay.com/sch/i.html?_nkw=sports+cards&LH_Sold=1&Product=Single&_udlo=35&LH_PrefLoc=1&_pgn={num}'
        products = get_index_data(get_page(url))
        for link in products:
            data = get_detail_data(get_page(link))
            write_csv(data, link)



if __name__ == '__main__':
    main()