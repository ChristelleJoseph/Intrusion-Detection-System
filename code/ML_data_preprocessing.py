
import os
import pandas as pd

def get_data():


def clean_training_data():
    csv_files = []
    csv_path = './data'
    file_dir = os.listdir(csv_path)
    for file in file_dir:
        csv_files.append(file)

    data = {}
    for name, filename in sorted(zip(csv_files, file_dir)):
        data[name] = pd.read_csv(os.path.join(csv_path, filename))



def clean_network_data(df):
    pass
