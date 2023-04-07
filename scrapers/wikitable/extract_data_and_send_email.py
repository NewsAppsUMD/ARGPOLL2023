import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('scrapers/wikitable/voting_intentions.csv')

# Filter the DataFrame to only include polls from the current month
current_month = datetime.now().strftime('%B')
df = df[df['Date'].str.contains(current_month)]

# Create a table from the filtered DataFrame
table_html = df.to_html(index=False)

# Set up email message
msg = MIMEMultipart()
msg['From'] = 'mercadoryan94@gmail.com'
msg['To'] = 'mercadoryan94@gmail.com'
msg['Subject'] = 'Daily Voting Intentions'

# Set up email body
body = 'Hello,\n\nEnclosed you will find the latest polling results for the 2023 Argentine General Election:\n\n'
body += table_html
body += '\n\nThank you,\nYour Name'
msg.attach(MIMEText(body, 'plain'))

# Add the CSV file as an attachment
with open('scrapers/wikitable/voting_intentions.csv', 'rb') as f:
    attachment = MIMEApplication(f.read(), _subtype='csv')
    attachment.add_header('Content-Disposition', 'attachment', filename='voting_intentions.csv')
    msg.attach(attachment)

# Send the email
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.login('mercadoryan94@gmail.com', 'your_email_password')
    smtp.send_message(msg)