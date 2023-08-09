#retrieves credentials from the Oracle wallet alias and post the events into ECM. 

import cx_Oracle
import requests
import json
import logging

logging.basicConfig(level=logging.INFO, filename='post_json.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_credentials_from_wallet(wallet_path, alias):
    try:
        connection = cx_Oracle.connect('/', '', dsn=f'/{wallet_path}')
        credentials = connection.get_credentials(alias)
        connection.close()
        return credentials.username, credentials.password
    except cx_Oracle.DatabaseError as e:
        logging.error(f'Error retrieving credentials from Oracle wallet: {str(e)}')
        return None, None

def post_json_file(url, file_path, username, password):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            data = json.load(file)

        headers = {'Content-Type': 'application/json'}
        auth = (username, password)
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
wallet_alias = 'your_alias'

username, password = get_credentials_from_wallet(wallet_path, wallet_alias)

if username and password:
    if latest_file_path:
        if post_json_file(url, latest_file_path, username, password):
            logging.info('JSON file processing and posting completed.')
        else:
            logging.info('JSON file processing failed.')
    else:
        logging.info('No eligible JSON file found for processing.')
else:
    logging.info('Oracle wallet credentials not available.')
