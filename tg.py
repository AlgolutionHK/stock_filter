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
    # result_df = pd.read_csv('signal/Jan_2024/01_06_2024_signal.csv')

    buy_signal = result_df[result_df['BUY'] == True]
    buy_name = buy_signal['Stock']
    buy_list = '📈 Buy: '
    for item in buy_name:
        buy_list += '#' + item + ' '

    sell_signal = result_df[result_df['SELL'] == True]
    sell_name = sell_signal['Stock']
    sell_list = '📉 Sell: '
    for item in sell_name:
        sell_list += '#' + item + ' '

    message = prev_time.strftime("%Y%m%d (%a)") + \
""":

{}
{}

以上內容只供參考，並非投資意見，亦不構成任何投資產品之要約、要約招攬或建議。投資附帶風險，過往表現並不代表將來的表現。本資料只作為一般用途，它並沒有考慮您的個人需要、投資目標及特定財政狀況。

{}""".format(buy_list,sell_list,config.GOOGLE_SHEET_LINK)

    # print(message)
    await bot.send_message(chat_id=config.CHANNEL_ID, text=message)

asyncio.run(send_to_channel())