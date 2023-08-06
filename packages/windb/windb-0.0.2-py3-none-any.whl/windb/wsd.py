import pandas as pd
from pymongo import UpdateOne, ASCENDING
import pdwind
from loguru import logger

from . import dbconn

def _fill_wsd(db, codes, fields, starttime, endtime, options=None):
    logger.info(f'update {fields} {starttime} -> {endtime}')

    dfs = pdwind.wsd(codes, fields, starttime, endtime, options=options)
    dfs = dfs[dfs.index >= pd.to_datetime(starttime.date())]

    for c, _ in dfs:
        updates = [
            UpdateOne({
                'time': k
            }, {
                '$set': v.to_dict()
            }, upsert=True) for k, v in dfs[c].T.items()]
        db[c].bulk_write(updates)
        db[c].create_index('time')

def _complete_wsd(db, codes, fields, starttime, endtime, options=None):
    info = db['__meta__'].find_one({
        'key': 'info'
    })
    if info:
        cur_starttime = info['starttime']
        cur_endtime = info['endtime']
    else:
        cur_starttime = None
        cur_endtime = None

    cur_codes = db.collection_names()
    cur_codes.remove('__meta__')

    codes_diff = set(codes) - set(cur_codes)

    # 补缺失的数据大类
    if codes_diff:
        _fill_wsd(db, list(codes_diff), fields, cur_starttime, cur_endtime, options=options)

    new_codes = list(set(codes).union(set(cur_codes)))

    # 补足前面缺失的日期
    if cur_starttime is None or starttime.date() < cur_starttime.date():
        if cur_starttime:
            _fill_wsd(db, new_codes, fields, starttime, cur_starttime, options=options)
            cur_starttime = starttime
        elif cur_endtime:
            _fill_wsd(db, new_codes, fields, starttime, cur_endtime, options=options)
            cur_starttime = starttime
        else:
            _fill_wsd(db, new_codes, fields, starttime, endtime, options=options)
            cur_starttime = starttime
            cur_endtime = endtime
        db['__meta__'].update_one(
            {'key': 'info'},
            {
                '$set': {
                    'starttime': cur_starttime,
                    'endtime': cur_endtime
                }
            },
            upsert=True)

    # 补足后面缺失的日期
    if cur_endtime is None or endtime.date() > cur_endtime.date():
        if cur_endtime:
            _fill_wsd(db, new_codes, fields, cur_endtime, endtime, options=options)
            cur_endtime = endtime
        elif cur_starttime:
            _fill_wsd(db, new_codes, fields, cur_starttime, endtime, options=options)
            cur_endtime = endtime
        db['__meta__'].update_one(
            {'key': 'info'},
            {
                '$set': {
                    'starttime': cur_starttime,
                    'endtime': cur_endtime
                }
            },
            upsert=True)

def _wsd_worker(db, codes, fields, full_fields, starttime, endtime=None, options=None):
    if isinstance(codes, str):
        codes = codes.split(',')
    if isinstance(fields, str):
        fields = fields.split(',')
    starttime = pd.to_datetime(starttime)
    endtime = pd.Timestamp.today() if endtime is None else pd.to_datetime(endtime)

    _complete_wsd(db, codes, full_fields, starttime, endtime, options=options)
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
        cursor = db[c].find(filters, projection).sort([('time', ASCENDING)])
        dfs[c] = pd.DataFrame(list(cursor)).set_index('time')
    return pd.concat([dfs[c] for c in codes], axis=1, keys=codes, names=['codes', 'fields'])

def _update_daily_worker(db, fields, force_last):

    info = db['__meta__'].find_one({
        'key': 'info'
    })
    if not info:
        return

    cur_starttime = info['starttime']
    cur_endtime = info['endtime']

    cur_codes = db.collection_names()
    cur_codes.remove('__meta__')

    now = pd.Timestamp.now()

    if cur_endtime.date() < now.date() or force_last:
        _fill_wsd(db, cur_codes, fields, cur_endtime, now)
        db['__meta__'].update_one(
            {'key': 'info'},
            {
                '$set': {
                    'starttime': cur_starttime,
                    'endtime': now
                }
            },
            upsert=True)

def wsd_update(force_last=False):
    _update_daily_worker(dbconn.db('wind_wsd'), 'open,high,low,close,volume,oi,amt', force_last)
    _update_daily_worker(dbconn.db('wind_edb'), 'close', force_last)

def wsd_contract(codes, fields, starttime, endtime=None):
    return _wsd_worker(dbconn.db('wind_wsd'), codes, fields, 'open,high,low,close,volume,oi,amt', starttime, endtime)

def wsd_edb(codes, starttime, endtime=None):
    return _wsd_worker(dbconn.db('wind_edb'), codes, 'close', 'close', starttime, endtime, options='Days=Weekdays').swaplevel(axis=1)['close']
