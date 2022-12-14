#Author: Ulysses O. Andulte
#Created Date: November 2022

import websocket,json, pprint, talib, numpy
import config,pa
from binance.client import Client
from binance.enums import *
from pa import Price_Action
from datetime import datetime




#inputs
TRADE_SYMBOL = 'BTCUSDT'
POSITION_SIZE = 100
TRADE_QUANTITY = 0.018 
TAKE_PROFIT = 5 #in percent
STOP_LOSS = 2 #in percent


#Global Variables and objects
price_action = Price_Action()
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1h"
closes = []
in_position = False
client = Client(config.API_KEY, config.API_SECRET)

try:
    client.get_account()
    print('API keys validated')
except Exception as e:
    print('Invalid API keys!')    


#Class/function definition

#Open_position_order function on Binance
def open_position_order(symbol,quantity, side, order_type = ORDER_TYPE_MARKET):

    try:
        print("sending order")
        order = client.create_order(
        symbol=symbol,
        side=side,
        type=order_type,
        quantity=quantity)
   
        print(order)
        
    except Exception as e:
        print('open position order error')
        return False
    
    return True

#Set StopLoss and Takeprofit order function on Binance using OCO order
def close_position_order(symbol, quantity, side, StopLoss_price, TakeProfit_price):

    try:
        print("sending order")
        order =  client.create_oco_order(
        symbol=symbol,
        side=side,
        quantity = quantity,
        price = TakeProfit_price,
        stopPrice = StopLoss_price,
        stoPLimitPrice= StopLoss_price,
        stopLimitTimeinForce= TIME_IN_FORCE_GTC
        )

        print(order)
        
        client.futures_create_order()

    except Exception as e:
        print('sl and tp order error')
        return False
    
    return True


#Websocket Functions

#Established connection to Websocket
def on_open(ws):
    print('opened connection')

#Terminate Connection to Websocket
def on_close(ws):
    print ('closed connection')


#Listen to Websocket for Price Change, OnTick
def on_message(ws,message):
    global closes
    json_message = json.loads(message)
    
    

    #captures the OHLC of the streamed message
    candle = json_message['k']

    #captures "close" flag
    is_candle_closed = candle['x']

    #captures the closing price
    close = candle['c']    

    #print ticker price
    print('ticker price:',close)
    
    #print closing price
    if is_candle_closed: print('candle closed price:', close) 
    
    # check if the bot have a present position on a given coin
    position_flag = client.get_asset_balance(asset='BTC')['free']
    if position_flag == 0:
        in_position = False


    if is_candle_closed:

       

       # generate buy/sell signal 
       y = price_action.open_range_breakout(message)


       # Send order on binance long position 
       if y == 11 and in_position == False :
           order_succeded = open_position_order(TRADE_SYMBOL,TRADE_QUANTITY, SIDE_BUY)
           if order_succeded:
                in_position = True

                # send Stoploss and Take Profit orders thru OCO orders
                StopLoss = str(float(close)-(STOP_LOSS/100)*float(close))
                TakeProfit = str(float(close)+(TAKE_PROFIT/100)*float(close))
                close_position_order(TRADE_SYMBOL,TRADE_QUANTITY,SIDE_SELL,StopLoss, TakeProfit)


       """" FOR SHORT POSITION LOGIC - Disabled since bot is modified as SPOT Only
       # Send order on binance short position
       if y == 10 and in_position == False:
            order_succeded = open_position_order(TRADE_SYMBOL,TRADE_QUANTITY, SIDE_SELL)
            if order_succeded:
                in_position = True

                # send Stoploss and Take Profit orders thru OCO orders
                StopLoss = str(float(close)+(STOP_LOSS/100)*float(close))
                TakeProfit = str(float(close)-(TAKE_PROFIT/100)*float(close))
                close_position_order(TRADE_SYMBOL,TRADE_QUANTITY,SIDE_BUY,StopLoss, TakeProfit)
        """

ws = websocket.WebSocketApp(SOCKET,on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()




