import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL to scrape data from
url = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Argentine_general_election"

# Send a request to the URL and get the page content
r = requests.get(url)

# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(r.content, "html.parser")

# Find the table with the poll data
table = soup.find("table", class_="wikitable")

# Extract the column names from the table
headers = []
for th in table.find_all("th"):
    headers.append(th.text.strip())

# Extract the poll data from the table
poll_data = []
for tr in table.find_all("tr")[1:]:
    tds = tr.find_all("td")
    poll = []
    for td in tds:
        poll.append(td.text.strip())
    poll_data.append(poll)

# Create a pandas dataframe with the poll data and column names
poll_df = pd.DataFrame(poll_data, columns=headers)

# Convert date column to datetime format
poll_df["Date"] = pd.to_datetime(poll_df["Date"], format="%d %b %Y")

# Get the latest poll data
latest_polls = poll_df.sort_values(by="Date", ascending=False).head(4)

# Format the latest poll data as an HTML table
latest_polls_html = latest_polls.to_html(index=False)

# Remove the new line character from the HTML table
latest_polls_html = latest_polls_html.replace('\n','')

# Format the HTML table to include borders and alternate row colors
latest_polls_html = latest_polls_html.replace('<table', '<table style="border-collapse: collapse; border: 1px solid black; font-size: 14px;" cellpadding="10"')
latest_polls_html = latest_polls_html.replace('<thead>', '<thead style="background-color: #f2f2f2;">')
latest_polls_html = latest_polls_html.replace('<tbody>', '<tbody style="background-color: #ffffff;">')

# Output the latest poll data as a variable that can be used in the send email step
print(f'::set-output name=poll_data::{latest_polls_html}')