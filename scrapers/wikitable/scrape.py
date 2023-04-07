import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

url = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Argentine_general_election#By_political_party_2023"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find_all('table')[1] # select the second table on the page

rows = table.find_all('tr')

# extract table headers
headers = []
for th in rows[0].find_all('th'):
    if th.find('a'):
        headers.append(th.find('a')['title'])
    else:
        headers.append(th.text.strip())

# find the index of the "Pollster" column and replace it with "Polling firm"
pollster_index = headers.index("Polling firm")
headers[pollster_index] = "Polling firm"

# extract table data and group by date
poll_data = {}
for row in rows[1:]:
    if row.find('th'):
        poll_date_str = row.find('th').text.strip()
        poll_date = datetime.strptime(poll_date_str, '%d %b %Y')
        if poll_date.date() < datetime.now().date() - timedelta(days=30): # only include polls from last 30 days
            break
        if poll_date not in poll_data:
            poll_data[poll_date] = []
        parties = {}
        for td in row.find_all('td'):
            if td.find('a'):
                party_name = td.find('a').get('title', td.text.strip())
                if party_name not in parties:
                    parties[party_name] = 0
                parties[party_name] += 1
        poll_data[poll_date].append(parties)

# write table data to CSV file
with open('voting_intentions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Poll Date'] + headers[2:])
    for poll_date, parties in poll_data.items():
        row = [poll_date.strftime('%d-%b-%Y')]
        for party_name in headers[2:]:
            count = sum(parties_data.get(party_name, 0) for parties_data in parties)
            row.append(count)
        writer.writerow(row)