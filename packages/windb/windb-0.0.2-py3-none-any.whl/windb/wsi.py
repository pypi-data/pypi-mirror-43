import pandas as pd
import pymongo
from pymongo import UpdateOne
import pdwind
from loguru import logger

from . import dbconn

def _fill_wsi(code, starttime, endtime, barsize):
    colname = f'{code}_{barsize}'
    logger.info(f'pdwind.wsi {code} "open,high,low,close,volume,oi,amt" {starttime} -> {endtime}')
    db = dbconn.db('wind_wsi')
    df = pdwind.wsi(code, "open,high,low,close,volume,oi,amt", starttime, endtime, f'BarSize={barsize}')[code]
    df = df.dropna(how='all')
    updates = [
        UpdateOne({
            'time': k
        }, {
            '$set': v.to_dict()
        }, upsert=True) for k, v in df.T.items()]
    db[colname].bulk_write(updates)
    db[colname].create_index('time')

def _complete_wsi(codes, starttime, endtime, barsize):
    db = dbconn.db('wind_wsi')

    for c in codes:
        colname = f'{c}_{barsize}'
        metaitem = db['__meta__'].find_one({
            'colname': colname
        })
        if metaitem:
            data_starttime = pd.to_datetime(metaitem.get('starttime'))
            data_endtime = pd.to_datetime(metaitem.get('endtime'))
        else:
            data_starttime = None
            data_endtime = None

        # 补足前面缺失的日期
        if data_starttime is None or starttime.date() < data_starttime.date():
            if data_starttime:
                _fill_wsi(c, starttime, data_starttime, barsize)
                data_starttime = starttime
            elif data_endtime:
                _fill_wsi(c, starttime, data_endtime, barsize)
                data_starttime = starttime
            else:
                _fill_wsi(c, starttime, endtime, barsize)
                data_starttime = starttime
                data_endtime = endtime
            db['__meta__'].update_one(
                {'colname': colname},
                {
                    '$set': {
                        'starttime': data_starttime,
                        'endtime': data_endtime
                    }
                },
                upsert=True)

        # 补足后面缺失的日期
        if data_endtime is None or endtime.date() > data_endtime.date():
            if data_endtime:
                _fill_wsi(c, data_endtime, endtime, barsize)
                data_endtime = endtime
            elif data_starttime:
                _fill_wsi(c, data_starttime, endtime, barsize)
                data_endtime = endtime
            db['__meta__'].update_one(
                {'colname': colname},
                {
                    '$set': {
                        'endtime': data_endtime
                    }
                },
                upsert=True)

def wsi(codes, fields, starttime, endtime, barsize):
    if isinstance(codes, str):
        codes = codes.split(',')
    if isinstance(fields, str):
        fields = fields.split(',')
    starttime = pd.to_datetime(pd.to_datetime(starttime).date())
    endtime = pd.to_datetime(pd.to_datetime(endtime).date()) + pd.Timedelta(days=1)

    _complete_wsi(codes, starttime, endtime, barsize)

    db = dbconn.db('wind_wsi')

    filters = {
        'time': {
            '$gte': starttime,
            '$lte': endtime
        }
    }
    projection = {f:1 for f in fields}
    projection['time'] = 1
    projection['_id'] = 0

    dfs = {}
    for c in codes:
        cursor = db[f'{c}_{barsize}'].find(filters, projection).sort([('time', pymongo.ASCENDING)])
        dfs[c] = pd.DataFrame(list(cursor)).set_index('time')
    return pd.concat([dfs[c] for c in codes], axis=1, keys=codes, names=['codes', 'fields'])
