# Import Libraries
import pandas as pd
import numpy as np

# Read the csv files
df = pd.read_csv('ab_data.csv')
df_country = pd.read_csv('countries.csv')

# Checking the details
df.head()
df.info()
df.shape #(294478, 5)
df.dtpyes
df.isnull().sum() #No blanks present

df_country.head()
df_country.info()
df_country.shape #(290584, 2)
df_country.dtpyes
df_country.isnull().sum() #No blanks present

#Changing the dtype and format of timestamp column
df.timestamp = pd.to_datetime(df.timestamp)
df.timestamp = df.timestamp.dt.floor('s')

# Checking for the unique values before merging
df.user_id.duplicated().sum() #3894
len(df.user_id.unique()) #290584
df_country.user_id.duplicated().sum() #0
len(df_country.user_id.unique()) #290584

# Merging the dataframes on the basis of user_id column
df_merged = pd.merge(df, df_country, on='user_id', how='inner')

# Checking for duplicate rows
df_merged.duplicated().sum() #No duplicate rows

# Checking for duplicate user_ids
df_merged.user_id.duplicated().sum() #3894

# The duplicate user_ids are to be removed. For users with multiple records we
# take their max conversion status. Hence the dataframe has to be sorted based on the conversion status
df_sorted = df_merged.sort_values('converted', ascending=False)
df_deduplicated = df_sorted.drop_duplicates('user_id', keep='first')
df_deduplicated.shape #(290584, 6)

# Let us filter out incorrect assignments
filt1 = df_deduplicated[(df_deduplicated['group'] == 'control') & (df_deduplicated['landing_page'] == 'old_page')]
filt1.shape #(144252, 6)

filt2 = df_deduplicated[(df_deduplicated['group'] == 'treatment') & (df_deduplicated['landing_page'] == 'new_page')]
filt2.shape #(144349, 6)

# The cleaned filters can be joined
df_cleaned = pd.concat([filt1, filt2])
df_cleaned.shape #(288601, 6)

# Aggregating and creating the columns as series
total_users = df_cleaned.groupby('group').user_id.count()
converted_users = df_cleaned.groupby('group').converted.sum()

# Calculating the conversion rate
conversion_rate = converted_users/total_users

#Constructing the final dataframe
df_final = pd.concat({'Total_users':total_users, 'Converted_users':converted_users, 'Conversion_rate':conversion_rate}, axis=1).rename_axis('Group')
df_final.shape #(2, 3)

# Importing library for z-test
from statsmodels.stats.proportion import proportions_ztest

# Sort the dataframe as required]
df_final.sort_index(ascending=False, inplace=True)

# Perform the z-test
z_stat, p_val = proportions_ztest(df_final.Converted_users, df_final.Total_users, alternative='larger')
z_stat #(-1.3599629336810064)
p_val #(0.9130791730945382)

# Importing libraries to plot a graph
import matplotlib.pyplot as plt
import seaborn as sns

# Plotting the graph
labels = ['control', 'treatment']
plt.figure(figsize=(8, 6))
plt.bar(labels, conversion_rate, color=sns.color_palette("pastel"))
plt.title('A/B Test: Conversion Rate', fontsize=14)
plt.xlabel('Group', fontsize=12)
plt.ylabel('Conversion Rate', fontsize=12)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1%}'))
plt.ylim(0, max(conversion_rate) * 1.3)
plt.tight_layout()
print("Generated ab_test_conversion_rate.png")