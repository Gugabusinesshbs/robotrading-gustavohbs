# 🌐 Guia de Conexão com Dados de Mercado em Tempo Real

Para que o seu sistema de trading automatizado opere com dados do mundo real, é necessário integrar o backend com uma fonte de dados de mercado em tempo real. Este guia explica como você pode fazer isso, focando no par XAUUSD.

## 1. Escolhendo uma Fonte de Dados em Tempo Real

Existem diversas APIs e provedores de dados de mercado que oferecem acesso a cotações em tempo real. Algumas opções populares incluem:

- **Corretoras (Brokers):** Muitas corretoras de Forex e criptomoedas oferecem APIs para acesso direto aos seus feeds de dados. Esta é a opção mais direta para trading ao vivo.
- **Provedores de Dados:** Empresas como Polygon.io, Finnhub, Alpha Vantage, ou até mesmo o próprio MetaTrader 5 (via `MetaTrader5` Python API) oferecem dados de mercado.
- **WebSockets:** Para dados de alta frequência, WebSockets são ideais, pois fornecem atualizações instantâneas de preços.

**Recomendação:** Para XAUUSD, a integração direta com a API da sua corretora ou o uso da biblioteca `MetaTrader5` para Python é a mais indicada, pois garante que os dados que você está analisando são os mesmos que a corretora está usando para execução de ordens.

## 2. Configurando a Conexão com Dados Reais (Exemplo com `MetaTrader5` Python API)

Vamos usar a biblioteca `MetaTrader5` para Python como exemplo, pois ela permite tanto a coleta de dados quanto a execução de ordens (o que será útil para o trading real).

### 2.1. Instalar a Biblioteca `MetaTrader5`

Certifique-se de que a biblioteca `MetaTrader5` esteja instalada no seu ambiente Python (o mesmo ambiente virtual do backend):

```bash
pip install MetaTrader5
```

### 2.2. Conectar ao MetaTrader 5

Você precisará ter o MetaTrader 5 instalado e rodando em sua máquina. O script Python se conectará a ele.

```python
import MetaTrader5 as mt5
from datetime import datetime

# Estabelecer conexão com o MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Exemplo: Obter o preço atual do XAUUSD
symbol = "XAUUSD"
last_tick = mt5.symbol_info_tick(symbol)
if last_tick:
    print(f"Preço atual do {symbol}: {last_tick.last}")
else:
    print(f"Não foi possível obter o tick para {symbol}")

# Desconectar do MetaTrader 5
mt5.shutdown()
```

### 2.3. Modificando o Backend (Flask) para Dados Reais

O seu backend Flask (`trading-backend/src/routes/trading.py`) atualmente simula dados. Você precisará modificar as funções que buscam dados para usar a API do MetaTrader 5.

**Passo 1: Atualizar `trading-backend/src/routes/trading.py`**

Você precisará criar uma função para buscar os dados OHLCV e o preço atual do XAUUSD usando `MetaTrader5`. Substitua a lógica de simulação pela chamada à API.

```python
# trading-backend/src/routes/trading.py

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import joblib
from flask import Blueprint, jsonify, request
from datetime import datetime
import time

trading_bp = Blueprint("trading", __name__)

# Carregar o modelo treinado
model = joblib.load("lightweight_trading_model.pkl")

# Variáveis de estado (para simulação, serão substituídas por dados reais)
is_trading_active = False
current_balance = 1000.0

# --- Funções para obter dados reais do MT5 ---
def get_mt5_data(symbol, timeframe, count):
    if not mt5.initialize():
        print("MT5 initialize() failed, error code =", mt5.last_error())
        return None
    
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    mt5.shutdown()
    
    if rates is None:
        return None
    
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df

def get_current_price(symbol):
    if not mt5.initialize():
        print("MT5 initialize() failed, error code =", mt5.last_error())
        return None
    
    tick = mt5.symbol_info_tick(symbol)
    mt5.shutdown()
    
    if tick:
        return tick.last
    return None

# --- Rotas da API --- (Exemplo de modificação)

@trading_bp.route("/status", methods=["GET"])
def get_status():
    global is_trading_active, current_balance
    
    # Obter preço atual do XAUUSD
    price = get_current_price("XAUUSD")
    if price is None:
        price = 0.0 # Valor padrão em caso de erro

    # ... (restante da lógica de status, como total_trades, win_rate, etc.)
    # Estes valores precisarão ser persistidos em um banco de dados ou arquivo para serem reais
    
    return jsonify({
        "is_active": is_trading_active,
        "current_price": price,
        "balance": current_balance,
        "total_trades": 0, # Substituir por valor real
        "win_rate": 0.0 # Substituir por valor real
    })

@trading_bp.route("/prediction", methods=["GET"])
def get_prediction():
    # Obter dados OHLCV para a predição
    df_ohlcv = get_mt5_data("XAUUSD", mt5.TIMEFRAME_M15, 100) # Exemplo: M15
    
    if df_ohlcv is None or df_ohlcv.empty:
        return jsonify({"direction": "NEUTRAL", "confidence": 0.5})

    # Preparar os dados para o modelo (mesma lógica do data_processor.py)
    # Isso é uma simplificação, você precisará replicar a lógica de feature engineering
    # do seu data_processor.py aqui para que o modelo receba os dados no formato correto.
    latest_data = df_ohlcv.iloc[-1] # Pega a última linha
    features = pd.DataFrame([[latest_data["open"], latest_data["high"], latest_data["low"], latest_data["close"], latest_data["tick_volume"]]], 
                             columns=["open", "high", "low", "close", "volume"])
    
    # Exemplo de cálculo de SMA simples para features
    features["SMA_5"] = df_ohlcv["close"].rolling(window=5).mean().iloc[-1]
    features["SMA_20"] = df_ohlcv["close"].rolling(window=20).mean().iloc[-1]
    
    # Fazer a predição
    prediction_proba = model.predict_proba(features)[0]
    direction = "ALTA" if prediction_proba[1] > prediction_proba[0] else "BAIXA"
    confidence = max(prediction_proba)

    return jsonify({"direction": direction, "confidence": confidence})

# ... (outras rotas como price-history, recent-trades, analytics, settings, logs)
# Elas também precisarão ser adaptadas para buscar dados reais ou persistidos.

@trading_bp.route("/toggle", methods=["POST"])
def toggle_trading():
    global is_trading_active
    is_trading_active = not is_trading_active
    
    if is_trading_active:
        # Iniciar o loop de trading em uma thread separada
        # (Isso é um exemplo, em produção você usaria um sistema de filas ou scheduler)
        print("Iniciando loop de trading...")
        # threading.Thread(target=run_trading_loop).start()
    else:
        print("Parando loop de trading...")
        
    return jsonify({"is_active": is_trading_active})

# --- Exemplo de loop de trading (executado quando is_trading_active é True) ---
def run_trading_loop():
    global is_trading_active, current_balance
    while is_trading_active:
        # 1. Obter dados mais recentes
        df_ohlcv = get_mt5_data("XAUUSD", mt5.TIMEFRAME_M1, 100) # Exemplo: M1
        if df_ohlcv is None or df_ohlcv.empty:
            time.sleep(5) # Espera antes de tentar novamente
            continue
        
        # 2. Preparar features e fazer predição
        latest_data = df_ohlcv.iloc[-1]
        features = pd.DataFrame([[latest_data["open"], latest_data["high"], latest_data["low"], latest_data["close"], latest_data["tick_volume"]]], 
                                 columns=["open", "high", "low", "close", "volume"])
        features["SMA_5"] = df_ohlcv["close"].rolling(window=5).mean().iloc[-1]
        features["SMA_20"] = df_ohlcv["close"].rolling(window=20).mean().iloc[-1]
        
        prediction_proba = model.predict_proba(features)[0]
        direction = "ALTA" if prediction_proba[1] > prediction_proba[0] else "BAIXA"
        confidence = max(prediction_proba)
        
        # 3. Lógica de execução de trade (simplificada)
        if confidence > 0.7: # Exemplo: confiança mínima de 70%
            # Aqui você integraria a lógica de execução de ordens do MT5
            # Ex: mt5.buy(), mt5.sell()
            print(f"Sinal de {direction} com confiança {confidence:.2f}")
            # Atualizar balance, registrar trade, etc.
            
        time.sleep(60) # Espera 1 minuto antes da próxima verificação
```

**Passo 2: Persistência de Dados**

Para ter um histórico real de trades, balanço e métricas, você precisará implementar um sistema de persistência de dados (ex: um banco de dados SQLite, PostgreSQL ou MongoDB) para armazenar os resultados das operações, o balanço da conta e os logs. O backend atual usa variáveis em memória que são resetadas a cada reinício.

## 3. Considerações Importantes para Trading Real

- **Conexão MT5:** O MetaTrader 5 precisa estar aberto e conectado à sua conta de trading (demo ou real) para que a API Python funcione.
- **Segurança:** Para trading real, a segurança é primordial. Nunca exponha suas credenciais de trading diretamente no código. Use variáveis de ambiente ou um sistema de gerenciamento de segredos.
- **Latência:** A velocidade da sua conexão com a corretora e a latência da API podem impactar a execução de trades.
- **Gestão de Erros:** Implemente um tratamento de erros robusto para lidar com falhas de conexão, erros de execução de ordens, etc.
- **Gerenciamento de Posições:** O sistema atual não gerencia posições abertas (Stop Loss, Take Profit, trailing stop) após a execução inicial. Para trading real, isso é crucial.
- **Backtesting e Otimização:** Antes de ir para uma conta real, realize backtests extensivos e otimize sua estratégia com dados reais da corretora para garantir a robustez.
- **Regulamentação:** Esteja ciente das regulamentações de trading em sua jurisdição.

## 4. Próximos Passos

1. **Obtenha uma conta demo** em uma corretora que suporte MetaTrader 5.
2. **Instale o MetaTrader 5** e conecte-se à sua conta demo.
3. **Modifique o `trading-backend/src/routes/trading.py`** para usar as funções `get_mt5_data` e `get_current_price`.
4. **Implemente a lógica de execução de ordens** usando `mt5.buy()`, `mt5.sell()`, `mt5.close()` dentro do `run_trading_loop`.
5. **Adicione persistência de dados** para balanço, trades e logs.
6. **Teste exaustivamente** em conta demo antes de considerar uma conta real.

---

**Desenvolvido por Manus AI**

*Este guia é um recurso educacional e não constitui aconselhamento financeiro. O trading envolve riscos.*

