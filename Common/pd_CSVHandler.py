# data_saver.py

import pandas as pd
import os

class DataSaver:
    def __init__(self, filename, columns=None):
        self.filename = os.path.join(os.getcwd(), filename)
        self.columns = columns or ['Timestamp', 'name','value']  # Default columns
        self._initialize_csv()

    def _initialize_csv(self):
        """
        Initialize the CSV file with headers if it doesn't exist.
        """
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.filename, index=False)

    def save_to_csv(self, data):
        """
        Append data to the CSV file using pandas DataFrame.
        :param data: List of data rows to be appended to the file.
        """
        df = pd.DataFrame(data, columns=self.columns)
        df.to_csv(self.filename, mode='a', header=False, index=False)
