#name: Daily Polling Results

on:
  schedule:
    - cron: "0 12 * * *"

jobs:
  scrape_data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install beautifulsoup4
          pip install pandas
      - name: Scrape data
        run: python scraper.py
      - name: Upload data
        uses: actions/upload-artifact@v2
        with:
          name: voting_intentions
          path: ./scrapers/wikitable/voting_intentions.csv
      - name: Send email
        uses: dawidd6/action-send-mail@v3.3.0
        with:
          server_address: smtp.gmail.com
          server_port: 587
          username: ${{ secrets.EMAIL }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: "Daily Voting Intentions"
          body: |
            <html>
              <body>
                <p>Hello,</p>
                <p>Enclosed you will find the latest polling results for the 2023 Argentine General Election:</p>
                <table>
                  <tr>
                    <th>Polling firm</th>
                    <th>Date</th>
                    <th>Party A</th>
                    <th>Party B</th>
                    <th>Party C</th>
                  </tr>
                  <tbody>
                    {% for row in data %}
                    <tr>
                      <td>{{ row.pollster }}</td>
                      <td>{{ row.date }}</td>
                      <td>{{ row.party_a }}</td>
                      <td>{{ row.party_b }}</td>
                      <td>{{ row.party_c }}</td>
                    </tr>
                    {% endfor %}
                  </tbody>
                </table>
                <p>Best regards,</p>
                <p>Ryan Mercado</p>
              </body>
            </html>
          from: mercadoryan94@gmail.com
          to: mercadoryan94@gmail.com
          attachments: |
            ./scrapers/wikitable/voting_intentions.csv