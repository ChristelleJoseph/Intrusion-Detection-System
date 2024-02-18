
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_target_category(data_dict):
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
    axes[1].tick_params(axis='x', rotation=90)

    plt.tight_layout()
    plt.show()
