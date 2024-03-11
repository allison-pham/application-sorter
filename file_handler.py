import pandas as pd

def read_file(file_path):
    return pd.read_csv(file_path)

def save_file(data, file_name = 'sorted_applications.csv'):
    data.to_csv(file_name, index = False)