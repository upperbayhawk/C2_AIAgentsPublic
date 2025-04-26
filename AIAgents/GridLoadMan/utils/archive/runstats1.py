import pandas as pd

# Read the CSV file
# Assuming the CSV file has columns: 'datetime', 'price', 'load'
df = pd.read_csv('../data/LMP_LOAD_meta.csv', parse_dates=['datetime'])

# Set datetime as the index
df.set_index('datetime', inplace=True)



# Define the 7-day period for analysis
start_date = '2023-06-01'
end_date = pd.to_datetime(start_date) + pd.Timedelta(days=7)

# Filter the dataframe to include only data within this 7-day window
df = df[(df.index >= start_date) & (df.index < end_date)]

# Resample data for each hour
hourly_stats = df.resample('7D').agg(['mean', 'min', 'max', 'std'])

print(hourly_stats)
