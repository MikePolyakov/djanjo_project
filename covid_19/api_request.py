import requests
import pprint

# response = requests.get('http://127.0.0.1:8000/api/v0/places/')

token = '7bf9ab81b95e95acb2481f66df1a49132cbaa5dc'
headers = {'Authorization': f'Token {token}'}
response = requests.get('http://127.0.0.1:8000/api/v0/articles/', headers=headers)
pprint.pprint(response.json())

