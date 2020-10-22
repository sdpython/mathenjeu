# -*- coding: utf-8 -*-
"""
@file
@brief Helpers to process data from logs.
"""
import re
from datetime import datetime
import hashlib
import numpy
import pandas
import ujson


def _duration(seq):
    dt = None
    t1 = None
    for t, e in seq:
        if e == 'enter':
            t1 = t
        elif e == 'leave':
            if t1 is None:
                # raise RuntimeError("Wrong logging {0}".format(seq))
                return datetime(2018, 1, 2) - datetime(2018, 1, 1)
            if dt is None:
                dt = t - t1
            else:
                dt += t - t1
            t1 = None
    return dt


def _enumerate_processed_row(rows, data, cache, last_key):
    """
    Converts time, data as dictionary into other data
    as dictionary.

    @param      rows        previous rows
    @param      data        data as dictionaries
    @param      cache       cache events
    @param      last_key    last seen key
    @return                 iterator on clean rows
    """
    def comma_semi(st):
        if st is None:
            return {}
        res = {}
        for val in st.split(','):
            spl = val.split(':')
            if len(spl) == 1:
                res[spl[0]] = True
            elif len(spl) == 2:
                res[spl[0]] = spl[1]
            else:
                raise ValueError(  # pragma: no cover
                    "Unable to parse value '{0}'".format(st))
        return res

    def hash4alias(st):
        by = st.encode("utf-8")
        m = hashlib.sha256()
        m.update(by)
        res = m.hexdigest()
        return res[:20] if len(res) > 20 else res

    session = data.get('session', None)
    ipadd = data.get('client', ['NN.NN.NN.NN'])[0]
    if ipadd is None:
        raise ValueError(  # pragma: no cover
            "Unable to extract an ip address from {0}".format(data))
    keys = {'qn', 'game', 'next', 'events'}
    if session is not None:
        alias = session['alias']
        person_id = hash4alias(alias + ipadd)

        res = dict(person_id=person_id, alias=alias, time=data['time'])
        event = data.get('msg', None)
        if event == 'qcm':
            res['qtime'] = 'begin'
            key = person_id, alias, data['game'], data['qn']
            if key not in cache:
                cache[key] = []
            cache[key].append((data['time'], 'enter'))
            if len(last_key) > 0:
                cache[last_key[0]].append((data['time'], 'leave'))
                last_key.clear()
            last_key.append(key)
            yield res

            events = data.get('events', None)
            res0 = res.copy()
            res0['qtime'] = 'event'
            if events is not None:
                if not isinstance(events, list):
                    events = [events]
                res = res0.copy()
                for event in events:
                    ev = comma_semi(event)
                    res.update(ev)
                    yield res

        elif event == "answer":
            res["qtime"] = 'end'
            q = data.get('data', None)
            if q is not None:
                qn = q['qn']
                game = q['game']
                q2 = {}
                for k, v in q.items():
                    if k in keys:
                        q2[k] = v
                    else:
                        q2["{0}-{1}-{2}".format(game, qn, k)] = v
                res.update(q2)
            key = person_id, alias, q['game'], q['qn']
            if key not in cache:
                cache[key] = []
            cache[key].append((data['time'], 'leave'))
            duration = _duration(cache[key])
            res["{0}-{1}-{2}".format(game, qn, 'nbvisit')
                ] = len(cache[key]) * 0.5
            res["{0}-{1}-{2}".format(game, qn, 'duration')] = duration
            last_key.clear()
            yield res

            events = data.get('events', None)
            res0 = res.copy()
            res0['qtime'] = 'event'
            if events is not None:
                if not isinstance(events, list):
                    events = [events]
                res = res0.copy()
                for event in events:
                    ev = comma_semi(event)
                    res.update(ev)
                    yield res


def enumerate_qcmlog(files):
    """
    Processes many files of logs produced by application
    @see cl QCMApp.

    @param      files       list of filenames
    @return                 iterator on observations as dictionary

    Example of data it processes::

        2018-12-12 17:56:42,833,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:2"]}
        2018-12-12 17:56:44,270,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:2"]}
        2018-12-12 17:56:44,349,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:2"]}
        2018-12-12 17:56:44,458,INFO,[DATA],{"msg":"qcm","session":{"alias":"xavierd"},"game":"simple_french_qcm","qn":"3"}
        2018-12-12 17:56:49,427,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:3"]}
        2018-12-12 17:56:50,817,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:3"]}
        2018-12-12 17:56:50,864,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:3"]}
        2018-12-12 17:56:53,302,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:3"]}
        2018-12-12 17:56:53,333,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:3"]}
        2018-12-12 17:56:54,208,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:3"]}
        2018-12-12 17:56:54,239,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"events":["game:simple_french_qcm,qn:3"]}
    """
    rows = []
    cache = {}
    last_key = []
    for name in files:
        if len(rows) > 1000:
            rows = rows[-1000:]
        with open(name, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "[DATA]" not in line:
                    continue
                line = line.strip("\n\r")
                spl = line.split(",INFO,[DATA],")
                ti = spl[0]
                sdata = ",INFO,[DATA],".join(spl[1:])
                try:
                    data = ujson.loads(sdata)  # pylint: disable=E1101
                except ValueError:
                    if '"' not in sdata and "'" in sdata:
                        sdata2 = sdata.replace("'", '"')
                        try:
                            data = ujson.loads(sdata2)  # pylint: disable=E1101
                        except ValueError:
                            if '"msg": "finish"' in sdata2:
                                # Fix the code somewhere else.
                                sdata3 = sdata2.replace(
                                    '"client": ("', '"client": ["')
                                sdata3 = sdata3.replace(
                                    '), "data": QueryParams', '], "data": QueryParams')
                                sdata3 = re.sub(
                                    'QueryParams\\(\\"game=([a-z_]+)\\"\\)', '{"game":"\\1"}', sdata3)
                                try:
                                    data = ujson.loads(  # pylint: disable=E1101
                                        sdata3)
                                except ValueError as e:
                                    raise ValueError(
                                        "Unable to process line\n{}\n{}\n{}".format(
                                            sdata, sdata2, sdata3)) from e
                            else:
                                raise ValueError(
                                    "Unable to process line\n{}\n{}".format(
                                        sdata, sdata2)) from e

                tid = datetime.strptime(ti, '%Y-%m-%d %H:%M:%S,%f')
                data['time'] = tid
                obss = _enumerate_processed_row(rows, data, cache, last_key)
                for obs in obss:
                    yield obs
                rows.append(data)


def _aggnotnan_serie(values):
    res = []
    for v in values:
        if isinstance(v, float) and numpy.isnan(v):
            continue
        if pandas.isnull(v):
            continue
        if v in ('ok', 'on'):
            v = 1
        elif v == 'skip':
            v = 1000
        res.append(v)
    if len(res) > 0:
        if isinstance(res[0], str):
            r = ",".join(str(_) for _ in res)
        else:
            if len(res) == 1:
                r = res[0]
            else:
                try:
                    r = sum(res)
                except TypeError:
                    r = 0
    else:
        r = numpy.nan
    return r


def _aggnotnan(values):
    if isinstance(values, pandas.core.series.Series):
        r = _aggnotnan_serie(values)
        return r
    else:
        res = []
        for col in values.columns:
            val = list(values[col])
            res.append(_aggnotnan_serie(val))
        df = pandas.DataFrame(res, values.columns)
        return df


def enumerate_qcmlogdf(files):
    """
    Processes many files of logs produced by application
    @see cl QCMApp in dataframe.

    @param      files       list of filenames
    @return                 iterator on observations as dictionary

    Example of data it processes::

        2018-12-12 17:56:42,833,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]", events":["game:sfq,qn:2"]}
        2018-12-12 17:56:44,270,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","events":["game:sfq,qn:2"]}
        2018-12-12 17:56:44,349,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","events":["game:sfq,qn:2"]}
        2018-12-12 17:56:44,458,INFO,[DATA],{"msg":"qcm","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","game":"sfq","qn":"3"}
        2018-12-12 17:56:49,427,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","events":["game:sfq,qn:3"]}
        2018-12-12 17:56:50,817,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","events":["game:sfq,qn:3"]}
        2018-12-12 17:56:50,864,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","events":["game:sfq,qn:3"]}
        2018-12-12 17:56:53,302,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","events":["game:sfq,qn:3"]}
        2018-12-12 17:56:53,333,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","events":["game:sfq,qn:3"]}
        2018-12-12 17:56:54,208,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","events":["game:sfq,qn:3"]}
        2018-12-12 17:56:54,239,INFO,[DATA],{"msg":"event","session":{"alias":"xavierd"},"client":["N.N.N.N",N]","events":["game:sfq,qn:3"]}
    """
    def select_name(col):
        return "-" in col

    def prepare_df(rows):
        df = pandas.DataFrame(rows)
        df2 = df[df.qtime == 'end']
        cols = ['person_id']
        cols2 = [c for c in df2.columns if select_name(c)]
        cols2.sort()
        df_question = df2[cols + cols2]
        gr_ans = df_question.groupby("person_id").agg(_aggnotnan)
        return gr_ans

    stack = {}
    index = {}
    for i, row in enumerate(enumerate_qcmlog(files)):

        person_id = row.get('person_id', None)
        if person_id is None:
            continue

        index[person_id] = i
        if person_id not in stack:
            stack[person_id] = []
        stack[person_id].append(row)

        rem = []
        for k, ind in index.items():
            if i - ind > 500:
                rem.append(k)
        for k in rem:
            yield prepare_df(stack[k])
            del stack[k]
            del index[k]
    for k, rows in stack.items():
        yield prepare_df(rows)
