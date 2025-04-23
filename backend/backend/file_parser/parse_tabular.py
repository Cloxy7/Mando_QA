# file_parser/parse_tabular.py

import pandas as pd
import json
import os

def parse_csv(file_path):
    df = pd.read_csv(file_path)
    return dataframe_to_text(df, file_path)

def parse_excel(file_path):
    df = pd.read_excel(file_path)
    return dataframe_to_text(df, file_path)

def parse_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    try:
        df = pd.json_normalize(data)
        return dataframe_to_text(df, file_path)
    except Exception:
        return f"Raw JSON:\n{json.dumps(data, indent=2)}"

def dataframe_to_text(df, file_path):
    summary = f"File: {os.path.basename(file_path)}\n"
    summary += f" Shape: {df.shape[0]} rows × {df.shape[1]} columns\n\n"
    summary += "Columns:\n"
    summary += ", ".join(df.columns) + "\n\n"
    preview = df.head(5).to_markdown(index=False)
    summary += f"Preview (first 5 rows):\n{preview}"
    return summary


