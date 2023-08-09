import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, NelsonAalenFitter
from lifelines.statistics import logrank_test

# Load the data from the Excel file into a pandas DataFrame (replace 'TheMammoth.xlsx' with your actual data file)
data = pd.read_excel('TheMammoth.xlsx', sheet_name='Vault')

# Replace NaN values in the "Time" column with 200
data["Time"].fillna(200, inplace=True)

# Create an 'Event' column based on the 'Time' values
data['Event'] = data['Time'].apply(lambda x: 1 if x != 200 else 0)

# Filter the data based on the specified settings
selected_discharge = [2.0]  # Changed to 0.5
selected_types = ["Caps", "20%_Multi-Caps"]  # Added "20%_Multi-Caps"
selected_sediments = ["No"]  # Changed to "No"
filtered_data = data[(data['Discharge'].isin(selected_discharge)) & 
                     (data['Type'].isin(selected_types)) & 
                     (data['Sediments'].isin(selected_sediments))]

# Create instances of KaplanMeierFitter and NelsonAalenFitter
kmf = KaplanMeierFitter()
naf = NelsonAalenFitter()

# Plot the Kaplan-Meier survival curves and Nelson-Aalen cumulative hazard curves
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

for sediment_setting in selected_sediments:
    group_data = filtered_data[(filtered_data['Sediments'] == sediment_setting)]

    for discharge in selected_discharge:
        for type_ in selected_types:
            type_group_data = group_data[(group_data['Discharge'] == discharge) & (group_data['Type'] == type_)]

            kmf.fit(durations=type_group_data["Time"], event_observed=type_group_data["Event"])
            kmf.plot_survival_function(ax=ax1, label=f'Discharge {discharge} l/s, Type {type_}, Sediments {sediment_setting}', ci_show=False)

            naf.fit(durations=type_group_data["Time"], event_observed=type_group_data["Event"])
            naf.plot_cumulative_hazard(ax=ax2, label=f'Discharge {discharge} l/s, Type {type_}, Sediments {sediment_setting}', ci_show=False)

            # Calculate log-rank test
            result = logrank_test(type_group_data[type_group_data['Time'] <= 180]['Time'], type_group_data[type_group_data['Time'] <= 180]['Event'], type_group_data[type_group_data['Time'] <= 180]['Time'])
            print(f'Log-Rank Test for Discharge {discharge} l/s, Type {type_}, Sediments {sediment_setting}: p-value = {result.p_value}')
            
            # Calculate and display median survival time
            median = kmf.median_survival_time_
            print("Median survival time for Type", type_, "is", median)

ax1.set_xlabel('Time')
ax1.set_ylabel('Survival Probability')
ax1.set_title('Kaplan-Meier Survival Curves')
ax1.legend(loc='best')
ax1.set_xlim(0, 180)  # Set the x-axis range
ax1.grid(True)

ax2.set_xlabel('Time')
ax2.set_ylabel('Cumulative Hazard (rate of occurrence)')
ax2.set_title('Nelson-Aalen Cumulative Hazard Curves')
ax2.legend(loc='best')
ax2.set_xlim(0, 180)  # Set the x-axis range
ax2.grid(True)

plt.tight_layout()
plt.show()
