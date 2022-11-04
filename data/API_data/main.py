import requests

url = 'https://mentalport-api.herokuapp.com/user-activity'
#url = 'https://mentalport-api.herokuapp.com/'
headers = {'Authorization': 'Bearer 98dca46d-8e00-425a-b82c-38d550634e4e'}
response = requests.get(url, headers=headers)

print(response.text)

with open('data.json', 'w+') as f:
    f.write(response.text)