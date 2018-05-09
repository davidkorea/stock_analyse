import pandas as pd
import matplotlib.pyplot as plt

data_df = pd.read_csv('./hw_pm1.csv')
data_df['Timestamp'] = pd.to_datetime(data_df['Timestamp'])
# print(data_df.info()
data_df.set_index('Timestamp',inplace=True)

resampled_df = data_df.resample('D').mean()

resampled_df['MA 3'] = resampled_df['PM'].rolling(window=3).mean()
resampled_df['MA 5'] = resampled_df['PM'].rolling(window=5).mean()
resampled_df['MA 7'] = resampled_df['PM'].rolling(window=7).mean()

resampled_df.plot()
plt.show()