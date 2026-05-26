# GoodForwardPeScreener

A Python screener that scans S&P 500 stocks for favorable Forward PE to Trailing PE ratios using Yahoo Finance data.

## Features
- Fetches all S&P 500 tickers automatically
- Retrieves Trailing PE and Forward PE for each ticker from Yahoo Finance
- Configurable ratio threshold (default: 0.5) in `config.py`
- Filters out tickers with negative or invalid PE values
- Retries fetching data for tickers with missing PE values in multiple passes, until no further progress is made
- Logs all actions, errors, and exceptions for troubleshooting
- Outputs results to a CSV file: `good_forward_pe_results_YYYYMMDD_HHMMSS.csv`

## Usage

1. Install requirements:
   ```bash
   pip install yfinance pandas
   ```
2. Edit `config.py` to set your desired `targetRatio` (optional).
3. Run the screener from the command line:
   ```bash
   python main.py
   ```
4. The results will be saved as a CSV in the current directory.

## Output
- CSV columns: Ticker, TrailingPE, ForwardPE, actualRatio, MarkAsInteresting
  - `MarkAsInteresting` is "v" if the actualRatio is less than or equal to the targetRatio, otherwise blank.
- Log file: `good_forward_pe_screener.log` (contains actions and error details)

## Error Handling & Retry Logic
- All errors and exceptions are logged for easy troubleshooting.
- Tickers with negative or missing PE values are excluded from results.
- Tickers for which data could not be obtained are retried in multiple passes. The screener will continue retrying as long as some tickers succeed in each pass. Retries stop when no further progress is made or all tickers have been processed.
