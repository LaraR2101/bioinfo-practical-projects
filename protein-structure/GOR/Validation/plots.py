import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""
# Given mean SOV results
data = {
    'WindowSize': ['11', '11', '11', '17', '17', '17', '23', '23', '23'],
    'GOR Version': ['gor1', 'gor3', 'gor4', 'gor1', 'gor3', 'gor4', 'gor1', 'gor3', 'gor4'],
    'Mean SOV': [56.88, 40.64, 19.32, 57.60, 40.64, 41.40, 54.58, 37.32, 32.42]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create the Seaborn plot for SOV scores
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sov_plot = sns.barplot(x='WindowSize', y='Mean SOV', hue='GOR Version', data=df, palette='viridis')

plt.title('Parameter Tuning: Window Size')
plt.xlabel('Window Size')
plt.ylabel('Mean SOV Score')

# Save the plot
plt.savefig('mean_sov_scores_windowSize.png')



# Adjusted data based on the mean SOV for each window size with gor versions.
adjusted_data = {
    'GOR Version': ['gor1', 'gor1', 'gor1', 'gor3', 'gor3', 'gor3', 'gor4', 'gor4', 'gor4'],
    'Window Size': ['11', '17', '23', '11', '17', '23', '11', '17', '23'],
    'Mean SOV': [56.88, 57.60, 54.58, 40.64, 40.64, 37.32, 19.32, 41.40, 32.42]
}

# Create a DataFrame from the adjusted data
adjusted_df = pd.DataFrame(adjusted_data)

# Create the grouped bar chart with Window Size as hue
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
adjusted_barplot = sns.barplot(x='GOR Version', y='Mean SOV', hue='Window Size', data=adjusted_df, palette='viridis')

plt.title('Parameter Tuning: Window Size')
plt.xlabel('GOR Version')
plt.ylabel('Mean SOV')

# Save the plot
plt.savefig('mean_sov_scores_windowSize2.png')

# Show the plot
plt.show()




pseudocounts_data = {
    'GOR Version': ['gor1', 'gor1', 'gor1', 'gor3', 'gor3', 'gor3', 'gor4', 'gor4', 'gor4'],
    'Window Size': ['1', '10', '100', '1', '10', '100', '1', '10', '100'],
    'Mean SOV': [34.58, 30.18, 31.96, 34.26, 33.96, 22.60, 24.50, 15.26, 14.38]
}

# Create a DataFrame from the corrected data
pseudocounts_df = pd.DataFrame(pseudocounts_data)

# Create the grouped bar chart with PseudoCount as hue
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
pseudocounts_plot = sns.barplot(x='GOR Version', y='Mean SOV', hue='PseudoCount', data=pseudocounts_df, palette='viridis')

plt.title('Parameter Tuning: Pseudocounts')
plt.xlabel('GOR Version')
plt.ylabel('Mean SOV Score')

# Save the plot
plt.savefig('mean_SOV_parameter_tuning_pseudocounts.png')

# Show the plot
#plt.show()



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt







# Create a DataFrame from the corrected data
pseudocounts_df = pd.DataFrame(pseudocounts_data)

# Create the grouped bar chart with PseudoCount as hue
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
pseudocounts_plot = sns.barplot(x='GOR Version', y='Mean SOV', hue='PseudoCount', data=pseudocounts_df, palette='viridis')

plt.title('Parameter Tuning: Pseudocounts')
plt.xlabel('GOR Version')
plt.ylabel('Mean SOV Score')

# Save the plot
plt.savefig('parameter_tuning_by_pseudocounts_corrected.png')

# Show the plot
plt.show()

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Data
data = {
    'Pseudocount': ['1', '1', '1', '10', '10', '10', '100', '100', '100'],
    'GOR_Version': ['GOR I', 'GOR III', 'GOR IV', 'GOR I', 'GOR III', 'GOR IV', 'GOR I', 'GOR III', 'GOR IV'],
    'Mean_SOV': [34.58, 34.26, 24.50, 30.18, 33.96, 15.26, 31.96, 22.60, 14.38]
}

df = pd.DataFrame(data)

# Plotting with Seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='GOR_Version', y='Mean_SOV', hue='Pseudocount', data=df, palette='viridis')
plt.title('Parameter Tuning: Pseudocount')
plt.xlabel('GOR Version')
plt.ylabel('Mean SOV')
plt.legend(title='Pseudocount')

plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/SOV_parameter_tuning_pseudocounts.png')




# Adjusted data based on the mean SOV for each window size with gor versions.
adjusted_data = {
    'GOR Version': ['gor1', 'gor1', 'gor1', 'gor3', 'gor3', 'gor3', 'gor4', 'gor4', 'gor4'],
    'Window Size': ['11', '17', '23', '11', '17', '23', '11', '17', '23'],
    'Mean SOV': [56.88, 57.60, 54.58, 40.64, 40.64, 37.32, 19.32, 41.40, 32.42]
}

# Create a DataFrame from the adjusted data
adjusted_df = pd.DataFrame(adjusted_data)

# Create the grouped bar chart with Window Size as hue
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
adjusted_barplot = sns.barplot(x='GOR Version', y='Mean SOV', hue='Window Size', data=adjusted_df, palette='viridis')

plt.title('Parameter Tuning: Window Size')
plt.xlabel('GOR Version')
plt.ylabel('Mean SOV')

# Save the plot
plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/sov_tuning_windowSize.png')



#postprocessing

# New dataset
data = {
    'Postprocessing': ['No postprocessing'] * 3 + ['Singular'] * 3 + ['Singular and Double'] * 3 + ['Singular, Double, and Triple'] * 3,
    'GOR_Version': ['GOR I', 'GOR III', 'GOR IV'] * 4,
    'q3': [
        61.18, 57.30, 59.06,
        53.38, 35.14, 19.08,
        53.30, 35.68, 19.70,
        52.88, 31.98, 19.08,
    ],
    'SOV': [
        57.60, 40.64, 41.40,
        31.26, 30.74, 16.00,
        30.18, 33.36, 16.72,
        28.48, 27.64, 13.40,
    ],
    'SOV_H': [
        55.40, 41.26, 39.82,
        39.06, 18.18, 1.44,
        39.06, 17.34, 1.14,
        37.32, 9.42, 0.36,
    ],
    'SOV_E': [
        55.84, 42.48, 30.58,
        0.02, 46.12, 31.66,
        0.00, 41.70, 28.70,
        0.00, 40.52, 25.56,
    ],
    'SOV_C': [
        55.00, 41.14, 51.06,
        35.42, 30.60, 15.66,
        32.60, 37.58, 19.58,
        29.72, 30.88, 13.44,
    ]
}

# Converting to DataFrame
df = pd.DataFrame(data)

# Melt the DataFrame to make it suitable for seaborn's barplot
df_melted = df.melt(id_vars=['Postprocessing', 'GOR_Version'], var_name='Metric', value_name='Value')

# Plotting
plt.figure(figsize=(14, 8))
sns.barplot(x='GOR_Version', y='Value', hue='Postprocessing', data=df_melted[df_melted['Metric'] == 'SOV'])
plt.title('Postprocessing: Removing Biologically Impossible Predictions')
plt.xlabel('GOR Version')
plt.ylabel('Value')
plt.legend(title='Postprocessing')

plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/sov_postprocessing.png')
