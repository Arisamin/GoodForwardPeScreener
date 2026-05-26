import yfinance as yf
import pandas as pd
import logging
from datetime import datetime
from config import targetRatio

# Setup logging
logging.basicConfig(
    filename='good_forward_pe_screener.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def fetch_sp500_tickers():
    """Fetch S&P 500 tickers from Wikipedia."""
    import requests
    from io import StringIO
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        print("Connecting to Wikipedia for S&P 500 tickers...")
        response = requests.get(url, headers=headers)
        tables = pd.read_html(StringIO(response.text))
        sp500_table = tables[0]
        tickers = sp500_table['Symbol'].tolist()
        print(f"Connected successfully to Wikipedia. Got {len(tickers)} tickers.")
        logging.info(f"Fetched {len(tickers)} S&P 500 tickers from Wikipedia.")
        return tickers
    except Exception as e:
        print(f"Failed to connect to Wikipedia: {e}")
        logging.error(f"Failed to fetch S&P 500 tickers from Wikipedia: {e}")
        # Fallback to a small sample if Wikipedia fails
        fallback = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'JPM', 'V']
        print(f"Using fallback list of {len(fallback)} stocks.")
        logging.info(f"Using fallback list of {len(fallback)} stocks.")
        return fallback

def fetch_pe_ratios(ticker):
    """Fetch Trailing PE and Forward PE for a ticker from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        trailing_pe = info.get('trailingPE', None)
        forward_pe = info.get('forwardPE', None)
        logging.info(f"{ticker}: TrailingPE={trailing_pe}, ForwardPE={forward_pe}")
        return trailing_pe, forward_pe
    except Exception as e:
        logging.error(f"{ticker}: Error fetching PE ratios: {e}")
        return None, None

def main():
    print("Screener started.")
    tickers = fetch_sp500_tickers()
    if len(tickers) == 0:
        print("Failed to fetch tickers from Wikipedia and fallback list is empty.")
        return
    else:
        print(f"Loaded {len(tickers)} tickers.")
    results = []
    total = len(tickers)
    for idx, ticker in enumerate(tickers, 1):
        trailing_pe, forward_pe = fetch_pe_ratios(ticker)
        if trailing_pe is None or forward_pe is None:
            print(f"[{idx}/{total}] {ticker}: Missing PE data, skipping.")
            continue
        try:
            actual_ratio = forward_pe / trailing_pe
        except Exception as e:
            logging.error(f"{ticker}: Error calculating ratio: {e}")
            print(f"[{idx}/{total}] {ticker}: Error calculating ratio: {e}")
            continue
        # Exclude negative or zero values
        if trailing_pe <= 0 or forward_pe <= 0 or actual_ratio < 0:
            print(f"[{idx}/{total}] {ticker}: Negative/zero PE or ratio, skipping.")
            continue
        if actual_ratio >= targetRatio:
            results.append({
                'Ticker': ticker,
                'TrailingPE': trailing_pe,
                'ForwardPE': forward_pe,
                'actualRatio': actual_ratio
            })
        if idx % 20 == 0 or idx == total:
            print(f"Processed {idx}/{total} tickers...")
    # Save results to CSV
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'good_forward_pe_results_{now}.csv'
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"Saved {len(results)} results to {output_file}.")
    logging.info(f"Saved {len(results)} results to {output_file}.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Exception caught in main: {e}")
        logging.exception(f"Fatal error in main: {e}")
