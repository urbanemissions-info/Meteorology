import pandas as pd
import os
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt

met_file = 'lucknow.2018.houravg.csv'
city_name = met_file.split('.')[0]
year = met_file.split('.')[1]

citymet_df = pd.read_csv(os.getcwd()+'/data/'+met_file)
citymet_df['year']  =year
citymet_df['datetime'] = pd.to_datetime(citymet_df[['year', 'month', 'day', 'hour']])

#Convert GMT to IST
citymet_df['datetime'] = citymet_df['datetime'] + timedelta(hours=5, minutes=30)

citymet_df['month'] = citymet_df['datetime'].dt.strftime('%b') # Convert month numbers to month names
citymet_df['day'] = citymet_df['datetime'].dt.day
citymet_df['hour'] = citymet_df['datetime'].dt.hour

month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
citymet_df['month'] = pd.Categorical(citymet_df['month'], categories=month_order, ordered=True)
# Calculate wind speed (ws)
citymet_df['ws'] = np.sqrt(citymet_df['u10']**2 + citymet_df['v10']**2)

# Calculate daily averages for each month
for var in ['tempc', 'mixht', 'ws']:
    monthly_averages_allday = citymet_df.groupby(['month', 'day'])[var].mean().reset_index()
    monthly_averages_daytime = citymet_df[(citymet_df['hour'] >=7)&(citymet_df['hour'] <=18)].groupby(['month', 'day'])[var].mean().reset_index()
    monthly_averages_nighttime = citymet_df[(citymet_df['hour'] <=6)|(citymet_df['hour'] >=19)].groupby(['month', 'day'])[var].mean().reset_index()

    # Pivot the data to create the table with months as columns
    pivot_table = monthly_averages_allday.pivot(index='day', columns='month', values=var)
    pivot_table.to_csv(os.getcwd()+'/data/'+city_name+'.'+year+'.'+var+'_allday_bymonth.csv', index=False)

    pivot_table = monthly_averages_daytime.pivot(index='day', columns='month', values=var)
    pivot_table.to_csv(os.getcwd()+'/data/'+city_name+'.'+year+'.'+var+'_daytime_bymonth.csv', index=False)

    pivot_table = monthly_averages_nighttime.pivot(index='day', columns='month', values=var)
    pivot_table.to_csv(os.getcwd()+'/data/'+city_name+'.'+year+'.'+var+'_nighttime_bymonth.csv', index=False)

