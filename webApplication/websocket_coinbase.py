import asyncio
import websockets
import json
import mysql.connector as mc


def main():
    asyncio.get_event_loop().run_until_complete(start_coinbase_websocket())
async def start_coinbase_websocket():
    async with websockets.connect('wss://ws-feed.pro.coinbase.com') as websocket:
        await websocket.send(build_request())
        async for m in websocket:
            jsonstr = json.loads(m)
            if str(jsonstr).find("{'type': 'subscriptions'") == -1:
                print(jsonstr)
                p_crypto_ticker = jsonstr["product_id"]
                print(p_crypto_ticker)
                p_crypto_bid = jsonstr['best_bid']
                print(p_crypto_bid)
                p_crypto_ask = jsonstr['best_ask']
                print(p_crypto_ask)
                # update crypto_currency price 
                msg= "update profit_and_loss set ask_price = "+ str(p_crypto_ask)+", bid_price = "+ str(p_crypto_bid) + "  where crypto_currency_symbol = '"+ str(p_crypto_ticker)+"';"
                update_cmd(msg)
                # update upl and  current_market_price at the profit_and_loss table
                # update for BTC
                crypto = 1
                t_qty = get_total_qty(crypto)
                upl_BTC = get_upl(t_qty, crypto)
                msg= "update profit_and_loss set unrealized_pl = "+ str(upl_BTC)+"  where p_n_l_pk = "+str(crypto)+";"
                update_cmd(msg)
                # update for ETH
                crypto = 2
                t_qty = get_total_qty(crypto)
                upl_ETH = get_upl(t_qty, crypto)
                msg= "update profit_and_loss set unrealized_pl = "+ str(upl_ETH)+ "  where p_n_l_pk = "+str(crypto)+";"
                update_cmd(msg)
                # update for LTC
                crypto = 3
                t_qty = get_total_qty(crypto)
                upl_LTC = get_upl(t_qty, crypto)
                msg= "update profit_and_loss set unrealized_pl = "+ str(upl_LTC)+  "  where p_n_l_pk = "+str(crypto)+";"
                update_cmd(msg)

                
def get_total_qty(crypto_pk):
    #retrieve total quantity
    conn = get_connection()
    result = conn.cmd_query("select total_quantity from profit_and_loss where p_n_l_pk = " +str(crypto_pk)+ ";")
    total_qty = conn.get_rows()
    conn.close()
    
    return float(total_qty[0][0][0])

def get_current_bid_price(crypto_pk):
    conn = get_connection()
    result = conn.cmd_query("select bid_price from profit_and_loss where p_n_l_pk = "+ str(crypto_pk) +";")
    current_bid_price = conn.get_rows()
    conn.close()
    current_bid_price = current_bid_price[0][0][0]
    return float(current_bid_price)


def get_upl(total_qty, crypto):
    #retrieve vwap before the new trade
    conn = get_connection()
    result = conn.cmd_query("select vwap from profit_and_loss where p_n_l_pk = "+ str(crypto) +";")
    vwap_old = conn.get_rows()
    conn.close()
    vwap_old = vwap_old[0][0][0]
    current_mkt_price = get_current_bid_price(crypto)
    upl = float(total_qty) * (float(current_mkt_price)-float(vwap_old))
    return upl


def build_request():
    return "{\"type\": \"subscribe\",\"product_ids\": [\"ETH-USD\",\"BTC-USD\",\"LTC-USD\"],\"channels\": [\"ticker\",{\"name\": \"ticker\",\"product_ids\": [\"ETH-USD\"]}]}"
    #"{\"type\": \"subscribe\",\"product_ids\": [\"ETH-USD\",\"ETH-EUR\"],\"channels\": [\"level2\",\"heartbeat\",{\"name\": \"ticker\",\"product_ids\": [\"ETH-BTC\",\"ETH-USD\"]}]}"

def get_connection():
    conn = mc.connect(user='root',
                      passwd='Pword2019!1',
                      host = 'localhost',
                      database = 'test')
    return conn
def trim_string(word):
    '''assuming the string parameter is a string containing words inclosed with "" '''
    split_list = word.split('"')
    return split_list[1]

def update_cmd(msg):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(msg)
    conn.commit()
    
    conn.close()

if __name__ == "__main__":
    main()

