# stock_analyse
tushare

# 1. Get stock data by tushare

```stock_df = tushare.get_k_data(code='600519', start='2010-01-01', end='2018-05-09',ktype='60')```

# 2. pandas

1. to_datetime
```php
stock_df['date'] = pd.to_datetime(stock_df['date'])
```
2. set datetime to index
```php
stock_df.set_index('date',inplace=True)
```
3. resample
```php
# resampled by day and set the last figure as this day's value
resampled_df = stock_df.resample('D').last()
resampled_df.dropna(inplace=True)
```
4. rolling(window=).func()
```php
resampled_df['MA 5'] = resampled_df['close'].rolling(window=5).mean()
```
5. plot
```php
resampled_df[ ['close','MA 5','MA 30','MA 60'] ].plot()
```

![](https://github.com/davidkorea/stock_analyse/blob/master/stock_plot.png)
