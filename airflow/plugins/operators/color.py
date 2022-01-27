import requests
import json

AIO_URL = 'http://localhost:4500'


def get_current_color():
    try:
        response = requests.get(AIO_URL + '/colors')
        current_color = json.loads(response.content)['CURRENT_COLOR']
    except requests.exceptions.RequestException as e:
        current_color = 'blue'
    return current_color
