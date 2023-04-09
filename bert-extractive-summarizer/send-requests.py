import requests

url = 'http://localhost:5000/summarize'
data = {
    'text': 'Het grote zwijn huppelt. Al denkt het na, waarom ben ik hier? Het grote zwijn huppelt verder. Het grote zwijn huppelt. Al denkt het na, waarom ben ik hier? Het grote zwijn huppelt verder. Het grote zwijn huppelt. Al denkt het na, waarom ben ik hier? Het grote zwijn huppelt verder.',
    'n':4
        }
response = requests.post(url, json=data)