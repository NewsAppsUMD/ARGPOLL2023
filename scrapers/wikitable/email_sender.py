import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
from datetime import datetime, timedelta
import os

# Get current date
now = datetime.now()

# Get the latest polling data
df = pd.read_csv('scrapers/wikitable/voting_intentions.csv')

# Get the latest poll dates
latest_poll_dates = df['Date'].unique()[-4:]

# Filter the latest polling data
latest_poll_data = df[df['Date'].isin(latest_poll_dates)]

# Format the polling data as an HTML table
table = "<table border='1'><tr><th>Polling firm</th><th>Date</th><th>Party A</th><th>Party B</th><th>Party C</th></tr>"
for i, row in latest_poll_data.iterrows():
    table += f"<tr><td>{row['Polling firm']}</td><td>{row['Date']}</td><td>{row['Party A']}</td><td>{row['Party B']}</td><td>{row['Party C']}</td></tr>"
table += "</table>"

# Set up email message
msg = MIMEMultipart()
msg['Subject'] = "Daily Voting Intentions"
msg['From'] = "mercadoryan94@gmail.com"
msg['To'] = "mercadoryan94@gmail.com"

# Create HTML message body
body = f"""\
<html>
  <body>
    <p>Hello,</p>
    <p>Enclosed you will find the latest polling results for the 2023 Argentine General Election.</p>
    {table}
    <p>Best regards,</p>
    <p>Ryan Mercado</p>
  </body>
</html>
"""

# Attach message body as HTML
msg.attach(MIMEText(body, 'html'))

# Attach CSV file as attachment
with open('scrapers/wikitable/voting_intentions.csv', 'rb') as f:
    attachment = MIMEApplication(f.read(), _subtype='csv')
    attachment.add_header('Content-Disposition', 'attachment', filename='voting_intentions.csv')
    msg.attach(attachment)

# Get password from GitHub secrets
password = os.environ.get('EMAIL_PASSWORD')

# Send email
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.login('mercadoryan94@gmail.com', password)
    smtp.send_message(msg)

print("Email sent!")
