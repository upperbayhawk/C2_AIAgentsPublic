import pandas as pd


def is_float(str_val):
    try:
        float(str_val)
        return True
    except ValueError:
        return False
# Calibrate the game level and duration to max the value proposition for homes
# algol 

# Read the CSV file
# Assuming the CSV file has columns: 'datetime', 'price', 'load'
df_stats = pd.read_csv('../data/LMP_LOAD_STATS.csv', parse_dates=['datetime'])
df_stats.set_index('datetime', inplace=True)
df_stats.index = df_stats.index.date

df_data = pd.read_csv('../data/LMP_LOAD_META.csv', parse_dates=['datetime'])
df_data.set_index('datetime', inplace=True)
df_data.index = df_data.index.date

"""
df_stats_all = pd.read_csv('../data/LMP_LOAD_STATS.csv', parse_dates=['datetime'])
df_stats_all.set_index('datetime', inplace=True)

df_data_all = pd.read_csv('../data/LMP_LOAD_META.csv', parse_dates=['datetime'])
df_data_all.set_index('datetime', inplace=True)
"""
# Iterating over rows using iterrows()
bronze_games_price = 0
bronze_games_load = 0
bronze_price = 75
bronze_price_std = 50

silver_games_price = 0
silver_games_load = 0
silver_price = 125
silver_price_std = 25

gold_games_price = 0
gold_games_load = 0
#250/150000
gold_price = 200
gold_price_std = 10


bronze_load = 80000
bronze_load_std = 15000

silver_load = 110000
silver_load_std = 18000

gold_load=140000
gold_load_std = 20000

#my_datetime = ""
my_lastday = ""
# Iterating over rows using iterrows()
for index, row in df_stats.iterrows():
    #print(f"Row Index: {index}")
    my_datetime = index
     # Iterating through columns in the row
    for column_name, value in row.items():
        #print(f"Column: {column_name}, Value: {value}")

        """
        if column_name == "price_mean":
            if (is_float(value)):
                if(float(value) > gold_price):
                    print("gold_price at " + str(my_datetime))
                elif (float(value) > silver_price):
                    print("silver_price at " + str(my_datetime))
                elif (float(value) > bronze_price):
                    print("bronze_price at " + str(my_datetime))
                
        if column_name == "price_min":
            if (is_float(value)):
                if(float(value) < 0.0):
                    print("price_min < 00 at " + str(my_datetime))
        """
        if column_name == "price_max":
            if my_lastday != my_datetime:
                my_lastday = my_datetime
                if (is_float(value)):
                    if(float(value) > gold_price):
                        gold_games_price = gold_games_price + 1
                        print("alert gold_price at " + str(my_datetime))
                        std = row["price_std"]
                        mean = row["price_mean"]
                        load_max = row["load_max"]
                        load_std = row["load_std"]
                        #print("alert gold_price std " + str(std) + " " + str(mean))
                        #
                        my_row =df_data.loc[my_datetime]
                        my_row_price = my_row["price"]
                        #print("real price " + str(my_row_price))
                    elif (float(value) > silver_price):
                        #print("silver_price at " + str(my_datetime))
                        silver_games_price = silver_games_price + 1
                    elif (float(value) > bronze_price):
                        #print("bronze_price at " + str(my_datetime))
                        bronze_games_price = bronze_games_price + 1

"""
        if do_std == True:
            if column_name == "price_std":
                if (is_float(value)):
                    if(float(value) > 0.0):
                        pass
                        print("alert gold_price_std: " + str(value))
                    elif (float(value) > silver_price_std):
                        #print("silver_price_std at " + str(my_datetime))
                        silver_games = silver_games + 1
                    elif (float(value) > bronze_price_std):
                        #print("bronze_price_std at " + str(my_datetime))
                        bronze_games = bronze_games + 1
            do_std = False
"""
# Add a separator for readability between rows
print("---")

my_lastday = ""


for index, row in df_stats.iterrows():
    my_datetime = index
     #print(f"Row Index: {index}")
    # Iterating through columns in the row

    for column_name, value in row.items():
       # print(f"Column: {column_name}, Value: {value}")
        """
        if column_name == "load_mean":
            if (is_float(value)):
                if(float(value) > 120000.0):
                    print("load_mean > 120000 at " + str(my_datetime))
        if column_name == "load_min":
            if (is_float(value)):
                if(float(value) > 100000.0):
                    print("load_min > 100000 at " + str(my_datetime))
        """
        
        if column_name == "load_max":
            if my_lastday != my_datetime:
                my_lastday = my_datetime
                if (is_float(value)):
                    if(float(value) > gold_load):
                        gold_games_load = gold_games_load + 1
                        print("alert gold_load at " + str(my_datetime))
                        load_std = row["load_std"]
                        load_mean = row["load_mean"]
                        price_std = row["price_std"]
                        price_max = row["price_max"]
                        #print("alert gold_load std " + str(load_std) + " " + str(load_mean))
                        #print("alert gold_load price " + str(price_max))
                        my_row =df_data.loc[my_datetime]
                        my_row_price = my_row["price"]
                        #print("real price " + str(my_row_price))
                    elif (float(value) > silver_load):
                        silver_games_load = silver_games_load + 1
                        #print("silver_load at " + str(my_datetime))
                    elif (float(value) > bronze_load):
                        #print("bronze_load at " + str(my_datetime))
                        bronze_games_load = bronze_games_load + 1
                        pass

"""
        if do_std == True:
            if column_name == "load_std":
                if (is_float(value)):
                    if(float(value) > 0.0):
                        print("alert gold_load_std on " + str(my_datetime))
                        #gold_games = gold_games + 1
                        pass
                    elif (float(value) > silver_load_std):
                        #print("silver_load_std at " + str(my_datetime))
                        silver_games = silver_games + 1
                    elif (float(value) > bronze_load_std):
                        #print("bronze_load_std at " + str(my_datetime))
                        bronze_games = bronze_games + 1
            do_std = False
"""
    # Add a separator for readability between rows
    #print("---")

print ("gold_games_price = " + str(gold_games_price))
print ("gold_games_load = " + str(gold_games_load))
print ("silver_games_price = " + str(silver_games_price))
print ("silver_games_load = " + str(silver_games_load))
print ("bronze_games_price = " + str(bronze_games_price))
print ("bronze_games_load = " + str(bronze_games_load))

