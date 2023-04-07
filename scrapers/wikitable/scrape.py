import requests
from bs4 import BeautifulSoup
import csv
from tabulate import tabulate

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

# extract table data
data = []
for row in rows[1:]:
    if row.find('th'):
        row_data = [row.find('th').text.strip()]
    else:
        row_data = []
    for td in row.find_all('td'):
        if td.find('a'):
            row_data.append(td.find('a').get('title', td.text.strip()))
        else:
            row_data.append(td.text.strip())
    data.append(row_data)

# generate markdown table using tabulate
table = tabulate(data, headers=headers, tablefmt='pipe')

# write markdown table to file
with open('voting_intentions.md', mode='w') as file:
    file.write(table)