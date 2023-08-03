import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# List of experiment numbers
experiment_numbers = ['E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E009', 'E010', 'E014', 'E015']

for exp in experiment_numbers:
    # loading and reading data for the current experiment
    df = pd.read_excel('W.xlsx', sheet_name='Dataset', usecols=['Experiment', 'Transportability'])

    # Filter data for the current experiment
    df_exp = df[df['Experiment'] == exp]

    # Check if all values are zero, skip irrelevant experiments
    if df_exp['Transportability'].sum() == 0:
        continue

    # Multiply all values in the 'Transportability' column by 100
    df_exp['Transportability'] *= 100

    # amputation of the NaN
    mean_value = df_exp['Transportability'].mean()
    df_exp['Transportability'].fillna(mean_value, inplace=True)

    # visualize the data using a histogram to get an initial understanding
    plt.hist(df_exp['Transportability'], bins='auto')  # 'auto' for the ideal number of bins
    plt.xlabel('Transportability')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of data for Experiment {exp}')
    plt.show()

    # calculate some statistics
    mean_value = df_exp['Transportability'].mean()
    median_value = df_exp['Transportability'].median()
    std_value = df_exp['Transportability'].std()
    skewness = df_exp['Transportability'].skew()
    kurtosis = df_exp['Transportability'].kurtosis()

    # print summary statistics
    print(f"\nSummary Statistics for Experiment {exp}:")
    print(f"Mean: {mean_value:.2f}")
    print(f"Median: {median_value:.2f}")
    print(f"Standard Deviation: {std_value:.2f}")
    print(f"Skewness: {skewness:.2f}")
    print(f"Kurtosis: {kurtosis:.2f}")
    
    # step 3: check which is best fit
    # fit the data to different distributions
    # normal dist
    normal = stats.norm.fit(df_exp['Transportability'])
    p_value_normal = stats.kstest(df_exp['Transportability'], 'norm', args=normal).pvalue

    # exponential dist
    exponential = stats.expon.fit(df_exp['Transportability'])
    p_value_exponential = stats.kstest(df_exp['Transportability'], 'expon', args=exponential).pvalue

    # log normal dist
    lognormal = stats.lognorm.fit(df_exp['Transportability'])
    p_value_lognormal = stats.kstest(df_exp['Transportability'], 'lognorm', args=lognormal).pvalue

    weibull = stats.exponweib.fit(df_exp['Transportability'])
    p_value_weibull = stats.kstest(df_exp['Transportability'], 'exponweib', args=weibull).pvalue

    # print them
    print("\nGoodness of Fit Test (Kolmogorov-Smirnov test) p-values:")
    print(f"Normal Distribution: {p_value_normal:.6f}")
    print(f"Exponential Distribution: {p_value_exponential:.6f}")
    print(f"Log-normal Distribution: {p_value_lognormal:.6f}")
    print(f"Weibull Distribution: {p_value_weibull:.6f}")

    # Choose the best fit distribution
    distribution_list = ['norm', 'expon', 'lognorm', 'exponweib']
    p_values = []

    for dist_name in distribution_list:
        dist = getattr(stats, dist_name)
        params = dist.fit(df_exp['Transportability'])
        p_value = stats.kstest(df_exp['Transportability'], dist_name, args=params).pvalue
        p_values.append(p_value)

    best_fit_index = np.argmax(p_values)
    best_fit_distribution = distribution_list[best_fit_index]
    best_fit_params = getattr(stats, best_fit_distribution).fit(df_exp['Transportability'])
    best_fit_p_value = p_values[best_fit_index]

    # print the best fit distribution and its parameters
    print(f"\nBest Fit Distribution for Experiment {exp}: {best_fit_distribution}")
    print(f"Best Fit Parameters: {best_fit_params}")
    print(f"Goodness of Fit (Kolmogorov-Smirnov test) p-value: {best_fit_p_value:.6f}")

    # generate data points for the best fit distribution PDF
    x = np.linspace(df_exp['Transportability'].min(), df_exp['Transportability'].max(), 1000)
    best_fit_pdf = getattr(stats, best_fit_distribution).pdf(x, *best_fit_params)

    # plot the histogram of the data
    plt.hist(df_exp['Transportability'], bins=15, density=True, alpha=0.6, label='Data')  # 'auto' for the ideal number of bins

    # plot the best fit distribution PDF
    plt.plot(x, best_fit_pdf, 'r', label=f'Best Fit {best_fit_distribution.capitalize()} Distribution')

    plt.xlabel('Transportability')
    plt.ylabel('Probability Density')
    plt.title(f'Histogram and Best Fit Distribution PDF for Experiment {exp}')
    plt.legend()
    plt.show()

    # plot the cumulative distribution function (CDF) of the best fit distribution
    best_fit_cdf = getattr(stats, best_fit_distribution).cdf(x, *best_fit_params)
    plt.plot(x, best_fit_cdf, 'g', label=f'Best Fit {best_fit_distribution.capitalize()} Distribution CDF')

    plt.xlabel('Transportability')
    plt.ylabel('Fraction')
    plt.title(f'CDF for Experiment {exp}')
    plt.legend()
    plt.show()
