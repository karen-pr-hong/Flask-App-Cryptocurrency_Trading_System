import pandas as pd
import numpy as np
import requests

url = "https://api.binance.com//api/v1/ticker/24hr"

def splitPair(tickerString):
    #if tickerString[:2]=='BTC' or tickerString[:2]=='ETH' or tickerString[:2]=='LTC':
    if tickerString[-4:]=='USDT':
        return [tickerString.split('USDT')[0].lower(),'usdt']
    return np.nan

bnn_df =pd.DataFrame(requests.get(url).json())
bnn_df['symbol']=bnn_df.apply(lambda x: splitPair(x['symbol']), axis = 1)
bnn_df = bnn_df.dropna()
bnn_df['base']=bnn_df.apply(lambda x: x['symbol'][0], axis = 1)
bnn_df['quote']=bnn_df.apply(lambda x: x['symbol'][1], axis = 1)
print(bnn_df)