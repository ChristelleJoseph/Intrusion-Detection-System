
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

csv_path = './data'
# csv_path = './generated_csv'

def clean_data(df):
    df.columns = df.columns.str.strip()
    if 'Label' in df.columns:
        df['Label'] = df['Label'].str.replace('�', '-', regex=False)
    df = df.drop_duplicates()
    df = df.dropna(axis=1, how='any')
    return df

def get_data(csv_path):
    data = {}
    file_dir = os.listdir(csv_path)

    for file in sorted(file_dir):
        if file.endswith('.csv'):
            full_path = os.path.join(csv_path, file)
            df = pd.read_csv(full_path)
            cleaned_df = clean_data(df)
            data[file] = cleaned_df

    return data

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def combine_and_plot(data_dict):
    dfs_with_label = [df for df in data_dict.values() if 'Label' in df.columns]

    combined_df = pd.concat(dfs_with_label, ignore_index=True)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    label_counts = combined_df['Label'].value_counts().sort_values(ascending=False)
    sns.countplot(y='Label', data=combined_df, palette='viridis', order=label_counts.index, ax=axes[0])
    axes[0].set_xscale('log')
    axes[0].set_title('Cumulative Distribution of Attack Types (Log Scale)')
    axes[0].set_xlabel('Frequency (Log Scale)')
    axes[0].set_ylabel('Attack Type')

    sns.countplot(x='Label', data=combined_df, palette='viridis', order=label_counts.index, ax=axes[1])
    axes[1].set_yscale('log')
    axes[1].set_title('Cumulative Distribution of Attack Types (Log Scale)')
    axes[1].set_ylabel('Frequency (Log Scale)')
    axes[1].set_xlabel('Attack Type')
    axes[1].tick_params(axis='x', rotation=90)  # Rotate x-axis labels for better readability

    plt.tight_layout()
    plt.show()

print(combine_and_plot(get_data(csv_path)))
