import csv
from datetime import datetime

# Set up variables
results = []
current_month = datetime.today().strftime('%B')
headers = []
pollster_index = 0

# Open CSV file
with open('scrapers/wikitable/voting_intentions.csv') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            headers = row
            pollster_index = headers.index('Polling firm')
        else:
            pollster = row[pollster_index]
            date_str = row[0]
            date = datetime.strptime(date_str, '%d %B %Y')
            if date.strftime('%B') == current_month:
                results.append(f'{pollster}: {", ".join(row[1:])}')

# Output results as a single string
print('\n'.join(results))