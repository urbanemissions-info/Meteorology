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

# 5th Percentile
def q5(x):
    return x.quantile(0.05)
# 90th Percentile
def q95(x):
    return x.quantile(0.95)

# Calculate monthly average, 5th percentile, and 95th percentile
monthly_stats = citymet_df.groupby('month').agg({'tempc':[q5, q95, 'mean'],
                                                 'ws':[q5, q95, 'mean'],
                                                 'mixht':[q5, q95, 'mean']}).reset_index()

monthly_stats_daytime = citymet_df[(citymet_df['hour'] >=7)&(citymet_df['hour'] <=18)].groupby('month').agg({'tempc':[q5, q95, 'mean'],
                                                                                                    'ws':[q5, q95, 'mean'],
                                                                                                    'mixht':[q5, q95, 'mean']}).reset_index()

monthly_stats_nightime = citymet_df[(citymet_df['hour'] <=6)|(citymet_df['hour'] >=19)].groupby('month').agg({'tempc':[q5, q95, 'mean'],
                                                                                                    'ws':[q5, q95, 'mean'],
                                                                                                    'mixht':[q5, q95, 'mean']}).reset_index()


for var in ['tempc', 'ws', 'mixht']:
    plt.figure(figsize=(10, 6))
    #plt.plot(monthly_stats[('month', '')],
     #        monthly_stats[(var, 'mean')], color='black', marker='o', label='Monthly Average')
    
    plt.fill_between(monthly_stats_daytime[('month', '')],
                    monthly_stats_daytime[(var, 'q5')],
                    monthly_stats_daytime[(var, 'q95')], color='orange', alpha=0.3, label='Daytime variation')
    
    plt.fill_between(monthly_stats_nightime[('month', '')],
                    monthly_stats_nightime[(var, 'q5')],
                    monthly_stats_nightime[(var, 'q95')], color='gray', alpha=0.3, label='Nighttime variation')
    
    plt.xlabel('Month')
    plt.ylabel(var)
    plt.title('Variation in hourly '+var)
    plt.xticks(monthly_stats[('month', '')])
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.getcwd()+'/docs/'+city_name+'_'+var+'_hourlyvariationbyyear_'+year+'.jpg', bbox_inches='tight')