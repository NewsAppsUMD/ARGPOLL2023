import pandas as pd
import datetime
import os


def extract_poll_dates(data_dir):
    # Read the CSV file
    df = pd.read_csv(os.path.join(data_dir, 'voting_intentions.csv'))

    # Get the unique poll dates for the current month
    curr_month = datetime.date.today().month
    poll_dates = set()

    for i, row in df.iterrows():
        date_str = row['Fieldwork date']
        if not pd.isna(date_str) and date_str != '':
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            if date.month == curr_month:
                poll_dates.add(date.strftime('%Y-%m-%d'))

    # Return the poll dates as a string
    return ', '.join(sorted(list(poll_dates)))


if __name__ == '__main__':
    # Get the path to the data directory from the environment variable
    data_dir = os.getenv('DATA_DIR')

    # Extract the poll dates and print them to stdout
    poll_dates = extract_poll_dates(data_dir)
    print(f'::set-output name=poll_dates::{poll_dates}')