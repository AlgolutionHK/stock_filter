import telegram
import config
import asyncio
from datetime import datetime, timedelta
import pandas as pd

async def send_to_channel():
    bot = telegram.Bot(token=config.API_KEY)

    time = datetime.now()
    prev_time = time - timedelta(days=1)

    result_df = pd.read_csv('signal/' + time.strftime("%b_%Y") + '/' + time.strftime("%m_%d_%Y") + '_signal.csv')
    # result_df = pd.read_csv('signal/Jan_2024/01_19_2024_signal.csv')
    signal_df = pd.read_csv('stock_name.csv')
    stock_name = signal_df['Stock']

    buy_list = '📈 Buy: '
    try:
        buy_signal = result_df[result_df['BUY'] == True]
        buy_name = buy_signal['Stock']
        for item in buy_name:
            if item in stock_name.values:
                print(item)
                buy_list += '#' + item + ' '
    except:
        pass
    

    sell_list = '📉 Sell: '
    try:
        sell_signal = result_df[result_df['SELL'] == True]
        sell_name = sell_signal['Stock']
        for item in sell_name:
            if item in stock_name.values:
                sell_list += '#' + item + ' '

    except:
        pass
    
    close_buy_list = '❌ Close Buy: '
    try:
        close_buy_signal = result_df[result_df['CLOSE BUY'] == True]
        close_buy_name = close_buy_signal['Stock']
        for item in close_buy_name:
            if item in stock_name.values:
                close_buy_list += '#' + item + ' '

    except:
        pass
    
    close_sell_list = '❌ Close Sell: '
    try:
        close_sell_signal = result_df[result_df['CLOSE SELL'] == True]
        close_sell_name = close_sell_signal['Stock']
        for item in close_sell_name:
            if item in stock_name.values:
                close_sell_list += '#' + item + ' '

    except:
        pass
    
    message = time.strftime("%Y%m%d (%a)") + \
""":

{}
{}
{}
{}

以上內容只供參考，並非投資意見，亦不構成任何投資產品之要約、要約招攬或建議。投資附帶風險，過往表現並不代表將來的表現。本資料只作為一般用途，它並沒有考慮您的個人需要、投資目標及特定財政狀況。

{}""".format(buy_list,sell_list,close_buy_list,close_sell_list,config.GOOGLE_SHEET_LINK)

    # print(message)
    await bot.send_message(chat_id=config.CHANNEL_ID, text=message)

# asyncio.run(send_to_channel())