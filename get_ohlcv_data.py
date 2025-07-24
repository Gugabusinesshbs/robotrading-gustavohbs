
import ccxt
import pandas as pd
import datetime

exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1m'
since = exchange.parse8601('2024-07-16T00:00:00Z') # 1 ano de histórico a partir de hoje

all_ohlcv = []

while True:
    print(f'Fetching OHLCV for {symbol} from {exchange.iso8601(since)}')
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
    if len(ohlcv) == 0:
        break
    all_ohlcv.extend(ohlcv)
    since = ohlcv[-1][0] + 60 * 1000 # Move to the next minute

df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)
df.to_csv('BTC_USDT_1m.csv')
print('Data collection complete and saved to BTC_USDT_1m.csv')


