import pandas as pd
import matplotlib.pyplot as plt
import tushare

stock_code = '600519'

def collect_data():
    stock_df = tushare.get_k_data(
        code=stock_code, start='2010-01-01', end='2018-05-09',ktype='60'
    )
    return stock_df

def process_data(stock_df):
    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df.set_index('date',inplace=True)
    resampled_df = stock_df.resample('D').last()
    resampled_df.dropna(inplace=True)
    return resampled_df

def analyse_data(resampled_df):
    resampled_df['MA 5'] = resampled_df['close'].rolling(window=5).mean()
    resampled_df['MA 30'] = resampled_df['close'].rolling(window=30).mean()
    resampled_df['MA 60'] = resampled_df['close'].rolling(window=60).mean()
    return resampled_df


def plot(resampled_df):
    resampled_df[ ['close','MA 5','MA 30','MA 60'] ].plot()
    plt.tight_layout()
    plt.show()

def main():
    stock_df = collect_data()
    resampled_df = process_data(stock_df)
    resampled_df = analyse_data(resampled_df)
    plot(resampled_df)

main()