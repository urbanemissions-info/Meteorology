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


# Create separate line plots for each month
months = citymet_df['month'].unique()
#  Define custom colors for each month
custom_colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'lime', 'indigo']

for var in ['tempc', 'ws', 'mixht']:
    # Calculate mean precipitation for each hour in each month
    hourly_means = citymet_df.groupby(['month', 'hour'])[var].mean().reset_index()
    
    plt.figure()
    for idx, month in enumerate(months):
        monthly_data = hourly_means[hourly_means['month'] == month]
        if month in ['Jan', 'Feb', 'Mar', 'Oct', 'Nov', 'Dec']:
            linestyle = 'dashed'
        else:
            linestyle = 'solid'
        plt.plot(monthly_data['hour'], monthly_data[var],
                 linestyle=linestyle, label=f'{month}', color=custom_colors[idx])

    plt.xlabel('Hour')
    plt.ylabel('Precipitation')
    plt.title('Hourly {} for Different Months'.format(var))
    plt.xticks(range(24))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.getcwd()+'/docs/'+city_name+'_'+var+'_diurnal_'+year+'.jpg', bbox_inches='tight')
