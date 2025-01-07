from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import requests
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import tkinter as tk
from tkinter import messagebox, ttk
import csv
from tabulate import tabulate
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image

def Show_test():
    # Get the data
    symbol = search_entry.get()
    timeframe = int(time_entry.get())
    test_data = pd.read_csv(symbol)
    filtered_data = test_data.tail(timeframe)

    # Format the table with the tabulate library
    formatted_table = tabulate(filtered_data, headers='keys', tablefmt='pretty', showindex=False)

    # Create a new window
    show_window = tk.Toplevel(root)
    show_window.title("Data table")
    show_window.geometry("745x400")
    text_widget = tk.Text(show_window, wrap="none", font=('Courier New', 10))
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
    text_widget.insert("1.0", formatted_table)
    text_widget.config(state="disabled")

def Show_graph_test():
    # Get the data
    symbol = search_entry.get()
    timeframe = int(time_entry.get())
    test_data = pd.read_csv(symbol)
    filtered_data = test_data.tail(timeframe).copy()

    # Ensure 'Date' is in datetime format and set as index
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
    filtered_data.set_index('Date', inplace=True)

    # Create the tkinter window
    graph_window = tk.Toplevel(root)
    graph_window.title(f"{symbol} chart - last {timeframe} rows")
    graph_window.geometry("700x600")
        
    # Create plot style and plotting
    dark_style = {
        "axes.facecolor": "#222222",
        "axes.edgecolor": "white",
        "axes.labelcolor": "white",
        "figure.facecolor": "#222222",
        "grid.color": "gray",
        "text.color": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "xtick.major.size": 7,
        "ytick.major.size": 7,
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.linewidth": 0.5}
    plt.style.use(dark_style)
    fig = plt.figure(figsize=(10, 5))  # Create a Matplotlib Figure
    plt.xlabel('Date')
    plt.ylabel('Closing price')
    plt.plot(filtered_data.index, filtered_data['Close'], label='Closing Price')
    plt.legend()
        
    # Embed the plot into the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def MACD():
    symbol = search_entry.get()
    timeframe = int(time_entry.get())
    test_data = pd.read_csv(symbol)
    filtered_data = test_data.tail(timeframe)


    macddf = filtered_data.ta.macd(fast=8, slow=21, signal=9, min_periods=None, append=True)
    print(type(macddf))




root = tk.Tk()
root.title('Show Data')
root.geometry('500x300')
prompt_label = tk.Label(root, text='Search symbol', font = ("Arial", 14))
prompt_label.pack()
search_entry = tk.Entry(root, font=('Arial', 12), width=20)
search_entry.pack(pady=3)
time_label = tk.Label(root, text='Search time period', font=('Arial', 14))
time_label.pack(pady=10)
time_entry = tk.Entry(root, font=('Arial', 12), width=15)
time_entry.pack(pady=3)
table_button = tk.Button(root, text='Show table', command=Show_test)
table_button.pack(pady=10)
graph_button = tk.Button(root, text='Show graph', command=Show_graph_test)
graph_button.pack(pady=10)
MACD_button = tk.Button(root, text="MACD", command=MACD)
MACD_button.pack(pady=10)
root.mainloop()

