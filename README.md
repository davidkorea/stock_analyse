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
1. data_df
```php
data_df = pd.read_csv('./csv')
```

```
<class 'pandas.core.frame.DataFrame'>
Int64Index: 20248 entries, 1520 to 26278
Data columns (total 7 columns):
year        20248 non-null int64
month       20248 non-null int64
day         20248 non-null int64
hour        20248 non-null int64
season      20248 non-null int64
PM_China    20248 non-null float64
PM_US       20248 non-null float64
dtypes: float64(2), int64(5)
memory usage: 1.2 MB
```
2. data format transform
```php
data_df['hour'] = data_df['hour'].astype('str') + ':00'
data_df['year'] = data_df['year'].astype('str')
data_df['month'] = data_df['month'].astype('str')
data_df['day'] = data_df['day'].astype('str')
```

```
 year month day   hour  season  PM_China  PM_US 
 2013     3   5   8:00       1     166.0  150.0 
 2013     3   5   9:00       1     165.0  163.0  
 2013     3   5  10:00       1     173.0  172.0   
 2013     3   5  11:00       1     182.0  192.0      
 2013     3   5  12:00       1     182.0  181.0    
```
```
<class 'pandas.core.frame.DataFrame'>
Int64Index: 20248 entries, 1520 to 26278
Data columns (total 9 columns):
year        20248 non-null object
month       20248 non-null object
day         20248 non-null object
hour        20248 non-null object
season      20248 non-null int64
PM_China    20248 non-null float64
PM_US       20248 non-null float64
dtypes: category(2), float64(2), int64(1), object(4)
memory usage: 1.3+ MB
```

3. combine datetime
```php
data_df['date'] = data_df['year'].str.cat( [ data_df['month'],data_df['day'] ], sep='-')
data_df['timestamp'] = data_df['date'].str.cat(data_df['hour'],sep=' ')
```
Multi-columns combine: new = A.str.cat( [ B, C ], sep='-' ) => A-B-C
```
     date       timestamp  
 2013-3-5   2013-3-5 8:00  
 2013-3-5   2013-3-5 9:00  
 2013-3-5  2013-3-5 10:00  
 2013-3-5  2013-3-5 11:00  
 2013-3-5  2013-3-5 12:00  
```

4. to_datetime
```php
data_df['timesatmp'] = pd.to_datetime(data_df['timesatmp'])
```
```
     date           timestamp  
 2013-3-5 2013-03-05 08:00:00  
 2013-3-5 2013-03-05 09:00:00  
 2013-3-5 2013-03-05 10:00:00  
 2013-3-5 2013-03-05 11:00:00  
 2013-3-5 2013-03-05 12:00:00  

```
5. set index
```php
data_df.set_index('timestamp', inplace=True)
```
index column has become to the 1st column.
```
                     year month day   hour  season  PM_China  PM_US 
timestamp                                                                      
2013-03-05 08:00:00  2013     3   5   8:00       1     166.0  150.0     
2013-03-05 09:00:00  2013     3   5   9:00       1     165.0  163.0      
2013-03-05 10:00:00  2013     3   5  10:00       1     173.0  172.0     
2013-03-05 11:00:00  2013     3   5  11:00       1     182.0  192.0     
2013-03-05 12:00:00  2013     3   5  12:00       1     182.0  181.0      
```
6. resample
```php
resampled_df = data_df.resample('D').mean()
```
all int/float columns will return resampled mean value
```
           season    PM_China       PM_US
timestamp                                 
2013-03-05     1.0  206.000000  216.937500
2013-03-06     1.0  222.217391  226.043478
2013-03-07     1.0  312.434783  323.826087
2013-03-08     1.0  231.863636  221.909091
2013-03-09     1.0   61.478261   61.695652
```
