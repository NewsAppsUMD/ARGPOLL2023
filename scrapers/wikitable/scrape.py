import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Get current month and year
now = datetime.datetime.now()
current_month = now.strftime("%B")
current_year = now.strftime("%Y")

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
pollster_index = headers.index("Pollster")
headers[pollster_index] = "Polling firm"

# extract table data and filter for current month
polling_data = []
for row in rows[1:]:
    row_data = []
    date = row.find('th').text.strip()
    date_obj = datetime.datetime.strptime(date, '%d %B %Y')
    if date_obj.month == now.month and date_obj.year == now.year:
        row_data.append(date)
        for td in row.find_all('td'):
            if td.find('a'):
                row_data.append(td.find('a').get('title', td.text.strip()))
            else:
                row_data.append(td.text.strip())
        polling_data.append(row_data)

# convert polling data to pandas dataframe
df = pd.DataFrame(polling_data, columns=headers)

# create HTML table
html_table = df.to_html(index=False)

# set up email
msg = MIMEMultipart()
msg['From'] = 'mercado@ryans.com'
msg['To'] = 'mercado@ryans.com'
msg['Subject'] = 'Daily Voting Intentions'

# create email body
body = 'Hello,\n\nEnclosed you will find the latest polling results for the 2023 Argentine General Election.'

# attach HTML table to email
part = MIMEText(html_table, 'html')
msg.attach(part)

# attach CSV file to email
with open('voting_intentions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(polling_data)

with open('voting_intentions.csv', 'rb') as f:
    attach = MIMEApplication(f.read(),_subtype="csv")
    attach.add_header('Content-Disposition','attachment',filename=str(current_month)+'_voting_intentions.csv')
    msg.attach(attach)

# send email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('mercado@ryans.com', 'password')
text = msg.as_string()
server.sendmail(msg['From'], msg['To'], text)
server.quit()