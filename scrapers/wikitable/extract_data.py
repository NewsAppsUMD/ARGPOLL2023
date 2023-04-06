name: Daily Voting Intentions

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  scrape_and_email:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install requests bs4 pandas

      - name: Scrape data and save to CSV
        run: python scrapers/wikitable/scrape.py

      - name: Extract Data and Send Email
        run: |
          cd scrapers/wikitable
          python extract_data.py

        env:
          GMAIL_ADDRESS: ${{ secrets.EMAIL }}
          GMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}