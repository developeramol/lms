import requests
import json

webhook_url = 'https://webhook.site/08a4e11e-f85e-42ce-8ae1-b5dd2e437c52'
data = {
    'name': 'Devops Journey',
    'position': 'Number One..Position.....!'
}

r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
