# -*- coding: utf-8 -*-

"""
    明确任务：
        计算指定股票的各项均线指标
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import tushare

stock_code = '600519'

# 结果保存路径
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)


def collect_data():
    """
        数据获取
    """
    stock_df = tushare.get_k_data(code=stock_code, start='2010-01-01', end='2018-01-01', ktype='60')
    return stock_df


def process_data(stock_df):
    """
        数据处理
    """
    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df.set_index('date', inplace=True)
    resampled_stock_df = stock_df.resample('D').last()
    resampled_stock_df.dropna(inplace=True)
    return resampled_stock_df


def analyze_data(stock_df):
    """
        数据分析
    """
    stock_df['MA 5'] = stock_df['close'].rolling(window=5).mean()
    stock_df['MA 30'] = stock_df['close'].rolling(window=30).mean()
    stock_df['MA 60'] = stock_df['close'].rolling(window=60).mean()

    return stock_df


def save_plot_results(stock_ext_df):
    """
        结果展示
    """
    stock_ext_df.to_csv(os.path.join(output_path, 'stock_ext.csv'))

    stock_ext_df[['close', 'MA 5', 'MA 30', 'MA 60']].plot()
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'stock_ext.png'))
    plt.show()


def main():
    """
        主函数
    """
    # 数据获取
    stock_df = collect_data()

    # 数据处理
    pro_stock_df = process_data(stock_df)

    # 数据分析
    stock_ext_df = analyze_data(pro_stock_df)


    save_plot_results(stock_ext_df)


if __name__ == '__main__':
    main()
