import pandas as pd
import pymongo
from pymongo import MongoClient, UpdateOne
from pymongo.bulk import BulkUpsertOperation
from pymongo.database import Database
import pdwind
from loguru import logger

_client: MongoClient = None

def init(host='localhost', port=27017, **kwargs):
    global _client
    _client = MongoClient(host=host, port=port, **kwargs)

def _fill_wsd(code, fields, starttime, endtime):
    logger.info(f'pdwind.wsd {code} {fields} {starttime} -> {endtime}')
    db = _client['wind_wsd']
    df = pdwind.wsd(code, list(fields), starttime, endtime)[code]
    updates = [
        UpdateOne({
            'time': k
        }, {
            '$set': v.to_dict()
        }, upsert=True) for k, v in df.T.items()]
    db[code].bulk_write(updates)
    db[code].create_index('time')

def _complete_wsd(codes, fields, starttime, endtime):
    db = _client['wind_wsd']

    for c in codes:
        metaitem = db['__meta__'].find_one({
            'colname': c
        })
        if metaitem:
            cur_fields = metaitem.get('fields') or []
            data_starttime = pd.to_datetime(metaitem.get('starttime'))
            data_endtime = pd.to_datetime(metaitem.get('endtime'))
            missing_fields = list(set(fields) - set(metaitem['fields']))
        else:
            cur_fields = []
            data_starttime = None
            data_endtime = None
            missing_fields = list(fields)

        # 先下载缺失字段
        if missing_fields:
            if data_starttime and data_endtime:
                _fill_wsd(c, list(missing_fields), data_starttime, data_endtime)

            cur_fields = cur_fields + missing_fields
            db['__meta__'].update_one(
                {'colname': c},
                {
                    '$set': {
                        'fields': cur_fields,
                        'updatetime': pd.Timestamp.now()
                    }
                },
                upsert=True)

        # 补足前面缺失的日期
        if data_starttime is None or starttime.date() < data_starttime.date():
            if data_starttime:
                _fill_wsd(c, list(cur_fields), starttime, data_starttime)
                data_starttime = starttime
            elif data_endtime:
                _fill_wsd(c, list(cur_fields), starttime, data_endtime)
                data_starttime = starttime
            else:
                _fill_wsd(c, list(cur_fields), starttime, endtime)
                data_starttime = starttime
                data_endtime = endtime
            db['__meta__'].update_one(
                {'colname': c},
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
                _fill_wsd(c, list(cur_fields), data_endtime, endtime)
                data_endtime = endtime
            elif data_starttime:
                _fill_wsd(c, list(cur_fields), data_starttime, endtime)
                data_endtime = endtime
            db['__meta__'].update_one(
                {'colname': c},
                {
                    '$set': {
                        'endtime': data_endtime
                    }
                },
                upsert=True)

def wsd(codes, fields, starttime, endtime=None):
    if isinstance(codes, str):
        codes = codes.split(',')
    if isinstance(fields, str):
        fields = fields.split(',')
    starttime = pd.to_datetime(starttime)
    endtime = pd.Timestamp.today() if endtime is None else pd.to_datetime(endtime)

    _complete_wsd(codes, fields, starttime, endtime)

    db = _client['wind_wsd']

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
        cursor = db[c].find(filters, projection).sort([('time', pymongo.ASCENDING)])
        dfs[c] = pd.DataFrame(list(cursor)).set_index('time')
    return pd.concat([dfs[c] for c in codes], axis=1, keys=codes, names=['codes', 'fields'])


def _fill_wsi(code, starttime, endtime, barsize):
    colname = f'{code}_{barsize}'
    logger.info(f'pdwind.wsi {code} "open,high,low,close,volume,oi,amt" {starttime} -> {endtime}')
    db = _client['wind_wsi']
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
    db = _client['wind_wsi']

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

    db = _client['wind_wsi']

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
