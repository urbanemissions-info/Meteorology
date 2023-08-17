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


monthly_precip = citymet_df.groupby('month')[['precip']].sum()

plt.figure()
ax = monthly_precip.plot(kind='bar')
plt.title('Total precipitation (mm/month)')
plt.xlabel('Month')
plt.xticks(rotation=0)  # Ensure month names are not rotated
plt.ylabel('mm')
# Adjust figure layout for legend
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/'+city_name+'_precip_statsbymonth_'+year+'.jpg', bbox_inches='tight')

