import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, ks_2samp

# Read data from Excel file
file_name = "excel.xlsx"
excel_data = pd.read_excel(file_name, sheet_name=None)

# Initialize lists to store results for each experiment
samples_list = [df['Transportability'].dropna().values for df in excel_data.values()]

# Define a dictionary to map experiment titles to descriptive names
experiment_titles = {
    '100': 'Experiment 100 (Description)',
    '50': 'Experiment 50 (Description)',
    '40': 'Experiment 40 (Description)',
    '30': 'Experiment 30 (Description)',
    '20': 'Experiment 20 (Description)'
}

# Plotting smoothed CDFs for each experiment
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)  # Subplot for CDFs

# Define a list of colors to use for each curve
colors = ['blue', 'green', 'red', 'purple', 'orange']

for i, (experiment_title, transportability) in enumerate(excel_data.items()):
    # Perform KDE on the data
    kde = gaussian_kde(samples_list[i].T)  # Transpose the data to 1D array
    x_vals = np.linspace(0, np.max(samples_list[i]), 1000)
    cdf_actual = np.cumsum(kde(x_vals)) / np.sum(kde(x_vals))

    # Get the descriptive name from the dictionary
    descriptive_name = experiment_titles[experiment_title]

    # Plot the CDF curve with a unique color for each experiment
    plt.plot(x_vals, cdf_actual, label=descriptive_name, color=colors[i])

plt.xlabel('Time of transport (seconds)')
plt.ylabel('Fraction of samples transported')
plt.legend(fontsize='small')  # Set the font size to 'small'
plt.grid(True)
plt.title('CDFs for Different Datasets using KDE')

# Calculate KS distance between pairs of experiments
pairs_to_compare = [('100', '50'), ('100', '40'), ('100', '30'), ('100', '20')]

ks_distances = []  # List to store KS distances
sample_sizes = []  # List to store sample sizes

for pair in pairs_to_compare:
    experiment1, experiment2 = pair
    data1 = samples_list[list(experiment_titles.keys()).index(experiment1)]
    data2 = samples_list[list(experiment_titles.keys()).index(experiment2)]
    ks_statistic, _ = ks_2samp(data1, data2)
    ks_distances.append(ks_statistic)
    sample_sizes.append(len(data2))

# Subplot for KS distance vs. sample size
plt.subplot(1, 2, 2)
plt.plot(sample_sizes, ks_distances, marker='o', linestyle='-', color='b')
plt.xlabel('Number of Samples')
plt.ylabel('KS Distance')
plt.title('KS Distance vs. Number of Samples')
plt.grid(True)

plt.tight_layout()  # Adjust subplot spacing for better visualization
plt.show()
