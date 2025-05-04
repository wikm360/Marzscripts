import requests
import logging
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv('PANEL_USERNAME')
DOMAIN = os.getenv('PANEL_URL')
password = os.getenv('PANEL_PASS')
protocol = os.getenv('TYPE')
inbounds_to_remove = os.getenv('INBOUND_TAG')
PORT = os.getenv('PORT')

def get_access_token(username, password):
    url = f'{DOMAIN}:{PORT}/api/admin/token'
    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while obtaining access token: {e}')
        return None

def get_users_list(access_token):
    url = f'{DOMAIN}:{PORT}/api/users'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        users_list = response.json()
        return users_list
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while retrieving users list: {e}')
        return None

def remove_inbounds_for_protocol(access_token, username, protocol, inbounds_to_remove):
    url = f'{DOMAIN}:{PORT}/api/user/{username}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user_details = response.json()

        if 'inbounds' in user_details:
            inbounds = user_details['inbounds'].get(protocol, [])
            updated_inbounds = [inbound for inbound in inbounds if inbound not in inbounds_to_remove]
            user_details['inbounds'][protocol] = updated_inbounds

            # Modify 'links' and 'subscription_url'
            user_details['links'] = []
            user_details['subscription_url'] = ""

            response = requests.put(url, json=user_details, headers=headers)
            response.raise_for_status()
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while removing inbounds for protocol: {e}')
        return False


# Configure logging settings
logging.basicConfig(filename='script_log.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

access_token = get_access_token(username, password)
if access_token:
    users_list = get_users_list(access_token)
    if users_list:
        for user in users_list['users']:
            # Remove specified inbounds for the specified protocol
            if 'inbounds' in user:
                if remove_inbounds_for_protocol(access_token, user['username'], protocol, inbounds_to_remove):
                    print(f"Inbounds removed successfully for user {user['username']} and protocol {protocol}.")
                else:
                    print(f"No specified inbounds found for user {user['username']} and protocol {protocol}.")
        print("All users modified successfully.")    
    else:
        print("Failed to retrieve the users list.")
else:
    print("Failed to obtain the access token.")

