"""
Below code will be used to post the events into ECM. 
"""

import requests
import json
import logging

logging.basicConfig(level=logging.INFO, filename='post_json.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def post_json_file(url, file_path, username, password):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            data = json.load(file)

        headers = {'Content-Type': 'application/json'}
        auth = (username, password)
        response = requests.post(url, json=data, headers=headers, auth=auth)

        if response.status_code == 200:
            logging.info('JSON file posted successfully.')
            return True
        else:
            logging.error(f'Error posting JSON file. Status code: {response.status_code}')
            return False
    except Exception as e:
        logging.error(f'Error in post_json_file: {str(e)}')
        return False

# Replace '<Application URL>' with the actual URL
url = 'http://<Application URL>/rest-api/CMRestService/RealTimeCaseCreationService/saveEventsAndPromoteToCase'
username = 'your_username'  # Replace with the actual username
password = 'your_password'  # Replace with the actual password

if latest_file_path:
    if post_json_file(url, latest_file_path, username, password):
        logging.info('JSON file processing and posting completed.')
    else:
        logging.info('JSON file processing failed.')
else:
    logging.info('No eligible JSON file found for processing.')
