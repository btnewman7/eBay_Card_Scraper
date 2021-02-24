# Steps:
# Make a request to eBay.com and get page
# Collect data from each detail page
# Collect all links to detail pages of each product
# Write scraped data to CSV file
import requests
import csv
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url)
    
    if not response.ok:
        print('Server sponded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
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
    
    #sport 
    try:
        rows = soup.find('div', class_='itemAttr').findAll('table')[0].findAll('tr') 
    except:
        rows= ''
    print(rows)

    #data = {
    #    'title': title,
    #    'currency': currency,
    #    'price': price
    #}

    #return data
    
def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = ''
    
    urls = [item.get('href') for item in links]
    
    return urls

#def write_csv(data, url):
#    with open('output.csv', 'a') as csvfile:
#        writer = csv.writer(csvfile)
#        
#        row = [data['title'],data['currency'], data['price'], url]
#
#        writer.writerow(row)


def main():
    url = 'https://www.ebay.com/itm/1969-TOPPS-BASEBALL-380-STAN-BAHNSEN-EX-MINT-YANKEES/154005822797?hash=item23db765d4d:g:etIAAOSwwOhfC~cu'
    #url = 'https://www.ebay.com/sch/i.html?_nkw=sports+cards&LH_Sold=1&Product=Single&_pgn=1'
    get_detail_data(get_page(url))
    #products = get_index_data(get_page(url))
    #for link in products:
        #data = get_detail_data(get_page(link))
        #write_csv(data, link)



if __name__ == '__main__':
    main()