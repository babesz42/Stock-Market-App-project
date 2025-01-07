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

class StockDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Stock Data')
        self.root.geometry('500x300')

        # Create the GUI elements
        self.prompt_label = tk.Label(self.root, text='Search symbol', font=("Arial", 14))
        self.prompt_label.pack()

        self.search_entry = tk.Entry(self.root, font=('Arial', 12), width=20)
        self.search_entry.pack(pady=3)

        self.time_label = tk.Label(self.root, text='Search time period', font=('Arial', 14))
        self.time_label.pack(pady=10)

        # Using a dropdown menu the select the timeframes
        self.selected_timeframe = tk.StringVar(root)
        self.selected_timeframe.set("ALL")
        self.dropdown_timeframe = tk.OptionMenu(root, self.selected_timeframe, "1Y", "3Y", "5Y", "ALL")
        self.dropdown_timeframe.pack(pady=4)

        self.table_button = tk.Button(self.root, text='Show table', command=self.Show)
        self.table_button.pack(pady=10)

        self.graph_button = tk.Button(self.root, text='Show graph', command=self.Show_graph)
        self.graph_button.pack(pady=10)

    def Get_data(self, API=''):
        # Get the data and handling wrong symbol inputs
        symbol = self.search_entry.get().strip()

        if not symbol:
            messagebox.showerror("Error", "Please enter a stock symbol")
            return None
        timeframe = self.selected_timeframe.get()
        try:
            ts = TimeSeries(key=API, output_format='pandas')
            symbol_data = ts.get_weekly_adjusted(symbol)[0]
            return symbol_data
        except KeyError:
            messagebox.showerror("Error", f"Invalid stock symbol: '{symbol}'. Check the stock market to find a real symbol.")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occured: {e}")
        # Filtering the data and error handling
        len_data = len(symbol_data)
        if timeframe == "ALL":
            filtered_data = symbol_data.copy()
        elif timeframe == "1Y" and len_data >= 52:
            filtered_data = symbol_data.head(52).copy()
        elif timeframe == "1Y" and len_data < 52:
            messagebox.showerror("Error", f"Stock does not have {timeframe[:1]} years of data")
            return None
        elif timeframe == "3Y" and len_data >= 156:
            filtered_data = symbol_data.head(156).copy()
        elif timeframe == "3Y" and len_data < 156:
            messagebox.showerror("Error", f"Stock does not have {timeframe[:1]} years of data")
            return None
        elif timeframe == "5Y" and len_data >= 260:
            filtered_data = symbol_data.head(260).copy()
        elif timeframe == "5Y" and len_data < 260:
            messagebox.showerror("Error", f"Stock does not have {timeframe[:1]} years of data")
            return None
        return filtered_data

    def Show(self):
        # Get the data
        filtered_data = self.Get_data()

        # Create the formatted table
        formatted_table = tabulate(filtered_data, headers='keys', tablefmt='pretty', showindex=True)

        # Create a new window to show the data
        show_window = tk.Toplevel(self.root)
        show_window.title("Data Table")
        show_window.geometry("1000x400")

        # Fill the window with the data and a slider
        slider = tk.Scale(root, resolution=2, orient="vertical")
        slider.pack
        text_widget = tk.Text(show_window, wrap="none", font=('Courier New', 10))
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)
        text_widget.insert("1.0", formatted_table)
        text_widget.config(state="disabled")

    def Show_graph(self):
        # Get the data
        filtered_data = self.Get_data()

        # Create and style the Matplotlib figure
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

        fig = plt.figure(figsize=(10, 5))
        plt.plot(filtered_data.index, filtered_data['5. adjusted close'], label='Adjusted Closing Price', color = 'lime', linewidth = 2.1)
        plt.xticks(rotation=45)
        plt.title("Stock Price Over Time")
        plt.xlabel('Date')
        plt.ylabel('Adjusted Closing Price')

        # Create a new window for the graph
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Stock Graph")
        graph_window.geometry("700x600")

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = StockDataApp(root)
    root.mainloop()
