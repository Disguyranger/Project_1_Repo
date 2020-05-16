import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import pandas as pd
from scipy.stats import linregress
import requests, json, datetime, sys, os
import tkinter as tk
def dataFigure(date_time, value, date_time_seconds, time_frame, key):
    plt.clf()
    plt.cla()
    plt.xticks(rotation = 30)
    plt.grid()
    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
    plt.xlabel('Date')
    plt.ylabel('Price per Coin')
    plt.plot(date_time, value, color = 'black')
    plt.title(f"{key.capitalize()} price over {time_frame} days")
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
    
def process(coinIndex, days):
    if not days.isnumeric():
        print("Days needs to be a number!")
        return
    quick_keys = {1: 'bitcoin', 2: 'litecoin', 3: 'ethereum', 4: 'ripple'}
    time_frame = int(days)
    listOfDicts = None
    key = quick_keys[coinIndex]
    url = f'https://api.coingecko.com/api/v3/coins/{key}/market_chart?vs_currency=usd&days={time_frame}'
    date_time, value, date_time_seconds, data_frame = checkCoinPrice(url, key)
        
        
    if listOfDicts is None:
        listOfDicts = data_frame
    else:
        listOfDicts[key] = data_frame[key]
        
    dataFigure(date_time, value, date_time_seconds, time_frame, key)
    print(listOfDicts)

window = tk.Tk()
userOptions = tk.LabelFrame(window, text="Options")
userOptions.pack(fill="x", anchor="nw")

radioButtonFrame = tk.Frame(userOptions)
radioButtonFrame.pack(anchor="w")
coinVar = tk.IntVar()
bitcoin = tk.Radiobutton(radioButtonFrame, text="Bitcoin", variable=coinVar, value=1)
bitcoin.pack(anchor="w")
ethereum = tk.Radiobutton(radioButtonFrame, text="Ethereum", variable=coinVar, value=2)
ethereum.pack(anchor="w")
litecoin = tk.Radiobutton(radioButtonFrame, text="Litecoin", variable=coinVar, value=3)
litecoin.pack(anchor="w")
ripple = tk.Radiobutton(radioButtonFrame, text="Ripple", variable=coinVar, value=4)
ripple.pack(anchor="w")

daysFrame = tk.Frame(userOptions)
daysFrame.pack(anchor="w")
daysLabel = tk.Label(daysFrame, text="Number of Days: ")
daysLabel.pack(anchor="w", side="left")
days = tk.StringVar()
daysInput = tk.Entry(daysFrame, textvariable=days)
daysInput.pack(anchor="w", side="left")

processButton = tk.Button(userOptions, text="Process", command= lambda: process(coinVar.get(), days.get()))
processButton.pack(anchor="w")

plotFrame = tk.LabelFrame(window, text="Plot")
plotFrame.pack(fill="x", anchor="nw")

f = plt.figure(figsize=(12,6))

canvas = FigureCanvasTkAgg(f, plotFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

toolbar=NavigationToolbar2Tk(canvas, plotFrame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
window.mainloop()