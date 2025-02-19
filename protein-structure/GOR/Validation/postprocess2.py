import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd

import pandas as pd


# Corrected data structure
data_corrected = {
    'Postprocessing': (
        ['No postprocessing'] * 3 + ['Postprocessing singular'] * 3 +
        ['Postprocessing singular and double'] * 3 + ['Postprocessing singular, double, and triple'] * 3
    ) * 3,
    'GOR Version': ['gor1', 'gor3', 'gor4'] * 4 * 3,
    'Type': ['H'] * 12 + ['E'] * 12 + ['C'] * 12,
    'Mean SOV': [
        # No postprocessing
        55.40, 41.26, 39.82,  # gor1, gor3, gor4 H
        55.84, 42.48, 30.58,  # gor1, gor3, gor4 E
        55.00, 41.14, 51.06,  # gor1, gor3, gor4 C
        # Postprocessing singular
        42.80, 37.68, 22.36,  # gor1, gor3, gor4 H
        0.52, 22.20, 44.50,   # gor1, gor3, gor4 E
        38.44, 56.76, 20.86,  # gor1, gor3, gor4 C
        # Postprocessing singular and double
        42.26, 37.50, 22.32,  # gor1, gor3, gor4 H
        0.26, 20.16, 43.96,   # gor1, gor3, gor4 E
        35.70, 59.22, 25.70,  # gor1, gor3, gor4 C
        # Postprocessing singular, double, and triple
        40.36, 36.76, 22.34,  # gor1, gor3, gor4 H
        0.26, 18.68, 44.00,   # gor1, gor3, gor4 E
        32.42, 57.92, 25.68   # gor1, gor3, gor4 C
    ]
}

# Create the DataFrame
df_corrected = pd.DataFrame(data_corrected)

# Creating the DataFrame
#df = pd.DataFrame(data)

import seaborn as sns
import matplotlib.pyplot as plt


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming df_corrected is your DataFrame with the correct structure


# Filter data for SOV_C
filtered_df_C = df_corrected[df_corrected['Type'] == 'C']
plt.figure(figsize=(10, 6))
sns.barplot(data=filtered_df_C, x='GOR Version', y='Mean SOV', hue='Postprocessing', palette='viridis')
plt.title('Mean SOV C by GOR Version and Postprocessing Type')
plt.xlabel('GOR Version')
plt.ylabel('Mean SOV C')

# Save the plot for SOV_C before showing it
plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/postprocessing_C_updated.png')
print('Plot for SOV C saved.')

# Show and then close the plot
plt.show()
plt.close()


"""
# Updated postprocessing data
data = {
    'Postprocessing': (
        ['No postprocessing'] * 3 + ['Postprocessing singular'] * 3 +
        ['Postprocessing singular and double'] * 3 + ['Postprocessing singular, double, and triple'] * 3
    ) * 3,
    'GOR Version': ['gor1', 'gor3', 'gor4'] * 4 * 3,
    'Type': ['H'] * 12 + ['E'] * 12 + ['C'] * 12,
    'Mean SOV': [
        # No postprocessing - H, E, C for gor1, gor3, gor4
        55.40, 55.84, 55.00, 41.26, 42.48, 41.14, 39.82, 30.58, 51.06,
        # Postprocessing singular
        42.80, 0.52, 38.44, 37.68, 22.20, 56.76, 22.36, 44.50, 20.86,
        # Postprocessing singular and double
        42.26, 0.26, 35.70, 37.50, 20.16, 59.22, 22.32, 43.96, 25.70,
        # Postprocessing singular, double, and triple
        40.36, 0.26, 32.42, 36.76, 18.68, 57.92, 22.34, 44.00, 25.68
    ]
}

# Creating the DataFrame
df_updated = pd.DataFrame(data)

# Display the first few rows of the dataframe to ensure it's constructed correctly
print(df_updated.head())


for letter in ['H', 'E', 'C']:
    filtered_df = df_updated[df_updated['Type'] == letter]
    plt.figure(figsize=(10, 6))
    sns.barplot(data=filtered_df, x='GOR Version', y='Mean SOV', hue='Postprocessing', palette='viridis')
    plt.title(f'Mean SOV {letter} by GOR Version and Postprocessing Type')
    plt.xlabel('GOR Version')
    plt.ylabel(f'Mean SOV {letter}')
    plt.savefig(f'C:/Users/test/PycharmProjects/propra24/crossVal/Postprocessing_{letter}.png')
    plt.close()

"""

