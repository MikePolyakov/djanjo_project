import requests
import pprint

# response = requests.get('http://127.0.0.1:8000/api/v0/places/')

token = '5a95bfeab30fba3532a554c34044213f8de0a77e'
headers = {'Authorization': f'Token {token}'}
response = requests.get('http://127.0.0.1:8000/api/v0/places/', headers=headers)
pprint.pprint(response.json())

