import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Updated Data with Pseudocount 0
data = {
    'Pseudocount': ['0', '0', '0', '1', '1', '1', '10', '10', '10', '100', '100', '100'],
    'GOR_Version': ['GOR I', 'GOR III', 'GOR IV', 'GOR I', 'GOR III', 'GOR IV', 'GOR I', 'GOR III', 'GOR IV', 'GOR I', 'GOR III', 'GOR IV'],
    'Mean_SOV': [57.60, 40.64, 41.40, 34.58, 34.26, 24.50, 30.18, 33.96, 15.26, 31.96, 22.60, 14.38]
}

df = pd.DataFrame(data)

# Plotting with Seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='GOR_Version', y='Mean_SOV', hue='Pseudocount', data=df, palette='viridis')
plt.title('Parameter Tuning: Pseudocount')
plt.xlabel('GOR Version')
plt.ylabel('Mean SOV')
plt.legend(title='Pseudocount')

plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/SOV_pseudocounts_with0.png')
