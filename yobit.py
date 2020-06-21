import json
import requests
import pandas as pd
import time
import pickle
from datetime import datetime



def yobit_req(method, pair_list=''):
    req = 'https://yobit.net/api/3/' + method + '/' + pair_list

    success = False
    while success == False:
        try:
            time.sleep(60/90) # to avoid overloading the api, which is limited to 100 requests / min
            response = requests.get(req).json()
            success = True
        except Exception as e:
            print('\nconnection error: ' + str(e))
            print('will try again soon..')
            time.sleep(10)

    return response

# returns pair min, max, fees
# I modified this from the Yobit definition
# to return a dataframe of all pairs and related feeds
def info(fetch_new=False):
    if fetch_new:
        response = yobit_req('info')
        df = pd.DataFrame()
        num_pairs = len(response['pairs'])

        print('getting info from Yobit')
        t0 = time.time()
        for [i, pair] in zip(range(num_pairs), response['pairs']):
            series = response['pairs'][pair]
            series.update({'pair': pair})
            df = df.append(series, ignore_index=True)

            pbar(start_time=t0, progress_pct=i/num_pairs)
        print('\nsaving to pickle')
        df.set_index('pair', inplace=True)
        pickle.dump(df, open('info.pkl', 'wb'))
    else:
        print('loading info from pickle')

        try:
            df = pickle.load(open('info.pkl', 'rb'))
        except FileNotFoundError:
            print('unable to find saved data, fetching new data')
            df = info(fetch_new=True) # recursive call to self
    return df

# returns open asks & bids
def depth(pair, limit=150):
    if limit > 2000:
        print('limit is too large, changing to max (2000)')
        limit = 2000
    request = pair + '?limit=' + str(limit)
    response = yobit_req('depth', request)[pair]
    return response

# statistical data for last 24 hrs
def ticker(pair):
    response = yobit_req('ticker', pair)[pair]
    return response

# recent completed trades, default 150, max 2000
def trades(pair, limit=150):
    if limit > 2000:
        print('limit is too large, changing to max (2000)')
        limit = 2000
    request = pair + '?limit=' + str(limit)
    response = yobit_req('trades', request)
    if len(response) != 0:
        response = response[pair]
        response = pd.DataFrame(response)

        # set index & update to a python-friendly version
        response.set_index('timestamp', inplace=True)
        response.index = [datetime.fromtimestamp(ts) for ts in response.index]

    else:
        response = pd.DataFrame(columns=['amount', 'price', 'tid', 'type'])


    return response

def init_master(fetch_new=False):
    if fetch_new:
        master = {}
        t0 = time.time()
        i = 0
        for pair in master.keys():
            i += 1
            pbar(start_time=t0, progress_pct=i/len(pairs))
            master[pair] = trades(pair, limit=2000)

        pickle.dump(master, open('master.pkl', 'wb'))
    else:
        print('loading master from pickle')

        try:
            master = pickle.load(open('master.pkl', 'rb'))
        except FileNotFoundError:
            print('unable to find saved data, fetching new data')
            master = init_master(fetch_new=True) # recursive call to self
    return master
