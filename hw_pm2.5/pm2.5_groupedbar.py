import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_df = pd.read_csv('./Beijing_PM.csv')
data_df.dropna(inplace=True)

#1 2013-2015 CN vs US
grouped_year_df = data_df.groupby('year')[ ['PM_China','PM_US'] ].mean()
grouped_year_df.plot(kind='bar',rot=0,title='2013-2015 CN vs US')
plt.tight_layout()
# plt.show()

#2 rank = [excellent,good,bad] stacked bar
data_df['Level_cn'] = pd.cut(data_df['PM_China'],
                             bins=[-np.inf,50,100,500,np.inf],
                             labels=['Excellent','Good','Bad','Die'])
data_df['Level_us'] = pd.cut(data_df['PM_US'],
                             bins=[-np.inf,50,100,500,np.inf],
                             labels=['Excellent','Good','Bad','Die'])
# pivot_df = pd.pivot_table(data_df,index='year',columns=['Level_cn','Level_us'],
#                           values=['day'],aggfunc='count')
# columns - outer level -> inner level
# values - different pivor due to diffenent value
pivot_cn = pd.pivot_table(data_df,index='year',columns=['Level_cn'],
                          values=['day'],aggfunc='count')
pivot_cn['day'].plot(kind='bar',stacked=True,rot=0)
# plt.show()

pivot_us = pd.pivot_table(data_df,index='year',columns=['Level_us'],
                       values=['day'],aggfunc='count')
pivot_us['day'].plot(kind='bar',stacked=True,rot=0)
# plt.show()

#3 Resample freq=1h -> 1day
data_df['hour'] = data_df['hour'].astype('str') + ':00'
data_df['year'] = data_df['year'].astype('str')
data_df['month'] = data_df['month'].astype('str')
data_df['day'] = data_df['day'].astype('str')
data_df['date'] = data_df['year'].str.cat([data_df['month'],
                                                data_df['day']],sep='-')
data_df['timestamp'] = data_df['date'].str.cat(data_df['hour'],sep=' ')
data_df['timestamp'] = pd.to_datetime(data_df['timestamp'])
data_df.set_index('timestamp',inplace=True)
resampled_df = data_df.resample('D').mean()
resampled_df['MA 7'] = resampled_df['PM_China'].rolling(window=5).mean()
resampled_df['MA 30'] = resampled_df['PM_China'].rolling(window=30).mean()
resampled_df[ ['PM_China','MA 7','MA 30'] ].plot()
plt.show()
