import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Given data structure with Mean SOV values inserted
data = {
    'GOR Version': (
        ['gor1', 'gor3', 'gor4'] * 4 +
        ['gor1', 'gor3', 'gor4'] * 4 +
        ['gor1', 'gor3', 'gor4'] * 4
    ),
    'Postprocessing': (
        ['No postprocessing'] * 3 + ['Postprocessing singular'] * 3 +
        ['Postprocessing singular and double'] * 3 + ['Postprocessing singular, double, and triple'] * 3
    ) * 3,
    'Type': ['H'] * 12 + ['E'] * 12 + ['C'] * 12,
    'Mean SOV': [
        # H scores
        55.40, 41.26, 39.82, 39.06, 18.18, 1.44, 39.06, 17.34, 1.14, 37.32, 9.42, 0.36,
        # E scores
        55.84, 42.48, 30.58, 0.02, 46.12, 31.66, 0.00, 41.70, 28.70, 0.00, 40.52, 25.56,
        # C scores
        55.00, 41.14, 51.06, 35.42, 30.60, 15.66, 32.60, 37.58, 19.58, 29.72, 30.88, 13.44
    ]
}

df = pd.DataFrame(data)

# Separate the data by type
for letter in ['H', 'E', 'C']:
    filtered_df = df[df['Type'] == letter]
    plt.figure(figsize=(10, 6))
    sns.barplot(data=filtered_df, x='GOR Version', y='Mean SOV', hue='Postprocessing', palette='viridis')
    plt.title(f'Mean SOV {letter} by GOR Version and Postprocessing Type')
    plt.xlabel('GOR Version')
    plt.ylabel(f'Mean SOV {letter}')
    # Update the path as needed for your system
    plt.savefig(f'C:/Users/test/PycharmProjects/propra24/crossVal/postprocessing_{letter}.png')
    plt.close()




