import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Data with Q3 values for different pseudocounts and GOR versions
data = {
    'Pseudocount': ['0', '0', '0', '1', '1', '1', '10', '10', '10', '100', '100', '100'],
    'GOR_Version': ['GOR I', 'GOR III', 'GOR IV', 'GOR I', 'GOR III', 'GOR IV', 'GOR I', 'GOR III', 'GOR IV', 'GOR I', 'GOR III', 'GOR IV'],
    'Mean_Q3': [61.18, 57.30, 59.06, 54.60, 55.34, 37.76, 52.82, 55.10, 20.06, 53.58, 34.94, 18.78]
}

df = pd.DataFrame(data)

# Plotting with Seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='GOR_Version', y='Mean_Q3', hue='Pseudocount', data=df, palette='viridis')
plt.title('Parameter Tuning: Pseudocounts')
plt.xlabel('GOR Version')
plt.ylabel('Mean Q3')
plt.legend(title='Pseudocount')

plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/Q3__pseudocounts.png')






import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Updated data based on the mean Q3 for each window size with gor versions.
adjusted_data = {
    'GOR Version': ['gor1', 'gor1', 'gor1', 'gor3', 'gor3', 'gor3', 'gor4', 'gor4', 'gor4'],
    'Window Size': ['11', '17', '23', '11', '17', '23', '11', '17', '23'],
    'Mean Q3': [60.48, 61.18, 56.10, 57.26, 57.30, 51.82, 30.00, 59.06, 50.62]
}

# Create a DataFrame from the adjusted data
adjusted_df = pd.DataFrame(adjusted_data)

# Create the grouped bar chart with Window Size as hue
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
adjusted_barplot = sns.barplot(x='GOR Version', y='Mean Q3', hue='Window Size', data=adjusted_df, palette='viridis')

plt.title('Parameter Tuning: Window Size')
plt.xlabel('GOR Version')
plt.ylabel('Mean Q3')

# Save the plot
plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/q3_tuning_windowSize.png')

