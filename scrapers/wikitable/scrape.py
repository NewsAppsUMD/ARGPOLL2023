import csv
import datetime
import requests
from bs4 import BeautifulSoup

# specify the URL of the web page
url = 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Argentine_general_election'

# send a request to the web page and get its HTML content
response = requests.get(url)
html_content = response.content

# create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# find the table element that contains the polling data
table = soup.find('table', class_='wikitable')

# get the current month and year
now = datetime.datetime.now()
current_month = now.month
current_year = now.year

# create a CSV file and write the header row
filename = 'polls_{}_{}.csv'.format(current_year, current_month)
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Pollster', 'Date', 'Sample size', 'Approve', 'Disapprove', 'Neutral'])

    # iterate over the rows in the table
    rows = table.find_all('tr')
    for row in rows[1:]:
        # extract the data from each cell in the row
        cells = row.find_all('td')
        data = [cell.get_text(strip=True) for cell in cells]

        # extract date and check if it's in the current month
        print(data)
        if len(data) > 1:
            date_str = data[1]
            date = datetime.datetime.strptime(date_str, '%B %d, %Y')
            if date.month == current_month:
                writer.writerow(data)
        else:
            print("Skipping row due to insufficient data: {}".format(data))