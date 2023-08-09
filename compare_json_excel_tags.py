"""
i have a json file, which has some tags, i have another excel sheet, which has the tags, i want to compare the json tags from json file with excel sheet tags. 
"""

import json
import pandas as pd
import logging

logging.basicConfig(filename='tag_comparison.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TagComparator:
    def __init__(self, json_file_path, excel_file_path):
        self.json_file_path = json_file_path
        self.excel_file_path = excel_file_path
        self.json_tags = []
        self.excel_tags = []

    def read_json_tags(self):
        with open(self.json_file_path, 'r') as json_file:
            data = json.load(json_file)
            self.json_tags = data.get('tags', [])

    def read_excel_tags(self):
        df = pd.read_excel(self.excel_file_path)
        self.excel_tags = df['Tags'].tolist()

    def compare_tags(self):
        common_tags = set(self.json_tags) & set(self.excel_tags)
        json_unique_tags = set(self.json_tags) - common_tags
        excel_unique_tags = set(self.excel_tags) - common_tags

        return {
            'common_tags': list(common_tags),
            'json_unique_tags': list(json_unique_tags),
            'excel_unique_tags': list(excel_unique_tags)
        }

if __name__ == "__main__":
    json_file_path = "path/to/your/json/file.json"
    excel_file_path = "path/to/your/excel/file.xlsx"

    comparator = TagComparator(json_file_path, excel_file_path)
    comparator.read_json_tags()
    comparator.read_excel_tags()

    tag_comparison_result = comparator.compare_tags()

    logging.info("Common Tags: %s", tag_comparison_result['common_tags'])
    logging.info("JSON Unique Tags: %s", tag_comparison_result['json_unique_tags'])
    logging.info("Excel Unique Tags: %s", tag_comparison_result['excel_unique_tags'])

    print("Tag comparison completed. Check tag_comparison.log for details.")
