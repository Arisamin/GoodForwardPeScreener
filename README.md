# GoodForwardPeScreener

A Python screener that scans S&P 500 stocks for favorable Forward PE to Trailing PE ratios using Yahoo Finance data.

## Features
- Fetches all S&P 500 tickers automatically
- Retrieves Trailing PE and Forward PE for each ticker from Yahoo Finance
- Configurable ratio threshold (default: 0.5) in `config.py`
- Filters out tickers with negative or invalid PE values
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
- CSV columns: Ticker, TrailingPE, ForwardPE, actualRatio
- Log file: `good_forward_pe_screener.log` (contains actions and error details)

## Error Handling
- All errors and exceptions are logged for easy troubleshooting.
- Tickers with negative or missing PE values are excluded from results.
