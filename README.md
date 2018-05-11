# stock_analyse
tushare

# 0. Basic

![](https://github.com/davidkorea/stock_analyse/blob/master/images/resample.jpg)
![](https://github.com/davidkorea/stock_analyse/blob/master/images/freq.jpg)
![](https://github.com/davidkorea/stock_analyse/blob/master/images/rolling.jpg)

# 1. Get stock data by tushare

```stock_df = tushare.get_k_data(code='600519', start='2010-01-01', end='2018-05-09',ktype='60')```

# 2. pandas

1. to_datetime
```php
stock_df['date'] = pd.to_datetime(stock_df['date'])
```

```
               date    open   close    high     low   volume    code
0  2017-11-08 14:00  649.31  652.50  654.45  648.10  11824.0  600519
1  2017-11-08 15:00  652.50  650.38  652.50  647.17   9766.0  600519
2  2017-11-09 10:30  648.00  652.23  654.15  644.90  13409.0  600519
3  2017-11-09 11:30  652.00  648.25  652.39  647.55   6765.0  600519
4  2017-11-09 14:00  648.25  647.17  649.10  646.00   5350.0  600519
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
 - **ONLY yyyy-mm-dd hh:mm could be resampled**
 - Because of Index column being set already, do NOT need to **stock_df['date']**.resample('D').last()
 
4. rolling(window=).func()
```php
resampled_df['MA 5'] = resampled_df['close'].rolling(window=5).mean()
```
5. plot
```php
resampled_df[ ['close','MA 5','MA 30','MA 60'] ].plot()
```

![](https://github.com/davidkorea/stock_analyse/blob/master/stock_plot.png)

# 3. UPGRATED CASE

combine multi-columns to datetime and set to index, rolling

## 3.1 CSV data preview
```
 year  month  day  hour  season  PM_China  PM_US
 2013      3    5     8       1     166.0  150.0
 2013      3    5     9       1     165.0  163.0
 2013      3    5    10       1     173.0  172.0
 2013      3    5    11       1     182.0  192.0
 2013      3    5    12       1     182.0  181.0
```

## 3.2 Codes
