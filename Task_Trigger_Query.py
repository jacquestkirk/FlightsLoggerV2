import requests


URL = "https://fierce-lake-44605.herokuapp.com/logger/queryCheapestFlight"

client = requests.session()

# Retrieve the CSRF token first
client.get(URL)  # sets cookie
csrftoken = client.cookies['csrf']

login_data = dict(csrfmiddlewaretoken=csrftoken)
r = client.post(URL, data=login_data, headers=dict(Referer=URL))