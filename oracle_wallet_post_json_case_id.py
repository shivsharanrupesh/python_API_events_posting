"""
accepting the username and password from Oracle wallet and then posting the events into ECM 
"""

import cx_Oracle
import requests
import json
import logging

logging.basicConfig(level=logging.INFO, filename='post_json.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_oracle_wallet_credentials(wallet_path):
    try:
        # Connect using the Oracle wallet to retrieve credentials
        connection = cx_Oracle.connect('/', '', dsn=f'/{wallet_path}')
        wallet_username = connection.username
        wallet_password = connection.password
        connection.close()
        return wallet_username, wallet_password
    except cx_Oracle.DatabaseError as e:
        logging.error(f'Error retrieving Oracle wallet credentials: {str(e)}')
        return None, None

def post_json_file(url, file_path, wallet_username, wallet_password):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            data = json.load(file)

        headers = {'Content-Type': 'application/json'}
        auth = (wallet_username, wallet_password)
        response = requests.post(url, json=data, headers=headers, auth=auth)

        if response.status_code == 200:
            logging.info('JSON file posted successfully.')
            response_data = response.json()
            if 'cases' in response_data:
                cases_generated = response_data['cases']
                logging.info(f'Number of cases generated: {len(cases_generated)}')
                logging.info(f'Case IDs:')
                for case in cases_generated:
                    case_id = case.get('caseId', 'N/A')
                    logging.info(case_id)
            else:
                logging.info('No cases generated in the response.')
            return True
        else:
            logging.error(f'Error posting JSON file. Status code: {response.status_code}')
            return False
    except Exception as e:
        logging.error(f'Error in post_json_file: {str(e)}')
        return False

# Replace '<Application URL>' with the actual URL
url = 'http://<Application URL>/rest-api/CMRestService/RealTimeCaseCreationService/saveEventsAndPromoteToCase'
wallet_path = '/path/to/your/wallet'

wallet_username, wallet_password = get_oracle_wallet_credentials(wallet_path)

if wallet_username and wallet_password:
    if latest_file_path:
        if post_json_file(url, latest_file_path, wallet_username, wallet_password):
            logging.info('JSON file processing and posting completed.')
        else:
            logging.info('JSON file processing failed.')
    else:
        logging.info('No eligible JSON file found for processing.')
else:
    logging.info('Oracle wallet credentials not available.')
