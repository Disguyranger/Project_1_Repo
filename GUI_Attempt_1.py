import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
import requests, json, datetime, sys, os

def dataFigure(date_time, value, date_time_seconds, time_frame, key):
    plt.figure(figsize=(9,6))
    plt.xticks(rotation = 30)
    plt.grid()
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.plot(date_time, value, color = 'black')
    plt.title(f"{key.capitalize()} price over {time_frame} days")
    plt.xlabel('Date')
    plt.ylabel('Price per Coin')
    regression = []
    (slope, intercept, rvalue, pvalue, stderr) = linregress(date_time_seconds, value)
    
    regress_values = []
    for i in date_time_seconds:
        regress_values.append(i * slope + intercept)
    plt.plot(date_time, regress_values,'-.', color = 'Blue')
    try:
        os.remove(f'{key.capitalize()}.png')
        print('Output File already exists. Deleting...') 
        print(f'Creating new file for {key.capitalize()} as png')
        plt.savefig(f'{key.capitalize()}.png')
    except OSError:
        print(f'Creating save file for {key.capitalize()} as png')
        plt.savefig(f'{key.capitalize()}.png')
        pass
    
def jawaherDF(date_time, value):
    stock_market = pd.read_csv('stockmarket.csv')
    stock_market['Date'] = pd.to_datetime(stock_market['Date'])
    crypto_df = pd.DataFrame ( { "date" : date_time, "price" : value })
    merged_df = pd.merge(crypto_df, stock_market, how= 'right', left_on= 'date' , right_on = 'Date' ).dropna()
    merged_df [['Date', 'price', 'Open']].plot(x= "Date").legend(['DoW Jones', ])


def checkCoinPrice(url, key):
    response = requests.get(url)
    data_construct = response.json()
    if data_construct == {"error":"Could not find coin with the given id"} or data_construct == {'error': 'invalid vs_currency'}:
        print("There was an issue with variables. Check work and try again.")
    date_time = []
    value = []
    date_time_seconds = []    
    for row in data_construct['prices']:
        date_time.append(datetime.datetime.utcfromtimestamp(int(row[0]/1000)))
        value.append(row[1])
        date_time_seconds.append(int((row[0]/1000)))
        
        
    date = []
    time = []
    for convertline in date_time:
        split = str(convertline).split(' ')
        date.append(split[0])
        time.append(split[1])
    data_frame = pd.DataFrame(date, time)
    data_frame = data_frame.reset_index().rename(columns= {'index': 'Time', 0: 'Date'})
    data_frame[key] = value
 
    return(date_time, value, date_time_seconds, data_frame)
    
def main():
    quick_keys = {1: 'bitcoin', 2: 'litecoin', 3: 'ethereum', 4: 'ripple'}
    time_frame = int(input("How far back would you like to look back? "))
    listOfDicts = None
    for coin_type in range(4):
        key = quick_keys[coin_type + 1]
        url = f'https://api.coingecko.com/api/v3/coins/{key}/market_chart?vs_currency=usd&days={time_frame}'
        date_time, value, date_time_seconds, data_frame = checkCoinPrice(url, key)
        
        
        if listOfDicts is None:
            listOfDicts = data_frame
        else:
            listOfDicts[key] = data_frame[key]
        
        dataFigure(date_time, value, date_time_seconds, time_frame, key)
    print(listOfDicts)
        
    jawaherDF(date_time, value)
    
    
    

main()