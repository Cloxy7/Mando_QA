import pandas as pd
import re
import json

def is_math_question(question):
    keywords = [
        "average", "mean", "sum", "total", "count",
        "maximum", "max", "minimum", "min", "median", "unique"
    ]
    return any(kw in question.lower() for kw in keywords)

def handle_math_fallback(question, file_path):
    # === Load structured file ===
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".json"):
            with open(file_path) as f:
                data = json.load(f)
            df = pd.json_normalize(data)
        else:
            return "Unsupported file type for math fallback."

        df.columns = [col.strip() for col in df.columns]
    except Exception as e:
        return f"❌ Could not parse structured file: {e}"

    q = question.lower()
    results = []

    # === Preprocess: map lowercase columns to real ones ===
    col_map = {col.lower(): col for col in df.columns}

    # === Chained: "sum of mean of A and B" ===
    if "sum of mean of" in q:
        match = re.findall(r"mean of ([\w_]+)", q)
        matched = [col_map[c.lower()] for c in match if c.lower() in col_map]
        if matched:
            total = 0
            for col in matched:
                if pd.api.types.is_numeric_dtype(df[col]):
                    total += df[col].mean()
                    results.append(f"Mean of '{col}': {df[col].mean():.4f}")
            results.append(f"Sum of means: {total:.4f}")
            return "\n".join(results)

    # === Per-column logic ===
    for col_lower, col_real in col_map.items():
        if col_lower in q:
            col_data = df[col_real].dropna()

            if "average" in q or "mean" in q:
                if pd.api.types.is_numeric_dtype(col_data):
                    results.append(f"Mean of '{col_real}': {col_data.mean():.4f}")
            if "maximum" in q or "max" in q:
                if pd.api.types.is_numeric_dtype(col_data):
                    results.append(f"Max of '{col_real}': {col_data.max():.4f}")
            if "minimum" in q or "min" in q:
                if pd.api.types.is_numeric_dtype(col_data):
                    results.append(f"Min of '{col_real}': {col_data.min():.4f}")
            if "sum" in q or "total" in q:
                if pd.api.types.is_numeric_dtype(col_data):
                    results.append(f"Sum of '{col_real}': {col_data.sum():.4f}")
            if "count" in q:
                results.append(f"Count in '{col_real}': {col_data.count()}")
            if "median" in q:
                if pd.api.types.is_numeric_dtype(col_data):
                    results.append(f"Median of '{col_real}': {col_data.median():.4f}")
            if "unique" in q:
                results.append(f"Unique values in '{col_real}': {list(col_data.unique())}")

    return "\n".join(results) if results else "❌ I couldn't detect a valid math operation or column from your question."
