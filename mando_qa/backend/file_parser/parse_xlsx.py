# parse_xlsx.py
import pandas as pd

def parse_xlsx(file_path):
    xl = pd.ExcelFile(file_path)
    return "\n\n".join([xl.parse(sheet).to_string() for sheet in xl.sheet_names])
