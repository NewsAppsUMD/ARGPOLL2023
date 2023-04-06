import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

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

# extract table data and write to pandas DataFrame
data = []
for row in rows[1:]:
    if row.find('th'):
        date_str = row.find('th').text.strip()
        date = datetime.strptime(date_str, '%d %b %Y')
    else:
        if date.month == datetime.now().month:
            row_data = [date_str]
            for td in row.find_all('td'):
                if td.find('a'):
                    row_data.append(td.find('a').get('title', td.text.strip()))
                else:
                    row_data.append(td.text.strip())
            data.append(row_data)

df = pd.DataFrame(data, columns=headers)

# group by polling firm and date and aggregate results
df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y')
df = df.groupby(['Polling firm', 'Date']).agg({'Percentage': 'max'}).reset_index()

# create formatted table as string
table_str = df.to_html(index=False)

# create email body
body = f"""Hello,

Enclosed you will find the latest polling results for the 2023 Argentine General Election.

{table_str}

Thank you,
Your Name
"""

# write email body to file
with open('email_body.txt', mode='w') as file:
    file.write(body)