# parse_txt.py
def parse_txt(file_path):
    with open(file_path, 'r') as f:
        return f.read()
