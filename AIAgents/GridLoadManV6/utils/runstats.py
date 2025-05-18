import pandas as pd

# Read the CSV file
# Assuming the CSV file has columns: 'datetime', 'price', 'load'
df = pd.read_csv('../data/LMP_LOAD_META.csv', parse_dates=['datetime'])

# Set datetime as the index
df.set_index('datetime', inplace=True)

# Ensure the data is sorted by datetime
df = df.sort_index()

# Apply a rolling window of 7 days
# Note: '7D' signifies a 7-day rolling window
rolling_df = df.rolling('7D')

# Calculate statistics for each window
# Mean, min, max, and standard deviation
stats = rolling_df.agg(['mean', 'min', 'max', 'std'])

#print(stats)

# Your previous code to create the 'stats' DataFrame
# ...

# Set pandas options to display more rows
pd.set_option('display.max_rows', None)  # None means no truncation

# Now print the DataFrame
#print(stats)
stats.to_csv('../data/LMP_LOAD_STATS.csv', index=True)


# Iterate through columns and then through each element in the column

