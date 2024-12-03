import sys
sys.path.append("/storage/emulated/0/Code_Projects/Python/Libraries/SecureProtectData")

import json
import csv
import os
import logging
from typing import Union, List

# Configure logging
logging.basicConfig(filename='currency.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Memory:
    def __init__(self):
        self.currencies = {}

    def create_currency(self, name: str, amount: float = 0) -> dict:
        currency = {'name': name, 'amount': amount}
        self.store_data(currency)
        logging.info(f"Created currency: {currency}")
        return currency

    def store_data(self, currency: dict):
        self.currencies[currency['name']] = currency
        logging.info(f"Stored currency in memory: {currency}")

    def get_data(self, name: str) -> Union[dict, None]:
        currency = self.currencies.get(name)
        logging.info(f"Retrieved currency: {currency}")
        return currency

    def update_currency(self, name: str, operation: str, new_value: float):
        currency = self.get_data(name)
        if currency:
            if operation == "Add":
                currency['amount'] += new_value
            elif operation == "Subtract":
                currency['amount'] -= new_value
            logging.info(f"Updated currency: {currency}")
        else:
            logging.warning(f"Currency not found: {name}")

    def list_all_currencies(self) -> List[dict]:
        logging.info("Listing all currencies")
        return list(self.currencies.values())

class File:
    def __init__(self, filename='currency_data.json', file_format='json'):
        self.filename = filename
        self.file_format = file_format

    def load_data(self):
        if self.file_format == 'json':
            with open(self.filename, 'r') as f:
                data = json.load(f)
                logging.info(f"Loaded data from {self.filename}")
                return data
        elif self.file_format == 'csv':
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                data = [row for row in reader]
                logging.info(f"Loaded data from {self.filename}")
                return data
        else:
            logging.error("Unsupported file format")
            return []

    def store_data(self, currencies: List[dict]):
        if self.file_format == 'json':
            with open(self.filename, 'w') as f:
                json.dump(currencies, f)
                logging.info(f"Stored data to {self.filename}")
        elif self.file_format == 'csv':
            with open(self.filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'amount'])
                writer.writeheader()
                writer.writerows(currencies)
                logging.info(f"Stored data to {self.filename}")

    def get_data(self, name: str) -> Union[dict, None]:
        data = self.load_data()
        for currency in data:
            if currency['name'] == name:
                logging.info(f"Retrieved currency from file: {currency}")
                return currency
        logging.warning(f"Currency not found in file: {name}")
        return None

    def update_currency(self, name: str, operation: str, new_value: float):
        data = self.load_data()
        for currency in data:
            if currency['name'] == name:
                if operation == "Add":
                    currency['amount'] += new_value
                elif operation == "Subtract":
                    currency['amount'] -= new_value
                self.store_data(data)
                logging.info(f"Updated currency in file: {currency}")
                return
        logging.warning(f"Currency not found in file for update: {name}")

    def backup_data(self, backup_filename='currency_backup.json'):
        os.rename(self.filename, backup_filename)
        logging.info(f"Backup created: {backup_filename}")

    def restore_data(self, backup_filename='currency_backup.json'):
        if os.path.exists(backup_filename):
            os.rename(backup_filename, self.filename)
            logging.info(f"Data restored from backup: {backup_filename}")
        else:
            logging.error("Backup file not found.")