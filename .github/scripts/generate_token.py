import jwt
import time
import requests
import os

app_id = os.environ.get('APP_ID')
installation_id = os.environ.get('INSTALLATION_ID')
private_key = os.environ.get('PRIVATE_KEY')

if not all([app_id, installation_id, private_key]):
    print("Missing environment variables.")
    print(f"APP_ID: {app_id}")
    print(f"INSTALLATION_ID: {installation_id}")
    print(f"PRIVATE_KEY: {'present' if private_key else 'missing'}")
    exit(1)

now = int(time.time())
payload = {
    'iat': now,
    'exp': now + 600,  # Token válido por 10 minutos
    'iss': app_id
}
jwt_token = jwt.encode(payload, private_key, algorithm='RS256')

url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Accept': 'application/vnd.github.v3+json'
}
response = requests.post(url, headers=headers)

if response.status_code == 201:
    access_token = response.json()['token']
    print(f'Access Token: {access_token}')
    # Salvar o token em um arquivo
    with open('access_token.txt', 'w') as token_file:
        token_file.write(access_token)
else:
    print(f'Error getting access token: {response.status_code}')
    print(response.json())
