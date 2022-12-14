# Introduction
Orb Crypto Bot is a trading robot for BTCUSDT written in python

# Package Content

bot.py     - entry point of this trading bot
pa.py      - price action class defition for strategy
config.py  - config file for "API_KEY" and "API_SECRET"

## Warning
This bot uses API keys to interact with your binance account. If you have no idea about APIs and coding in python, please do not attempt to use this bot.
Please do not share your private API keys to anyone. The author is not responsible for the misusage of this bot. This project is intended for educational purspose only. Use it to your own discreation. 

## About the Project
This trading bot uses the Open Range Breakout Strategy (ORB) in 15mins for BTCUSDT. This is implemented on binance spot only. This project is an implemention of my GOLD_ORB strategy for crypto currency. The ORB strategy utilizes the volatility of the market open and generate the trading signal from the range established during the first hours of the trading day. If breakout happens on the range then buy-long signal is generated by the bot, short-sell signal for breakdown otherwise. For this python implementaion only long position is available since it is configured as spot in binance.

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
> Again if you do not have any ideas about binance API keys and python programmingm please do not proceed. Misused of api keys could hacked your binance account. Proceed at your own risk

The trading bot will require for you to provide your binance "API_KEY" and "API_SECRET", this can be generated on your binance account under "API MANAGEMENT".
Once you've obtain this two code on your account, you can paste it on "config.py" file located at orb_cryptoBot/config.py.

If the API keys provided is correct, The bot will prompt "API Keys Validated" once the bot is started. If the provided API keys is incorrect the bot will prompt "Invalid API Keys!"


## Strategy

The strategy for this file is located on different python file as class (pa.py). This strategy  is a python implementation of previous project (GOLD_ORB).
This class contains a member function open_range_breakout. This function will read incoming tick data (price change) from the websocket. The function will generate the buy and sell signal. Thus this bot only uses price action to generate entry signals. The output is an integer type, it will output "11" for buy-long signal , "10" for sell-short signal and "0" if no signal was generated. This outputs will be pass to the bot.py which will send order to binance including the stoploss and takeprofit orders. 

