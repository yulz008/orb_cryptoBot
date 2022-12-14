# Introduction
Orb Crypto Bot is a trading robot for BTCUSDT written in Python

## Package Content

 - bot.py     - entry point of this trading bot
 - pa.py      - price action class definition for the strategy
 - config.py  - config file for "API_KEY" and "API_SECRET"

## Warning
This bot uses API keys to interact with your binance account. If you have no idea about APIs and coding in python, please do not attempt to use this bot.
Please do not share your private API keys to anyone. The author is not responsible for the misusage of this bot. This project is intended for educational purpose only. Use at your own discretion.

## About the Project
This trading bot uses the Open Range Breakout Strategy (ORB) in 15mins for BTCUSDT. This is implemented on binance spot only. This project is an implementation of my GOLD_ORB strategy for crypto currency. See link below for details:

https://github.com/yulz008/GOLD_ORB

The ORB strategy utilizes the volatility of the market open and generates the buy/sell signal from the range established during the first hours of the trading day. If breakout happens on the range then buy-long signal is generated by the bot, short-sell signal for breakdown otherwise. For this python implementation only long position is available since it is configured as spot in binance.

## Requirement

install python 3.10.0 (or newer version) 

additional packages:
```
$ pip install python-binance
$ pip install websockets
$ pip install numpy
```

## API Keys

> **Warning**
> Again, if you do not have any ideas about binance API keys and Python programming please do not proceed. Misused of API keys could hack your binance account. Proceed at your own risk

The trading bot will require for you to provide your binance "API_KEY" and "API_SECRET", this can be generated on your binance account under "API MANAGEMENT".
Once you've obtained this two code on your account, you can paste it on "config.py" file located at orb_cryptoBot/config.py.

If the API keys provided is correct, the bot will prompt "API Keys Validated" once the bot is started. If the provided API keys is incorrect the bot will prompt "Invalid API Keys!"


## Strategy

The strategy for this file is located on different python file as a class definition (pa.py). This strategy  is a python implementation of my previous project (GOLD_ORB). This class contains a member function "open_range_breakout". This function will read incoming tick data (price change) from the websocket. Then analyzes it to generate the buy and sell signal. Thus, this bot only uses price action alone to generate entry signals. The output is an integer type, it will output "11" for buy-long signal , "10" for sell-short signal and "0" if no signal was generated. These outputs will be pass to "bot.py" which will send buy/sell order to binance including the stoploss and take profit orders. 

### Strategy Logic

//execute only at the closing price of each candle
1. 15 minutes after market open, get initial range low and high of the candle. (Initial support and resistance)
2. at succeeding candles update range high and low, else do nothing.
3. on final range, generate buy/sell signal at breakout/breakdown.
4. repeat

### Overall Bot Logic

//After program is compiled and now running
1. Read inputs
2. Check if API keys are valid, prompt error message if invalid
3. Open websocket connection, prompt to terminal
4. On each message of the websocket:
     - check for current position of BTC
     - print ticker price
     - If ticker price is a closing price:
          - print closing price
          - call open_range_breakout to generate buy/sell signal
          - if buy/sell signal, and no current position of BTC:
             - Send order to binance to open a position
             - Send order for SL and TP

## Inputs

The inputs for this bot can be configured on the bot.py source file.

 - TRADE_SYMBOL   
    - the desired symbol to trade, input is in str
 - TRADE_QUANTITY 
    - the size/volume of your trade, please compute this carefully it varies from symbol to symbol, input is in decimal
 - TAKE_PROFIT    
    - the percentage move on price before taking profit, input is in decimal (e.g if 10% desired move, input 10)
 - STOP_LOSS      
    - the percentage move on price before exiting the position with a loss, input in decimal (e.g if -2% desired move, input 2)


## How to use and install the bot

1. download/pull the repository to your local folder.
2. from the command line, change the directory to your local folder
3. run the program:  \**directory\ python bot.py 
4. If the bot successfully loaded it will output ticker prices from the command line.
5. The bot is now running and interacting with binance.
![image](https://user-images.githubusercontent.com/117939069/207553604-256ae5f3-452d-4d81-8ef0-e18f594d92fc.png)

## Reference

Special thanks to @PartTimeLarry for great tutorials on creating trading bot on python-binance. 
Please check his github and youtube channel!

https://github.com/hackingthemarkets/binance-tutorials

## Disclaimer

This code is just meant to be used for learning. In no way do I promise profitable trading outcomes. Do not risk money that you can't afford to lose because the authors and any affiliates assume no responsibility for your trading results. This strategy DO NOT come with ANY warranty, thus there may be flaws in the code. Investments are risky by nature! Future outcomes cannot be predicted based on past performance!              

