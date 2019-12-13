from flask import Flask
from flask import render_template
from flask import request, jsonify
import mysql.connector as mc

app = Flask(__name__)



@app.route('/')
def home():
    #get sysdate
    conn = get_connection()
    result = conn.cmd_query("select sysdate()")
    sysdate = conn.get_rows()
    conn.close()
    #get profit_and_loss data
    conn = get_connection()
    result = conn.cmd_query("select * from profit_and_loss")
    profit_and_loss = conn.get_rows()
    conn.close()
    #get blotter data - bitcoin
    conn = get_connection()
    blt = conn.cmd_query("select trade_count, concat(crypto_currency_symbol,' ',crypto_currency_name), side, price, trade_quantity, trade_timestamp from blotter left join profit_and_loss on crypto_currency_fk = p_n_l_pk where p_n_l_pk = 1 order by trade_count;")
    blt_list_btc = conn.get_rows()
    conn.close()
    #get blotter data - ethereum
    conn = get_connection()
    blt = conn.cmd_query("select trade_count, concat(crypto_currency_symbol,' ',crypto_currency_name), side, price, trade_quantity, trade_timestamp from blotter left join profit_and_loss on crypto_currency_fk = p_n_l_pk where p_n_l_pk = 2 order by trade_count;")
    blt_list_eth = conn.get_rows()
    conn.close()
    #get blotter data - litecoin
    conn = get_connection()
    blt = conn.cmd_query("select trade_count, concat(crypto_currency_symbol,' ',crypto_currency_name), side, price, trade_quantity, trade_timestamp from blotter left join profit_and_loss on crypto_currency_fk = p_n_l_pk where p_n_l_pk = 3 order by trade_count;")
    blt_list_ltc = conn.get_rows()
    conn.close()
    # cash
    cash = get_cash_amount()
    return render_template('index.html',  sdate = sysdate[0][0][0], pnl = profit_and_loss[0], blt_btc = blt_list_btc[0], blt_eth = blt_list_eth[0], blt_ltc = blt_list_ltc[0], cash=cash)
    



@app.route('/submitOrder', methods=['post'])
def get_sumbission():
    #get sysdate
    conn = get_connection()
    result = conn.cmd_query("select sysdate()")
    sysdate = conn.get_rows()
    conn.close()
    #get profit_and_loss data
    conn = get_connection()
    result = conn.cmd_query("select * from profit_and_loss")
    profit_and_loss = conn.get_rows()
    conn.close()
    #get users inputs
    orderQuantity = request.form['orderQuantity']
    orderSide = request.form['orderSide']
    cryptoOrdered = request.form['cryptoOrdered']
    #retrieve trade count before the next trade
    conn = get_connection()
    trade_count = conn.cmd_query("select count(*) from blotter")
    trade_ct = conn.get_rows()
    conn.close()
    print(trade_ct[0][0][0])
    #update database according to user input
    
    if str(orderSide) == 'Buy':
        orderPrice = 'ask_price'
        pnl_qty = float(orderQuantity)
    elif str(orderSide) == 'Sell':
        orderPrice = 'bid_price'
        pnl_qty = -float(orderQuantity)

    total_qty_before = get_total_qty_before(cryptoOrdered)
    total_qty_after = get_total_qty_after(pnl_qty, total_qty_before)
    latest_tran_bid_price = get_latest_tran_bid_price(cryptoOrdered)
    latest_tran_ask_price = get_latest_tran_ask_price(cryptoOrdered)
    #update pnl table - when buy
    if str(orderSide) == 'Buy':
        cash_before_trans = get_cash_amount()
        # check if transaction is valid
        if (pnl_qty*latest_tran_ask_price) <= cash_before_trans:
            #update profit and loss
            vwap = get_vwap(cryptoOrdered, latest_tran_ask_price, pnl_qty, total_qty_before, total_qty_after)
            msg = "update profit_and_loss set total_quantity = " + str(total_qty_after) + ", vwap = " + str(vwap) + " where p_n_l_pk = " + cryptoOrdered + ";"
            print(msg)
            update_cmd(msg)
            #update cash
            msg = "update cash set cash_amount = " + str(cash_before_trans - (pnl_qty*latest_tran_ask_price)) +";"
            update_cmd(msg)
            #update blotter table
            msg= "insert into blotter(crypto_currency_fk,side,trade_timestamp,trade_count,price,trade_quantity) values("+ cryptoOrdered +", '"+ str(orderSide) +"', (select sysdate()), "+ str(trade_ct[0][0][0]+1) + ", "+ str(latest_tran_ask_price)+", "+ orderQuantity +");"
            print(msg)
            update_cmd(msg)
    #update pnl table - when sell
    elif str(orderSide) == 'Sell':
        if float(orderQuantity) <= total_qty_before:
            current_bid_price = get_current_bid_price(cryptoOrdered)
            rpl = get_rpl(cryptoOrdered,pnl_qty, current_bid_price)
            msg = "update profit_and_loss set total_quantity = " + str(total_qty_after) + ", realized_pl = " + str(rpl) + " where p_n_l_pk = " + cryptoOrdered + ";"
            print(msg)
            update_cmd(msg)
            #update cash
            cash_before_trans = get_cash_amount()
            msg = "update cash set cash_amount = " + str(cash_before_trans - (pnl_qty*latest_tran_bid_price)) +";"
            update_cmd(msg)
            #update blotter table
            msg= "insert into blotter(crypto_currency_fk,side,trade_timestamp,trade_count,price,trade_quantity) values("+ cryptoOrdered +", '"+ str(orderSide) +"', (select sysdate()), "+ str(trade_ct[0][0][0]+1) + ", "+ str(latest_tran_bid_price)+", "+ orderQuantity +");"
            print(msg)
            update_cmd(msg)
    #get blotter data - bitcoin
    conn = get_connection()
    blt = conn.cmd_query("select trade_count, concat(crypto_currency_symbol,' ',crypto_currency_name), side, price, trade_quantity, trade_timestamp from blotter left join profit_and_loss on crypto_currency_fk = p_n_l_pk where p_n_l_pk = 1 order by trade_count;")
    blt_list_btc = conn.get_rows()
    conn.close()
    #get blotter data - ethereum
    conn = get_connection()
    blt = conn.cmd_query("select trade_count, concat(crypto_currency_symbol,' ',crypto_currency_name), side, price, trade_quantity, trade_timestamp from blotter left join profit_and_loss on crypto_currency_fk = p_n_l_pk where p_n_l_pk = 2 order by trade_count;")
    blt_list_eth = conn.get_rows()
    conn.close()
    #get blotter data - litecoin
    conn = get_connection()
    blt = conn.cmd_query("select trade_count, concat(crypto_currency_symbol,' ',crypto_currency_name), side, price, trade_quantity, trade_timestamp from blotter left join profit_and_loss on crypto_currency_fk = p_n_l_pk where p_n_l_pk = 3 order by trade_count;")
    blt_list_ltc = conn.get_rows()
    conn.close()
    # cash
    cash = get_cash_amount()
    return render_template('index.html',  sdate = sysdate[0][0][0], pnl = profit_and_loss[0], blt_btc = blt_list_btc[0], blt_eth = blt_list_eth[0], blt_ltc = blt_list_ltc[0],cash=cash)








def get_connection():
    conn = mc.connect(user='root',
                      passwd='Pword2019!1',
                      host = 'localhost',
                      database = 'test')
    return conn

def update_cmd(msg):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(msg)
    conn.commit()
    
    conn.close()

#pnl functions
def get_total_qty_before(crypto_pk):
    #retrieve total quantity before the new trade
    conn = get_connection()
    result = conn.cmd_query("select total_quantity from profit_and_loss where p_n_l_pk = "+str(crypto_pk)+";")
    total_qty = conn.get_rows()
    conn.close()
    
    return float(total_qty[0][0][0])

def get_total_qty_after(new_order_qty, total_qty_before):
    return float(total_qty_before) + float(new_order_qty)

def get_latest_tran_bid_price(crypto_pk):
    #retrieve price of the latest trade
    conn = get_connection()
    result = conn.cmd_query("select bid_price from profit_and_loss where p_n_l_pk = "+crypto_pk+";")
    price = conn.get_rows()
    conn.close()
    return float(price[0][0][0])
def get_latest_tran_ask_price(crypto_pk):
    #retrieve price of the latest trade
    conn = get_connection()
    result = conn.cmd_query("select ask_price from profit_and_loss where p_n_l_pk = "+crypto_pk+";")
    price = conn.get_rows()
    conn.close()
    return float(price[0][0][0])


def get_vwap(crypto_pk, buy_price_new, trade_qty_new, old_total_qty, new_total_qty):
    #retrieve vwap before the new trade
    conn = get_connection()
    result = conn.cmd_query("select vwap from profit_and_loss where p_n_l_pk = "+ str(crypto_pk) +";")
    vwap_old = conn.get_rows()
    conn.close()
    vwap_old = float(vwap_old[0][0][0])
    vwap = ((vwap_old * old_total_qty) + (buy_price_new * trade_qty_new))/ new_total_qty
    print("vwap: "+ str(((vwap_old * old_total_qty) + (buy_price_new * trade_qty_new))/ new_total_qty))
    return float(vwap)

def get_current_bid_price(crypto_pk):
    conn = get_connection()
    result = conn.cmd_query("select bid_price from profit_and_loss where p_n_l_pk = "+ str(crypto_pk) +";")
    current_bid_price = conn.get_rows()
    conn.close()
    current_bid_price = float(current_bid_price[0][0][0])
    return current_bid_price

def get_rpl(crypto_pk,sell_qty, current_bid_price):
    #retrieve vwap before the new trade
    conn = get_connection()
    result = conn.cmd_query("select vwap from profit_and_loss where p_n_l_pk = "+ str(crypto_pk) +";")
    vwap_old = conn.get_rows()
    conn.close()
    vwap_old = vwap_old[0][0][0]
    rpl = float(sell_qty) * (float(vwap_old)-float(current_bid_price))
    print("rpl = "+ str(rpl))
    return rpl 

def get_cash_amount():
    #retrieve vwap before the new trade
    conn = get_connection()
    result = conn.cmd_query("select cash_amount from cash where id = 1;")
    cash = conn.get_rows()
    conn.close()
    cash = float(cash[0][0][0])
    return cash 

# $env:FLASK_DEBUG=1
# export FLASK_DEBUG=1