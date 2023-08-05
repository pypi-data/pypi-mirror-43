# sort-dataframeby-monthorweek
It sorts a dataframe by month names or by week names

Assume a dataframe has a month name column and one wants to sort the dataframe by month column in chronological order, this package helps to do that. This package can also be used to sort dataframe by weekday column.

# How to install
    pip install sort-dataframeby-monthorweek
    
There are 4 different functions in this package. We will see usage of below mentioned functions.

```python
    Sort_Dataframeby_Month
    Sort_Dataframeby_Weekday
```

# Example1
In this example we will see how to sort a sample dataframe by month name column
``` python
    import pandas as pd
    
    df = pd.DataFrame([['Feb',254],['Apr',420],['Jan',301],['Mar',449]],columns=['Month','Sales'])
    df
    Out: 
      Month  Sales
    0   Feb    254
    1   Apr    420
    2   Jan    301
    3   Mar    449
```
Now, use Sort_Dataframeby_Month function to sort above dataframe
``` python
    df_sort = sort_dataframeby_monthorweek.Sort_Dataframeby_Month(df=df,monthcolumnname='Month')
    df_sort
    Out:
      Month  Sales
    0   Jan    301
    1   Feb    254
    2   Mar    449
    3   Apr    420
```

# Example2
In this example we will see how to sort a sample dataframe by weekday column

``` python
    df1 = pd.DataFrame([['Tue',25],['Thu',42],['Mon',30],['Wed',44]],columns=['Weekday','Sales'])
    df1
    Out: 
      Weekday  Sales
    0     Tue     25
    1     Thu     42
    2     Mon     30
    3     Wed     44
```
Now, use Sort_Dataframeby_Weekday function to sort df1

``` python
    df1_sort = sort_dataframeby_monthorweek.Sort_Dataframeby_Weekday(df=df1,Weekdaycolumnname='Weekday')
    df1_sort
    Out: 
      Weekday  Sales
    0     Mon     30
    1     Tue     25
    2     Wed     44
    3     Thu     42
```
Above functions work for lower, upper and mixed case months or weekdays. It works for full names of months ('January') and weekdays ('Monday') as well.
