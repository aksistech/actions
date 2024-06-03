import jwt
import time
import requests
import os

app_id = os.environ['APP_ID']
installation_id = os.environ['INSTALLATION_ID']
private_key = os.environ['PRIVATE_KEY']

now = int(time.time())
payload = {
    'iat': now,
    'exp': now + 600,  # Token valid for 10 minutes
    'iss': app_id
}
jwt_token = jwt.encode(payload, private_key, algorithm='RS256')

# Get access token
url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Accept': 'application/vnd.github.v3+json'
}
response = requests.post(url, headers=headers)

if response.status_code == 201:
    access_token = response.json()['token']
    print(f'AccessToken Generated: {access_token}')
    with open('code/.github/scripts/access_token.txt', 'w') as token_file:
        token_file.write(access_token)
else:
    print(f'Error getting access token: {response.status_code}')
    print(response.json())

