import requests

response = requests.get('http://localhost:5001')
print(response.content)