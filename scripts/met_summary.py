import pandas as pd
import os
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt

citymet_df = pd.read_csv(os.getcwd()+'/data/lucknow.2018.houravg.csv')
citymet_df['year']  =2018
citymet_df['datetime'] = pd.to_datetime(citymet_df[['year', 'month', 'day', 'hour']])
#Convert GMT to IST
citymet_df['datetime'] = citymet_df['datetime'] + timedelta(hours=5, minutes=30)
citymet_df['month'] = citymet_df['datetime'].dt.strftime('%b') # Convert month numbers to month names
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
citymet_df['month'] = pd.Categorical(citymet_df['month'], categories=month_order, ordered=True)

# Calculate wind speed (ws)
citymet_df['ws'] = np.sqrt(citymet_df['u10']**2 + citymet_df['v10']**2)

# Calculate wind direction (wd) in degrees
citymet_df['wd'] = (180 / np.pi) * np.arctan2(citymet_df['u10'], citymet_df['v10']) + 180

# Calculate wind direction categories- 8 Categories
def categorize_wind_direction_8(degrees):
    categories = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = int((degrees + 22.5) / 45) % 8
    return categories[index]
# Choose colors for wind direction categories
colors_8 = {'N': '#F79646', 'NE': '#984807', 'E': '#8EB341', 'SE': '#B9CDE5',
            'S': '#558ED5', 'SW': '#215968', 'W': '#4F6228', 'NW': '#731C1A'}

# Calculate wind direction categories - N, E, W, S
def categorize_wind_direction_4(degrees):
    if 45 <= degrees < 135:
        return 'E'
    elif 135 <= degrees < 225:
        return 'S'
    elif 225 <= degrees < 315:
        return 'W'
    else:
        return 'N'
# Choose colors for wind direction categories
colors_4 = {'N': '#F79646', 'E': '#8EB341', 'S': '#558ED5', 'W': '#4F6228'}


def categorize_wind_speed(speed):
    if speed < 2:
        return '<2'
    elif 2 <= speed < 4:
        return '2-4'
    elif 4 <= speed < 6:
        return '4-6'
    elif 6 <= speed < 8:
        return '6-8'
    else:
        return '>8'
# Choose colors for wind speed categories
colors_ws = {'<2': '#984807', '2-4': '#E46C0A', '4-6': '#F79646', '6-8': '#FCD5B5', '>8':'#D9D9D9'}

def categorize_mixing_height(mixht):
    if mixht < 100:
        return '<100'
    elif 100 <= mixht < 500:
        return '100-500'
    elif 500 <= mixht < 1000:
        return '500-1K'
    elif 1000 <= mixht < 2000:
        return '1K-2K'
    else:
        return '>2000'
# Choose colors for MIXHT categories
colors_mixht = {'<100': '#403152', '100-500': '#604A7B', '500-1K': '#B3A2C7', '1K-2K': '#FFFF00', '>2000':'#4F6228'}


def categorize_tempc(tempc):
    if tempc < 15:
        return '<15'
    elif 15 <= tempc < 20:
        return '15-20'
    elif 20 <= tempc < 25:
        return '20-25'
    elif 25 <= tempc < 30:
        return '25-30'
    elif 30 <= tempc < 35:
        return '30-35'
    else:
        return '>35'
# Choose colors for wind direction categories
colors_tempc = {'<15': '#10253F', '15-20': '#376092', '20-25': '#C6D9F1', 
                '25-30': '#F8F8F8', '30-35':'#E6B9B8', '>35':'#953735'}


citymet_df['wd_category_8'] = citymet_df['wd'].apply(categorize_wind_direction_8)
citymet_df['wd_category_4'] = citymet_df['wd'].apply(categorize_wind_direction_4)
citymet_df['ws_category'] = citymet_df['ws'].apply(categorize_wind_speed)
citymet_df['mixht_category'] = citymet_df['mixht'].apply(categorize_mixing_height)
citymet_df['tempc_category'] = citymet_df['tempc'].apply(categorize_tempc)

citymet_df['total_hours'] = citymet_df.groupby('month')['datetime'].transform('count')
citymet_df['percentage_wd_8'] = (citymet_df.groupby(['month', 'wd_category_8'])['datetime'].transform('count') / citymet_df['total_hours']) * 100
citymet_df['percentage_wd_4'] = (citymet_df.groupby(['month', 'wd_category_4'])['datetime'].transform('count') / citymet_df['total_hours']) * 100
citymet_df['percentage_ws'] = (citymet_df.groupby(['month', 'ws_category'])['datetime'].transform('count') / citymet_df['total_hours']) * 100
citymet_df['percentage_mixht'] = (citymet_df.groupby(['month', 'mixht_category'])['datetime'].transform('count') / citymet_df['total_hours']) * 100
citymet_df['percentage_tempc'] = (citymet_df.groupby(['month', 'tempc_category'])['datetime'].transform('count') / citymet_df['total_hours']) * 100

citymet_df.to_csv(os.getcwd()+'/data/lucknow.2018.houravg_processed.csv', index=False)

# PLOTS - 8 Wind Directions
plt.figure()
pivot_df = citymet_df.pivot_table(index='month', columns='wd_category_8', values='percentage_wd_8', fill_value=0)
pivot_df = pivot_df[['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']] 
ax = pivot_df.plot(kind='bar', stacked=True, color=[colors_8[col] for col in pivot_df.columns])
plt.title('Wind Direction Distribution in Each Month')
plt.xlabel('Month')
plt.xticks(rotation=0)  # Ensure month names are not rotated
plt.ylabel('Percentage of Hours')
ax.legend(title='Wind Direction', bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=8)
# Adjust figure layout for legend
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_8winddirection_stacked.jpg', bbox_inches='tight')

# Create a pie chart for wind direction distribution over the entire year
plt.figure()
yearly_distribution = citymet_df['wd_category_8'].value_counts(normalize=True) * 100
yearly_distribution.plot(kind='pie', autopct='%1.1f%%',
                         colors=[colors_8[cat] for cat in yearly_distribution.index])
plt.title('Wind Direction Distribution for the Year')
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_8winddirection_pie.jpg', bbox_inches='tight')


# PLOTS - 4 Wind Directions
plt.figure()
pivot_df = citymet_df.pivot_table(index='month', columns='wd_category_4', values='percentage_wd_4', fill_value=0)
pivot_df = pivot_df[['N', 'E', 'S', 'W']] 
ax = pivot_df.plot(kind='bar', stacked=True, color=[colors_4[col] for col in pivot_df.columns])
plt.title('Wind Direction Distribution in Each Month')
plt.xlabel('Month')
plt.xticks(rotation=0)  # Ensure month names are not rotated
plt.ylabel('Percentage of Hours')
ax.legend(title='Wind Direction', bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=4)
# Adjust figure layout for legend
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_4winddirection_stacked.jpg', bbox_inches='tight')

plt.figure()
yearly_distribution = citymet_df['wd_category_4'].value_counts(normalize=True) * 100
yearly_distribution.plot(kind='pie', autopct='%1.1f%%',
                         colors=[colors_4[cat] for cat in yearly_distribution.index])
plt.title('Wind Direction Distribution for the Year')
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_4winddirection_pie.jpg', bbox_inches='tight')

# PLOTS - 5 Wind Speeds
plt.figure()
pivot_df = citymet_df.pivot_table(index='month', columns='ws_category', values='percentage_ws', fill_value=0)
pivot_df = pivot_df[['<2', '2-4', '4-6', '6-8', '>8']] 

ax = pivot_df.plot(kind='bar', stacked=True, color=[colors_ws[col] for col in pivot_df.columns])
plt.title('Wind Direction Distribution in Each Month')
plt.xlabel('Month')
plt.xticks(rotation=0)  # Ensure month names are not rotated
plt.ylabel('Percentage of Hours')
ax.legend(title='Wind Direction', bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=8)
# Adjust figure layout for legend
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_5windspeed_stacked.jpg', bbox_inches='tight')

plt.figure()
yearly_distribution = citymet_df['ws_category'].value_counts(normalize=True) * 100
yearly_distribution.plot(kind='pie', autopct='%1.1f%%',
                         colors=[colors_ws[cat] for cat in yearly_distribution.index])
plt.title('Wind Speed Distribution for the Year')
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_5windspeed_pie.jpg', bbox_inches='tight')

# PLOTS - 5 MIXHT
plt.figure()
pivot_df = citymet_df.pivot_table(index='month', columns='mixht_category', values='percentage_mixht', fill_value=0)
pivot_df = pivot_df[['<100', '100-500', '500-1K', '1K-2K', '>2000']] 
ax = pivot_df.plot(kind='bar', stacked=True, color=[colors_mixht[col] for col in pivot_df.columns])
plt.title('Wind Direction Distribution in Each Month')
plt.xlabel('Month')
plt.xticks(rotation=0)  # Ensure month names are not rotated
plt.ylabel('Percentage of Hours')
ax.legend(title='Wind Direction', bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=8)
# Adjust figure layout for legend
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_5mixht_stacked.jpg', bbox_inches='tight')

plt.figure()
yearly_distribution = citymet_df['mixht_category'].value_counts(normalize=True) * 100
yearly_distribution.plot(kind='pie', autopct='%1.1f%%',
                         colors=[colors_mixht[cat] for cat in yearly_distribution.index])
plt.title('Wind Direction Distribution for the Year')
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_5mixht_pie.jpg', bbox_inches='tight')


# PLOTS - 6 TEMP
plt.figure()
pivot_df = citymet_df.pivot_table(index='month', columns='tempc_category', values='percentage_tempc', fill_value=0)
pivot_df = pivot_df[['<15', '15-20', '20-25', '25-30', '30-35', '>35']] 
ax = pivot_df.plot(kind='bar', stacked=True, color=[colors_tempc[col] for col in pivot_df.columns])
plt.title('Wind Direction Distribution in Each Month')
plt.xlabel('Month')
plt.xticks(rotation=0)  # Ensure month names are not rotated
plt.ylabel('Percentage of Hours')
ax.legend(title='Wind Direction', bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=8)
# Adjust figure layout for legend
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_6tempc_stacked.jpg', bbox_inches='tight')

plt.figure()
yearly_distribution = citymet_df['tempc_category'].value_counts(normalize=True) * 100
yearly_distribution.plot(kind='pie', autopct='%1.1f%%',
                         colors=[colors_tempc[cat] for cat in yearly_distribution.index])
plt.title('Wind Direction Distribution for the Year')
plt.tight_layout()
plt.savefig(os.getcwd()+'/docs/met_summary_6tempc_pie.jpg', bbox_inches='tight')

