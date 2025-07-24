
import yfinance as yf
import pandas as pd
import datetime

symbol = 'BTC-USD' # Símbolo para Bitcoin em USD no Yahoo Finance

timeframe = '1m' # Tentando 1 minuto
start_date = datetime.datetime.now() - datetime.timedelta(days=7) # 7 dias de histórico para 1m
end_date = datetime.datetime.now()

print(f"Downloading {symbol} data from {start_date} to {end_date} with interval {timeframe}")
data = yf.download(symbol, start=start_date, end=end_date, interval=timeframe)

if not data.empty:
    print("Columns before processing:", data.columns)
    # Flatten MultiIndex columns if they exist
    if isinstance(data.columns, pd.MultiIndex):
        # For yfinance, the first level is the OHLCV type, and the second is the ticker.
        # We want to keep only the OHLCV type and convert to lowercase.
        data.columns = [col[0].lower() for col in data.columns]

    data = data[['open', 'high', 'low', 'close', 'volume']]
    data.to_csv('BTC_USD_1m.csv')
    print('Data collection complete and saved to BTC_USD_1m.csv')
else:
    print('Failed to download data or data is empty.')


