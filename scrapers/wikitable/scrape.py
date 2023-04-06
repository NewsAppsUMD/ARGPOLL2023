import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

# Define URL to scrape
url = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Argentine_general_election"

# Send a request to the website and get the HTML content
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Find the table with the polling data
table = soup.find("table", {"class": "wikitable"})

# Find all rows of the table
rows = table.findAll("tr")

# Create empty lists to store the data
dates = []
polling_firms = []
sample_sizes = []
intents = []

# Loop through the rows of the table and extract the data
for row in rows[1:]:
    cells = row.findAll("td")
    date = cells[0].get_text().strip()
    polling_firm = cells[1].get_text().strip()
    sample_size = cells[2].get_text().strip()
    intent = cells[3].get_text().strip()

    # Check if the date is in the correct format
    try:
        date_obj = datetime.datetime.strptime(date, '%d %B %Y')
    except ValueError:
        print(f"Ignoring invalid date format: {date}")
        continue

    # Check if the date is in the current month
    if date_obj.month != datetime.datetime.now().month:
        continue

    dates.append(date)
    polling_firms.append(polling_firm)
    sample_sizes.append(sample_size)
    intents.append(intent)

# Create a dictionary to store the data
data = {
    "Date": dates,
    "Polling Firm": polling_firms,
    "Sample Size": sample_sizes,
    "Intent": intents,
}

# Create a pandas DataFrame from the dictionary
df = pd.DataFrame(data)

# Create a directory to store the CSV file
if not os.path.exists("scrapers/wikitable"):
    os.makedirs("scrapers/wikitable")

# Save the DataFrame to a CSV file
df.to_csv("scrapers/wikitable/voting_intentions.csv", index=False)