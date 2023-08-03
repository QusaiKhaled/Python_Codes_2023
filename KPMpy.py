import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

# Load the data from the Excel file into a pandas DataFrame (replace 'W.xlsx' and 'Y4shuffled' with your actual data file and sheet name)
data = pd.read_excel('W2.xlsx', sheet_name='Y4shuffled')

# Create an instance of KaplanMeierFitter
kmf = KaplanMeierFitter()

# Separate the data into groups based on the values of "Discharge" (assuming it's a categorical variable)
groups = data['Discharge'].unique()

# Plot the Kaplan-Meier survival curve for each group
plt.figure(figsize=(8, 6))
for group in groups:
    group_data = data[data['Discharge'] == group]
    kmf.fit(durations=group_data["Transportability"], event_observed=[True] * len(group_data))
    kmf.plot_survival_function(label=f'Discharge {group} l/s')

plt.xlabel('Transportability')
plt.ylabel('Survival Probability')
plt.title('Kaplan-Meier Survival Curves for Different Discharge Levels and Transportability')
plt.legend(loc='best')
plt.grid(True)
plt.show()
