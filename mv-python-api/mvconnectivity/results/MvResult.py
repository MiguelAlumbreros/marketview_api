import pandas as pd

import csv
from io import StringIO

class MvResult:
    def __init__(self, csv_data, parsing_funcs=None):
        if not csv_data or csv_data.strip() == "":
            self.headers = []
            self.rows = []
            return
            
        reader = csv.reader(StringIO(csv_data))
        data = list(reader)

        self.headers = data[0]

        if parsing_funcs is not None:
            for i, row in enumerate(data[1:], start=1):
                for col_name, func in parsing_funcs.items():
                    param_name = col_name.split('-')[-1]
                    if param_name in self.headers:
                        col_index = self.headers.index(param_name)
                        data[i][col_index] = func(data[i][col_index])

        self.rows = [dict(zip(self.headers, row)) for row in data[1:]]

    def __str__(self):
        if not self.headers:
            return ""
            
        header_string = ', '.join(self.headers)
        row_strings = []
        for row in self.rows:
            row_string = ', '.join(str(row[header]) for header in self.headers)
            row_strings.append(row_string)
        
        all_rows = '\n'.join(row_strings)
        return f"{header_string}\n{all_rows}"  
  
    def to_dataframe(self):
        return pd.DataFrame(self.rows)