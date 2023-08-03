import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data from the Excel file
data = pd.read_excel('W.xlsx')

# List of experiment numbers
experiment_numbers = ['E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007', 'E008', 'E009', 'E010', 'E013', 'E014', 'E015']

# Create a list to store data for each experiment
experiment_data = [data[data['Experiment'] == exp]['Transportability'] for exp in experiment_numbers]

# Set up the figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Custom color palette for the box plots
custom_colors = {
    'E001': 'lightcoral',
    'E002': 'red',
    'E003': 'darkred',
    'E004': 'lightgreen',
    'E005': 'limegreen',
    'E006': 'green',
    'E007': 'lightyellow',
    'E008': 'yellow',
    'E009': 'darkkhaki',
    'E010': 'blue',
    'E013': 'lightpink',
    'E014': 'pink',
    'E015': 'hotpink',
}

# Plot 1: Box plot without data points (Original)
sns.boxplot(x="Experiment", y="Transportability", data=data, order=experiment_numbers, palette=custom_colors, ax=axes[0])
axes[0].set_xlabel('Experiment')
axes[0].set_ylabel('Transportability (1/s)')  # Add the unit to the y-axis label
axes[0].set_title('Box Plot without Data Points')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)

# Plot 2: Box plot with data points (New)
sns.boxplot(x="Experiment", y="Transportability", data=data, order=experiment_numbers, showfliers=False, palette=custom_colors, ax=axes[1])
sns.stripplot(x="Experiment", y="Transportability", data=data, order=experiment_numbers, color="black", size=4, jitter=True, ax=axes[1])
axes[1].set_xlabel('Experiment')
axes[1].set_ylabel('Transportability (1/s)')  # Add the unit to the y-axis label
axes[1].set_title('Box Plot with Data Points')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)

# Adjust the layout to avoid overlapping titles and labels
plt.tight_layout()

# Show the plots
plt.show()
