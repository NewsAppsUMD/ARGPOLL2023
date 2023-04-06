import requests

url = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Argentine_general_election"

response = requests.get(url)

print(response.text)