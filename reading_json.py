"""
fetching the latest json file from the source path: 
we will get a json file with the file name as: RIB_PRX_TD01003P_20230524_082650_000000 where RIB_PRX_TD01003P will be same for all the file, 20230524 - will be the date format, 082650 - will be the time stamp, 000000 - will be the sequence number which may not change. 
this code will accept this kind of a file name and select the latest file or todays file for processing once the file processing is done, move that file to different directoy. 
"""

import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, filename='get_latest_file.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_latest_json_file(directory_path):
    try:
        today = datetime.now().strftime('%Y%m%d')
        latest_file = None
        latest_timestamp = None

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) and filename.startswith('RIB_PRX_TD01003P_'):
                parts = filename.split('_')
                if len(parts) == 4:
                    date_str = parts[2]
                    time_str = parts[3][:6]  # Take the first 6 characters of the time stamp
                    try:
                        file_date = datetime.strptime(date_str, '%Y%m%d').date()
                        file_time = datetime.strptime(time_str, '%H%M%S').time()
                    except ValueError:
                        continue

                    if file_date == datetime.now().date() and (latest_timestamp is None or file_time > latest_timestamp):
                        latest_file = file_path
                        latest_timestamp = file_time

        return latest_file
    except Exception as e:
        logging.error(f'Error in get_latest_json_file: {str(e)}')
        return None

def move_file(file_path, destination_directory):
    try:
        filename = os.path.basename(file_path)
        new_path = os.path.join(destination_directory, filename)
        os.rename(file_path, new_path)
        logging.info(f'File moved to {destination_directory}')
    except Exception as e:
        logging.error(f'Error moving file: {str(e)}')

# Replace 'path/to/source/directory' and 'path/to/destination/directory' with the actual paths
source_directory = 'path/to/source/directory'
destination_directory = 'path/to/destination/directory'

latest_file_path = get_latest_json_file(source_directory)

if latest_file_path:
    logging.info(f'Latest JSON file: {latest_file_path}')
    move_file(latest_file_path, destination_directory)
else:
    logging.info('No eligible JSON file found for processing.')

