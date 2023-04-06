import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

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

# create dictionary to store poll results
polls = {}

# extract table data and update dictionary
for row in rows[1:]:
    poll_date = row.find('th').text.strip()
    poll_date = datetime.strptime(poll_date, '%d %B %Y').date()
    if poll_date.month == datetime.today().month: # check if poll date is in current month
        if poll_date not in polls:
            polls[poll_date] = {header: '' for header in headers[1:]} # initialize poll results with empty strings
        for i, td in enumerate(row.find_all('td')):
            polls[poll_date][headers[i+1]] = td.text.strip()

# convert dictionary to DataFrame
df = pd.DataFrame.from_dict(polls, orient='index')

# format date column
df.index = df.index.strftime('%d %B %Y')

# send email with DataFrame
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# create email message
msg = MIMEMultipart()
msg['Subject'] = 'Daily Voting Intentions'
msg['From'] = 'your_email@example.com'
msg['To'] = 'recipient_email@example.com'

# create text version of DataFrame
df_text = df.to_string(index=True)

# add text to email body
body = 'Hello,\n\nEnclosed you will find the latest polling results for the 2023 Argentine General Election:\n\n'
body += df_text

msg.attach(MIMEText(body, 'plain'))

# send email with smtplib
import smtplib

# add your email and password as environment variables or replace with your own values
EMAIL = os.environ.get('EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL, EMAIL_PASSWORD)

    # attach DataFrame as CSV file
    csv_data = df.to_csv(index=True).encode('utf-8')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(csv_data)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="arg_polls.csv"')