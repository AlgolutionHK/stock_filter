import yfinance as yf
import pandas as pd
from datetime import timedelta, datetime
import concurrent.futures
from time import sleep

stock_list = pd.read_csv("stock_name.csv")

def get_earnings_df(tickers):
    # Create an empty DataFrame
    earnings_df = pd.DataFrame()
    
    # Get the current date
    current_date = datetime.now().date()
    
    # Calculate the end date (1 week from the current date)
    start_date = current_date - timedelta(days=7)
    end_date = current_date + timedelta(days=7)
    
    # Define a helper function to process each ticker
    def process_ticker(ticker):
        try:
            # Get the list of tickers in the index
            stock = yf.Ticker(ticker)
            
            # Get the earnings dates for the ticker
            earnings_dates = stock.earnings_dates
            sleep(1)
            
            # Loop through each earnings date
            for earnings_date in earnings_dates.index:
                # Check if the earnings date is within the week
                if start_date <= earnings_date.date() <= end_date:
                    # Add the earnings date to the DataFrame
                    earnings_df.loc[earnings_date.date(), 'ticker'] = stock.ticker
            print(ticker, "added!")
        except:
            print(ticker, "not available!")
    
    # Create a ThreadPoolExecutor with a maximum of 10 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        # Submit each ticker to the executor
        futures = [executor.submit(process_ticker, ticker) for ticker in tickers]
        
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
    
    return earnings_df

earnings_df = get_earnings_df(stock_list['Stock']).sort_index()

earnings_df.to_csv("earnings_df.csv")