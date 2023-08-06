import pandas as pd
import itertools as it
import functools as ft


def multi_args(function, constants, variables, isProduct=False, maxLimit=None):
    """
    Run a function on different parameters and
    aggregate results
    function
        function to be parametrized
    constants
        arguments that would remain constant
        throughtout all the scenarios
        dictionary with key being argument name
        and value being the argument value
    variables
        arguments that need to be varied
        dictionary with key being argument name
        and value being list of argument values
        to substitute
    isProduct
        list of variables for which all combinations
        are to be tried out.
    maxLimit
        Maximum number of simulations to be run
        before terminating. Useful in case of long
        running simulations.
        default 1000

    By default, this function zips through each of the
    variables but if you need to have the Cartesian
    product, specify those variables in isProduct.

    returns a Series with different variables and
    the results
    """
    from functools import partial
    import concurrent.futures

    if maxLimit:
        MAX_LIMIT = maxLimit
    else:
        MAX_LIMIT = 1000

    func = partial(function, **constants)
    arg_list = []
    if isProduct:
        args = it.product(*variables.values())
    else:
        args = zip(*variables.values())
    keys = variables.keys()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        tasks = []
        for i, arg in enumerate(args):
            kwds = {a: b for a, b in zip(keys, arg)}
            tasks.append(executor.submit(func, **kwds))
            arg_list.append(arg)
            i += 1
            if i >= MAX_LIMIT:
                print('MAX LIMIT reached', MAX_LIMIT)
                break
    result = [task.result() for task in tasks]
    s = pd.Series(result)
    s.name = 'values'
    s.index = pd.MultiIndex.from_tuples(arg_list, names=keys)
    return s


def stop_loss(price, stop_loss, order='B', tick_size=0.05):
    """
    Return the stop loss for the order
    price
        price from which stop loss is to be calculated
    stop_loss
        stop loss percentage from price
    order
        the original order type - B for Buy and S for Sell
        If the original order is buy, then a sell stop
        loss is generated and vice-versa
    tick_size
        tick_size to be rounded off
    >>> stop_loss(100, 3)
    >>> 97

    Notes
    ------
    * passing a negative value may throw unexpected results
    * raises ValueError if order is other than B or S

    """
    if order == 'B':
        return tick(price * (1 - stop_loss * 0.01), tick_size)
    elif order == 'S':
        return tick(price * (1 + stop_loss * 0.01), tick_size)
    else:
        raise ValueError('order should be either B or S')


def tick(price, tick_size=0.05):
    """
    Rounds a given price to the requested tick
    """
    return round(price / tick_size)*tick_size


def create_orders(data, rename, **kwargs):
    """
    create an orders dataframe from an existing dataframe
    by renaming columns and providing additional columns
    data
        dataframe
    rename
        columns to be renamed as dictionary
    kwargs
        key value pairs with key being column names
        and values being dataframe values
    """
    data = data.rename(rename, axis='columns')
    for k, v in kwargs.items():
        data[k] = v
    return data


def recursive_merge(dfs, on=None, how='inner', columns={}):
    """
    Recursively merge all dataframes in the given list

    Given a list of dataframes, merge them based on index or columns.
    By default, dataframes are merged on index. Specify the **on**
    argument to merge by columns. The "on" columns should be available
    in all the dataframes

    Parameters
    -----------
    dfs
        list of dataframes
    on
        columns on which the dataframes are to be merged.
        By default, merge is done on index
    how
        how to apply the merge
        {'left', 'right', 'outer', 'inner'}, default 'inner'.
        Same as pandas merge
    columns
        To return only specific columns from specific dataframes,
        pass them as a dictionary with key being the index of the 
        dataframe in the list and value being the list of columns
        to merge. **your keys should be string**
        See examples for more details
        >>> recursive_merge(dfs, columns = {'1': ['one', 'two']})
        Fetch only the columns one and two from the second dataframe
    """
    data = dfs[0]
    for i, d in enumerate(dfs[1:], 1):
        if columns.get(str(i)):
            cols = list(columns.get(str(i)))
            cols.extend(on)
        else:
            cols = d.columns

        if on is None:
            data = data.merge(d[cols], how=how, left_index=True, right_index=True)
        else:
            data = data.merge(d[cols], how=how, on=on)
    return data


def get_nearest_option(spot, n=1, opt='C', step=100):
    """
    Given a spot price, calculate the nearest options
    spot
        spot price of the instrument
    n
        number of nearest option prices
    opt
        call or put option. 'C' for call and 'P' for put
    step
        step size of the option price
    returns a list of options
    >>> get_nearest_option(23457, 2)
    >>> [23400, 23500]
    >>> get_nearest_option(23457, 2, 'P')
    >>> [23400, 23300]    
    All calculations are based on in the money option. So,
    get_nearest_option(24499) would return 24400
    """
    in_money = int(spot/step) * step
    option_prices = []
    for i in range(n):
        if opt == 'C':
            strike = in_money + step*i
            option_prices.append(strike)
        elif opt == 'P':
            strike = in_money - step*i
            option_prices.append(strike)
        else:
            print('Option type not recognized; Check the opt argument')
    return option_prices

def calendar(start, end, holidays=None, alldays=False,
             start_time=None, end_time=None, freq='D', **kwargs):
    """
    Generate a calendar removing the list of
    given holidays.
    Provide date arguments as strings in the
    format **YYYY-MM-DD**
    start
        start date of the period
    end
        end date of the period
    holidays
        list of holidays as strings
    alldays
        True/False
        True to generate dates for all days
        including weekends. default: False  
    start_time
        start time for each day as string
    end_time
        end time for each day as string     
    freq
        frequency of the calendar
    kwargs
        kwargs to the pandas date range function

    Note
    -----
    1) This function is slow, especially when generating
    timestamps. So, use them only once at the start
    of your program for better performance
    2) This function generates calendar only for 
    business days. To use all the available days,
    se the alldays argument to True

    """
    if alldays:
        dfunc = ft.partial(pd.date_range, freq='D', **kwargs)
    else:
        dfunc = ft.partial(pd.bdate_range, freq='B', **kwargs)

    dates = list(dfunc(start=start, end=end))
    if (holidays):
        holidays = [pd.to_datetime(dt) for dt in holidays]
        for hol in holidays:
            dates.remove(hol)

    # Initialize times
    if (start_time or end_time):
        if not(start_time):
            start_time = "00:00:00"
        if not(end_time):
            end_time = "23:59:59"
        timestamps = []
        fmt = "{:%Y%m%d} {}"
        for d in dates:
            start_ts = fmt.format(d, start_time)
            end_ts = fmt.format(d, end_time)
            ts = pd.date_range(start=start_ts, end=end_ts, freq=freq, **kwargs)
            timestamps.extend(ts)
        return timestamps
    else:
        return dates

def get_ohlc_intraday(data, start_time, end_time, date_col=None,
        col_mappings=None, sort=False):
    """
    Get ohlc for a specific period in a day for all days
    for all the symbols.
    data
        dataframe with symbol, timestamp, date, open, high, low, close columns.
        The timestamp and date columns are assumed to be of pandas datetime type.
        Each row represents data for a single stock at a specified period of time
        If you have different column names, use the col_mappings argument
        to rename the columns
    start_time
        start time for each day
    end_time
        end time for each day
    date_col
        date column to aggregate; this is in addition to time column.
        If no date column is specified, a date column is created.
    col_mappings
        column mappings as a dictionary
        (Eg.) if the symbol column is named as assetName and timestamp
        as ts, then pass rename={'assetName': 'symbol', 'ts': 'timestamp'}
    sort
        Whether the data is sorted by timestamp.
        If True, data is not sorted else data is sorted

    returns
        a dataframe with symbol, date, open, high, low and close columns

    Note
    -----
    To speed up computation
        1) If the data is already sorted, pass sort=True
        2) If date column is already available, then pass date_col=column_name
    Timestamp and date are assumed to be pandas datetime
    """
    if col_mappings:
        data = data.rename(col_mappings, axis='columns')
    if not(sort):
        data = data.sort_values(by='timestamp')
    if not(date_col):
        data['date'] = data['timestamp'].dt.date
        date_col = 'date'
    data = data.set_index('timestamp')

    def calculate_ohlc(df):
        """
        Internal function to calculate OHLC
        """

        date = df.iloc[0].at[date_col].strftime('%Y-%m-%d')
        fmt = "{date} {time}" # date time format
        s = fmt.format(date=date, time=start_time)
        e = fmt.format(date=date, time=end_time)
        temp = df.loc[s:e]
        agg = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'}
        return temp.groupby('symbol').agg(agg)
    return data.groupby([date_col]).apply(calculate_ohlc)


def get_expanding_ohlc(data, freq, col_mappings=None):
    """
    Given a dataframe with OHLC, timestamp and symbol columns
    return a OHLC dataframe with open price, expanding high,
    expanding low and close prices
    data
        dataframe with OHLC, timestamp and symbol columns
    freq
        frequency by which the data is to be resampled.
        A pandas frequency string
    col_mappings
        column mappings as a dictionary
        (Eg.) if the symbol column is named as assetName and timestamp
        as ts, then pass rename={'assetName': 'symbol', 'ts': 'timestamp'}
    Note
    -----
    The returned dataframe has the same length and index of the 
    original dataframe. The resampling is done only to calculate the
    expanding high, low prices   
    """
    if col_mappings:
        data = data.rename(col_mappings, axis='columns')

    def calculate_ohlc(df):
        temp = pd.DataFrame({
        'high': df['high'].expanding().max(),
        'low': df['low'].expanding().min()
        })
        temp['close'] = df['close']
        temp['open'] = df['open'].iloc[0]
        return temp

    cols = ['open', 'high', 'low', 'close'] # for sorting return value
    return data.resample(freq).apply(calculate_ohlc)[cols]
