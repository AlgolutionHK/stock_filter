import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, timedelta, time
import json

def upload_signal():
    # Load Excel file into a Pandas dataframe
    time = datetime.now()
    prev_time = time - timedelta(days=1)
    path = time.strftime("%b_%Y") 
    # print(os.listdir())
    df = pd.read_excel(path + ".xlsx")
    # df = pd.read_excel('Aug_2023.xlsx')
    df = df.fillna('')

    gc = gspread.service_account('key.json')

    #connect to your sheet (between "" = the name of your G Sheet, keep it short)
    sh = gc.open(path).sheet1
    sh.format("A1:Z999",{
    "backgroundColor": {
    "red": 1.0,
    "green": 1.0,
    "blue": 1.0
    }})

    #write values in cells a3 and b3
    data = df.values.tolist()
    header = df.columns.values.tolist()
    data.insert(0, header)
    sh.update(data)

    #Highlight new signals
    signal_list = sh.findall(prev_time.strftime("%d/%m"))
    for cell in signal_list:
        des_cell = cell.address
        sh.format(des_cell, {
        "backgroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 0.0
        }})

        row = cell.row
        sh.format("A" + str(row) + ":F" + str(row), {
        "backgroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 0.0
        }})

    sh.set_basic_filter()


def upload_history():
    # Load Excel file into a Pandas dataframe
    df = pd.read_excel("history.xlsx")
    df = df.fillna('')

    gc = gspread.service_account('key.json')
    
    sh = gc.open("History").sheet1

    # Update values
    data = df.values.tolist()
    data = [[str(value.strftime('%Y/%m')) if isinstance(value, datetime) or isinstance(value, time) else value for value in sublist] for sublist in data]
    header = df.columns.values.tolist()
    data.insert(0, header)
    data = [row[:8] for row in data]

    sh.update(data,raw=False)


def upload_signal_public():
    # Load Excel file into a Pandas dataframe
    time = datetime.now()
    prev_time = time - timedelta(days=1)
    path = time.strftime("%b_%Y") + "_signal"
    # print(os.listdir())
    df = pd.read_excel(path + ".xlsx")
    # df = pd.read_excel('Aug_2023.xlsx')
    df = df.fillna('')
    gc = gspread.service_account('key.json')

    #connect to your sheet (between "" = the name of your G Sheet, keep it short)
    sh = gc.open(path).sheet1
    sh.format("A1:Z999",{
    "backgroundColor": {
    "red": 1.0,
    "green": 1.0,
    "blue": 1.0
    }})

    #write values in cells a3 and b3
    data = df.values.tolist()
    header = df.columns.values.tolist()
    data.insert(0, header)
    sh.update(data)

    #Highlight new signals
    signal_list = sh.findall(prev_time.strftime("%d/%m"))
    for cell in signal_list:
        des_cell = cell.address
        sh.format(des_cell, {
        "backgroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 0.0
        }})

        row = cell.row
        sh.format("A" + str(row) + ":F" + str(row), {
        "backgroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 0.0
        }})




# upload_signal()
upload_history()
# upload_signal_public()