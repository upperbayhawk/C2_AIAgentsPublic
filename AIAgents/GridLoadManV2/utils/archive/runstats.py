import pandas as pd

# Read the CSV file
# Assuming the CSV file has columns: 'datetime', 'price', 'load'
df = pd.read_csv('../data/LMP_LOAD_meta.csv', parse_dates=['datetime'])

# Filter dates between June 1, 2023, and October 3, 2023

start_date = '2023-06-01'
end_date = '2023-10-03'
df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

# Set datetime as the index
df.set_index('datetime', inplace=True)

# Resample data for each 7-day period and calculate statistics
stats = df.resample('7D').agg(['mean', 'min', 'max', 'std'])

print(stats)
