import os
import pandas as pd
import datetime

data_dir = os.getenv('DATA_DIR')
file_path = os.path.join(data_dir, 'voting_intentions.csv')

df = pd.read_csv(file_path)

df['start_date'] = df['start_date'].apply(lambda x: datetime.datetime.strptime(x, '%d %B %Y').date())
df['end_date'] = df['end_date'].apply(lambda x: datetime.datetime.strptime(x, '%d %B %Y').date())

curr_month = datetime.datetime.now().month

poll_dates = []
for index, row in df.iterrows():
    if row['start_date'].month == curr_month:
        poll_dates.append(f"{row['start_date'].strftime('%B %d')} - {row['end_date'].strftime('%B %d, %Y')}")

if poll_dates:
    print('\n'.join(poll_dates))
else:
    print("No polls this month.")