import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Argentine_general_election'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find_all('table')[0]

rows = table.find_all('tr')

data = []

for row in rows[1:]:
    cols = row.find_all('td')
    if len(cols) >= 3:
        date_str = cols[0].get_text().strip()
        if date_str:
            date = datetime.strptime(date_str, '%d %b %Y')
            firm = cols[1].get_text().strip()
            result = cols[2].get_text().strip()
            data.append([date, firm, result])

data.sort(key=lambda x: x[0], reverse=True)

with open('scrapers/wikitable/voting_intentions.csv', 'w') as f:
    f.write('Date,Firm,Result\n')
    for row in data:
        f.write('{},{},{}\n'.format(row[0].strftime('%Y-%m-%d'), row[1], row[2]))

with open('email_body.txt', 'w') as f:
    f.write('Hello,\n\nEnclosed you will find the latest polling results for the 2023 Argentine General Election.\n\n')
    f.write('Date\tFirm\tResult\n')
    for row in data:
        f.write('{}\t{}\t{}\n'.format(row[0].strftime('%Y-%m-%d'), row[1], row[2]))