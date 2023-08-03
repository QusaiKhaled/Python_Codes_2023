import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Read data from Excel file
file_name = "Data.xlsx"
excel_data = pd.read_excel(file_name, sheet_name=None)

# Initialize lists to store results for each experiment
samples_list = []

# Process each experiment sheet
for experiment_title, df in excel_data.items():
    # Extract the transport times from the DataFrame
    times_transport = df['Transport_time']

    # Store the data for calibration
    samples_list.append(times_transport)

# Define a dictionary to map experiment titles to descriptive names
experiment_titles = {
    'E001': 'Experiment 1 (0.5 l/s, no_sed)',
    'E002': 'Experiment 2 (1.0 l/s, no_sed)',
    'E003': 'Experiment 3 (2.0 l/s, no_sed)',
    'E004': 'Experiment 4 (0.5 l/s, with_sed)',
    'E005': 'Experiment 5 (1.0 l/s, with_sed)',
    'E006': 'Experiment 6 (2.0 l/s, with_sed)'
}

# Plotting smoothed CDFs for each experiment
plt.figure(figsize=(10, 6))
plt.subplot(1, 1, 1)  # Single subplot for CDFs

for i, (experiment_title, df) in enumerate(excel_data.items()):
    # Perform KDE on the data
    kde = gaussian_kde(samples_list[i].dropna())
    x_vals = np.linspace(0, np.max(samples_list[i]), 1000)
    cdf_actual = np.cumsum(kde(x_vals)) / np.sum(kde(x_vals))

    # Scale the CDF with the % of elements that have transported
    scaled_cdf = cdf_actual * (len(samples_list[i]) - samples_list[i].isna().sum()) / len(samples_list[i])

    # Get the descriptive name from the dictionary
    descriptive_name = experiment_titles[experiment_title]

    if experiment_title in ['E001', 'E002', 'E003']:
        # Change line style for E001, E002, and E003 curves
        plt.plot(x_vals, scaled_cdf, label=descriptive_name, linestyle='--')
    else:
        # Use default line style for other curves (E004, E005, and E006)
        plt.plot(x_vals, scaled_cdf, label=descriptive_name)

plt.xlabel('Time of transport (seconds)')
plt.ylabel('Fraction of samples transported')
plt.legend(fontsize='small')  # Set the font size to 'small'
plt.grid(True)
plt.title('Scaled CDFs for Different Datasets using KDE')

plt.tight_layout()  # Adjust subplot spacing for better visualization
plt.show()
