import datetime
import pandas as pd
from WindPy import w

w.start()

__all__ = ['wsd', 'wss']

def wsd(codes, fields, first_date, last_date, options=None):
    if isinstance(codes, str):
        codes = codes.split(',')
    if isinstance(fields, str):
        fields = fields.split(',')

    dfs = {}

    for field in fields:
        ret = w.wsd(codes, field, first_date, last_date, options)
        index = pd.to_datetime(ret.Times)

        if len(ret.Times) > 1:
            data = dict(zip(codes, ret.Data))
            dfs[field] = pd.DataFrame(data, index=index)
        else:
            data = dict(zip(codes, ret.Data[0]))
            dfs[field] = pd.DataFrame(data, index=index)

    result = pd.concat([dfs[f] for f in fields], axis=1, keys=fields, names=['fields', 'codes']).swaplevel(axis=1)
    result.index.name = 'date'
    return result

def wsi(codes, fields, start_time, stop_time, options=None):
    if isinstance(codes, str):
        codes = codes.split(',')
    if isinstance(fields, str):
        fields = fields.split(',')

    dfs = {}

    for code in codes:
        ret = w.wsi(code, fields, start_time, stop_time, options)
        index = pd.to_datetime(ret.Times)

        if len(ret.Times) > 1:
            data = dict(zip(fields, ret.Data))
            dfs[code] = pd.DataFrame(data, index=index)
        else:
            data = dict(zip(fields, ret.Data[0]))
            dfs[code] = pd.DataFrame(data, index=index)

    result = pd.concat([dfs[c] for c in codes], axis=1, keys=codes, names=['codes', 'fields'])
    result.index.name = 'time'
    return result

def wst(codes, fields, start_time, stop_time, options=None):
    if isinstance(codes, str):
        codes = codes.split(',')
    if isinstance(fields, str):
        fields = fields.split(',')

    dfs = {}

    for code in codes:
        ret = w.wst(code, fields, start_time, stop_time, options)
        index = pd.to_datetime(ret.Times)

        if len(ret.Times) > 1:
            data = dict(zip(fields, ret.Data))
            dfs[code] = pd.DataFrame(data, index=index)
        else:
            data = dict(zip(fields, ret.Data[0]))
            dfs[code] = pd.DataFrame(data, index=index)

    result = pd.concat([dfs[c] for c in codes], axis=1, keys=codes, names=['codes', 'fields'])
    result.index.name = 'time'
    return result

def wss(codes, fields, date=None):
    if isinstance(codes, str):
        codes = codes.split(',')
    if isinstance(fields, str):
        fields = fields.split(',')
    if isinstance(date, datetime.date):
        date = date.strftime('%Y%m%d')
    ret = w.wss(codes, fields, f"tradeDate={date};priceAdj=U;cycle=D" if date is not None else None)

    data = {fields[i]: ret.Data[i] for i in range(len(fields))}
    return pd.DataFrame(data, index=codes)

def wset_futurecc(startdate, enddate, wind_code, fields=None):
    """fields: sec_name,code,wind_code,delivery_month,change_limit,target_margin,contract_issue_date,last_trade_date,last_delivery_month
    """
    if fields and not isinstance(fields, str):
        fields = ','.join(fields)

    if fields:
        ret = w.wset('futurecc', f'startdate={startdate};enddate={enddate};wind_code={wind_code};field={fields}')
    else:
        ret = w.wset('futurecc', f'startdate={startdate};enddate={enddate};wind_code={wind_code}')

    data = {ret.Fields[i]: ret.Data[i] for i in range(len(ret.Fields))}
    return pd.DataFrame(data)

def wset_futureoir(startdate, enddate, varity, wind_code, order_by):
    if wind_code:
        ret = w.wset('futureoir', f'startdate={startdate};enddate={enddate};varity={varity};wind_code={wind_code};order_by={order_by};ranks=all')
    else:
        ret = w.wset('futureoir', f'startdate={startdate};enddate={enddate};varity={varity};order_by={order_by};ranks=all')
    data = {ret.Fields[i]: ret.Data[i] for i in range(len(ret.Fields))}
    df = pd.DataFrame(data)
    time, date_per_day = zip(*df.groupby('date'))
    date_per_day = [df.set_index('ranks') for df in date_per_day]
    return pd.concat(date_per_day, axis=1, keys=time, names=['time', 'fields'])

def wset_futurevir(startdate, enddate, varity, wind_code, order_by):
    if wind_code:
        ret = w.wset('futurevir', f'startdate={startdate};enddate={enddate};varity={varity};wind_code={wind_code};order_by={order_by};ranks=all')
    else:
        ret = w.wset('futurevir', f'startdate={startdate};enddate={enddate};varity={varity};ranks=all')
    data = {ret.Fields[i]: ret.Data[i] for i in range(len(ret.Fields))}
    df = pd.DataFrame(data)
    time, date_per_day = zip(*df.groupby('date'))
    date_per_day = [df.set_index('ranks') for df in date_per_day]
    return pd.concat(date_per_day, axis=1, keys=time, names=['time', 'fields'])

def tdays(first_day, last_day, options=None):
    ret = w.tdays(first_day, last_day, options)
    return pd.to_datetime(ret.Data[0])

def tdayscount(first_day, last_day, options=None):
    ret = w.tdayscount(first_day, last_day, options)
    return ret.Data[0][0]

def tdaysoffset(offset, tday, options=None):
    ret = w.tdaysoffset(offset, tday, options)
    return pd.to_datetime(ret.Data[0][0])
