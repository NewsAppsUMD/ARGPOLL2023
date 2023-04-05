import csv
import datetime

# get the current year and month
now = datetime.datetime.now()
year = now.year
month = now.month

# read the CSV file and extract the poll dates for the current month
with open('voting_intentions.csv', mode='r') as file:
    reader = csv.reader(file)
    header = next(reader)
    poll_dates = set()
    for row in reader:
        date_str = row[0]
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        if date.year == year and date.month == month:
            poll_dates.add(date_str)

# print the poll dates for the current month
print(poll_dates)