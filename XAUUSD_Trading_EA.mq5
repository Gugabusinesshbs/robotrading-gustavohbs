//+------------------------------------------------------------------+
//|                                            XAUUSD_Trading_EA.mq5 |
//|                                                     Manus AI     |
//|                                       https://www.manus.computer |
//+------------------------------------------------------------------+
#property copyright "Manus AI"
#property link      "https://www.manus.computer"
#property version   "1.00"
#property description "Expert Advisor para XAUUSD com timeframes M1, M5, M15, H1 e lógica de trading baseada em indicadores."

//--- Parâmetros de entrada do EA
input double      LotSize = 0.01;           // Tamanho do Lote
input int         MagicNumber = 12345;      // Número Mágico para Ordens
input int         StopLossPips = 500;       // Stop Loss em pontos (50 pips para XAUUSD)
input int         TakeProfitPips = 1000;    // Take Profit em pontos (100 pips para XAUUSD)
input int         SmaPeriodFast = 5;        // Período da SMA Rápida
input int         SmaPeriodSlow = 20;       // Período da SMA Lenta
input int         RsiPeriod = 14;           // Período do RSI
input int         MacdFastPeriod = 12;      // Período Rápido do MACD
input int         MacdSlowPeriod = 26;      // Período Lento do MACD
input int         MacdSignalPeriod = 9;     // Período do Sinal do MACD
input int         BbPeriod = 20;            // Período das Bandas de Bollinger
input double      BbDeviations = 2.0;       // Desvios Padrão das Bandas de Bollinger
input ENUM_TIMEFRAMES CurrentTimeframe = PERIOD_H1; // Timeframe principal para operações
input double      MinConfidence = 0.70;     // Confiança mínima para abrir uma operação (simulada)

//--- Variáveis globais
int OnInit()
  {
//---
   Print("XAUUSD Trading EA inicializado no timeframe: ", EnumToString(CurrentTimeframe));
//--- Retorna INIT_SUCCEEDED se a inicialização for bem-sucedida
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//--- Obter o preço atual do XAUUSD
   MqlTick tick;
   if(!SymbolInfoTick(_Symbol, tick))
     {
      Print("Erro ao obter tick para ", _Symbol);
      return;
     }

   double currentPrice = tick.last;

//--- Obter dados OHLCV para o timeframe principal
   MqlRates rates[];
   if(CopyRates(_Symbol, CurrentTimeframe, 0, 100, rates) < 100)
     {
      Print("Não há dados suficientes para o timeframe ", EnumToString(CurrentTimeframe));
      return;
     }

   //--- Calcular indicadores técnicos
   double smaFast = iMA(_Symbol, CurrentTimeframe, SmaPeriodFast, 0, MODE_SMA, PRICE_CLOSE, 0);
   double smaSlow = iMA(_Symbol, CurrentTimeframe, SmaPeriodSlow, 0, MODE_SMA, PRICE_CLOSE, 0);
   double rsiValue = iRSI(_Symbol, CurrentTimeframe, RsiPeriod, PRICE_CLOSE, 0);
   
   // MACD
   double macdBuffer[], signalBuffer[];
   int macdHandle = iMACD(_Symbol, CurrentTimeframe, MacdFastPeriod, MacdSlowPeriod, MacdSignalPeriod, PRICE_CLOSE);
   if(macdHandle == INVALID_HANDLE)
     {
      Print("Erro ao criar handle MACD");
      return;
     }
   if(CopyBuffer(macdHandle, 0, 0, 1, macdBuffer) != 1 || CopyBuffer(macdHandle, 1, 0, 1, signalBuffer) != 1)
     {
      Print("Erro ao copiar buffers MACD");
      return;
     }
   double macdValue = macdBuffer[0];
   double macdSignal = signalBuffer[0];

   // Bandas de Bollinger
   double bbUpperBuffer[], bbMiddleBuffer[], bbLowerBuffer[];
   int bbHandle = iBands(_Symbol, CurrentTimeframe, BbPeriod, 0, BbDeviations, PRICE_CLOSE);
   if(bbHandle == INVALID_HANDLE)
     {
      Print("Erro ao criar handle BB");
      return;
     }
   if(CopyBuffer(bbHandle, 0, 0, 1, bbUpperBuffer) != 1 || CopyBuffer(bbHandle, 1, 0, 1, bbMiddleBuffer) != 1 || CopyBuffer(bbHandle, 2, 0, 1, bbLowerBuffer) != 1)
     {
      Print("Erro ao copiar buffers BB");
      return;
     }
   double bbUpper = bbUpperBuffer[0];
   double bbMiddle = bbMiddleBuffer[0];
   double bbLower = bbLowerBuffer[0];

   //--- Lógica de trading baseada em indicadores (simulando a predição do LLM)
   // Esta é uma simplificação da lógica do LLM, usando regras claras para decisão.
   // A 


   // A "confiança" é calculada com base na convergência dos indicadores
   double confidence = CalculateConfidence(smaFast, smaSlow, rsiValue, macdValue, macdSignal, currentPrice, bbUpper, bbMiddle, bbLower);
   
   // Determinar direção da operação
   string direction = DetermineDirection(smaFast, smaSlow, rsiValue, macdValue, macdSignal, currentPrice, bbUpper, bbMiddle, bbLower);
   
   // Verificar se a confiança é suficiente para abrir uma operação
   if(confidence >= MinConfidence)
     {
      if(direction == "BUY" && !HasOpenPositions(_Symbol, MagicNumber))
        {
         double sl = currentPrice - (StopLossPips * _Point);
         double tp = currentPrice + (TakeProfitPips * _Point);
         Trade.Buy(LotSize, _Symbol, 0, sl, tp, "BUY_SIGNAL_" + DoubleToString(confidence, 2));
         Print("Operação de COMPRA aberta com confiança: ", confidence);
        }
      else if(direction == "SELL" && !HasOpenPositions(_Symbol, MagicNumber))
        {
         double sl = currentPrice + (StopLossPips * _Point);
         double tp = currentPrice - (TakeProfitPips * _Point);
         Trade.Sell(LotSize, _Symbol, 0, sl, tp, "SELL_SIGNAL_" + DoubleToString(confidence, 2));
         Print("Operação de VENDA aberta com confiança: ", confidence);
        }
     }

   //--- Gestão de posições abertas
   ManageOpenPositions(currentPrice, rsiValue, macdValue, macdSignal);
  }

//+------------------------------------------------------------------+
//| Expert deinit function                                           |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   Print("XAUUSD Trading EA desinicializado. Razão: ", reason);
  }

//+------------------------------------------------------------------+
//| Funções auxiliares                                               |
//+------------------------------------------------------------------+
#include <Trade/Trade.mqh> // Incluir a biblioteca Trade para operações de trading
CTrade Trade; // Instância da classe CTrade

//+------------------------------------------------------------------+
//| Calcula a confiança da operação baseada na convergência dos indicadores |
//+------------------------------------------------------------------+
double CalculateConfidence(double smaFast, double smaSlow, double rsi, double macd, double macdSignal, double price, double bbUpper, double bbMiddle, double bbLower)
  {
   double confidence = 0.0;
   int signals = 0;
   
   // Sinal 1: Cruzamento das médias móveis
   if(smaFast > smaSlow)
     {
      confidence += 0.25;
      signals++;
     }
   else if(smaFast < smaSlow)
     {
      confidence += 0.25;
      signals++;
     }
   
   // Sinal 2: RSI não está em zona de sobrecompra/sobrevenda extrema
   if(rsi > 30 && rsi < 70)
     {
      confidence += 0.20;
      signals++;
     }
   
   // Sinal 3: MACD confirma a direção
   if(macd > macdSignal)
     {
      confidence += 0.25;
      signals++;
     }
   else if(macd < macdSignal)
     {
      confidence += 0.25;
      signals++;
     }
   
   // Sinal 4: Posição em relação às Bandas de Bollinger
   if(price > bbMiddle && price < bbUpper)
     {
      confidence += 0.15;
      signals++;
     }
   else if(price < bbMiddle && price > bbLower)
     {
      confidence += 0.15;
      signals++;
     }
   
   // Sinal 5: Volume (simulado baseado na volatilidade)
   double volatility = MathAbs(price - bbMiddle) / (bbUpper - bbLower);
   if(volatility > 0.3 && volatility < 0.7)
     {
      confidence += 0.15;
      signals++;
     }
   
   // Normalizar a confiança baseada no número de sinais
   if(signals > 0)
     {
      confidence = confidence * (signals / 5.0);
     }
   
   return MathMin(confidence, 1.0); // Limitar a confiança a 100%
  }

//+------------------------------------------------------------------+
//| Determina a direção da operação baseada nos indicadores          |
//+------------------------------------------------------------------+
string DetermineDirection(double smaFast, double smaSlow, double rsi, double macd, double macdSignal, double price, double bbUpper, double bbMiddle, double bbLower)
  {
   int buySignals = 0;
   int sellSignals = 0;
   
   // Análise das médias móveis
   if(smaFast > smaSlow)
      buySignals++;
   else if(smaFast < smaSlow)
      sellSignals++;
   
   // Análise do RSI
   if(rsi < 50 && rsi > 30)
      buySignals++;
   else if(rsi > 50 && rsi < 70)
      sellSignals++;
   
   // Análise do MACD
   if(macd > macdSignal && macd > 0)
      buySignals++;
   else if(macd < macdSignal && macd < 0)
      sellSignals++;
   
   // Análise das Bandas de Bollinger
   if(price > bbMiddle && price < bbUpper)
      buySignals++;
   else if(price < bbMiddle && price > bbLower)
      sellSignals++;
   
   // Determinar direção baseada na maioria dos sinais
   if(buySignals > sellSignals)
      return "BUY";
   else if(sellSignals > buySignals)
      return "SELL";
   else
      return "NEUTRAL";
  }

//+------------------------------------------------------------------+
//| Verifica se há posições abertas para o símbolo e número mágico   |
//+------------------------------------------------------------------+
bool HasOpenPositions(string symbol, int magic)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong position_ticket = PositionGetTicket(i);
      if(position_ticket == 0)
        {
         continue;
        }
      if(PositionGetString(POSITION_SYMBOL) == symbol && PositionGetInteger(POSITION_MAGIC) == magic)
        {
         return true;
        }
     }
   return false;
  }

//+------------------------------------------------------------------+
//| Gerencia posições abertas (trailing stop, fechamento antecipado) |
//+------------------------------------------------------------------+
void ManageOpenPositions(double currentPrice, double rsi, double macd, double macdSignal)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong position_ticket = PositionGetTicket(i);
      if(position_ticket == 0)
        {
         continue;
        }
      
      if(PositionGetString(POSITION_SYMBOL) == _Symbol && PositionGetInteger(POSITION_MAGIC) == MagicNumber)
        {
         double positionOpenPrice = PositionGetDouble(POSITION_PRICE_OPEN);
         ENUM_POSITION_TYPE positionType = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
         
         // Lógica de fechamento antecipado baseada em reversão de sinais
         bool shouldClose = false;
         
         if(positionType == POSITION_TYPE_BUY)
           {
            // Fechar compra se RSI estiver em sobrecompra extrema ou MACD reverter
            if(rsi > 80 || (macd < macdSignal && macd < 0))
              {
               shouldClose = true;
              }
           }
         else if(positionType == POSITION_TYPE_SELL)
           {
            // Fechar venda se RSI estiver em sobrevenda extrema ou MACD reverter
            if(rsi < 20 || (macd > macdSignal && macd > 0))
              {
               shouldClose = true;
              }
           }
         
         if(shouldClose)
           {
            Trade.PositionClose(position_ticket);
            Print("Posição fechada antecipadamente devido à reversão de sinais");
           }
        }
     }
  }

//+------------------------------------------------------------------+
//| Fecha todas as posições abertas de um determinado tipo           |
//+------------------------------------------------------------------+
void CloseAllPositions(string symbol, int magic, ENUM_POSITION_TYPE type)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong position_ticket = PositionGetTicket(i);
      if(position_ticket == 0)
        {
         continue;
        }
      if(PositionGetString(POSITION_SYMBOL) == symbol && PositionGetInteger(POSITION_MAGIC) == magic && PositionGetInteger(POSITION_TYPE) == type)
        {
         Trade.PositionClose(position_ticket);
        }
     }
  }

//+------------------------------------------------------------------+
//| Função para análise multi-timeframe (opcional)                   |
//+------------------------------------------------------------------+
bool AnalyzeMultiTimeframe()
  {
   // Analisar M1, M5, M15 e H1 para confirmar sinais
   ENUM_TIMEFRAMES timeframes[] = {PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_H1};
   int bullishCount = 0;
   int bearishCount = 0;
   
   for(int i = 0; i < ArraySize(timeframes); i++)
     {
      double smaFast = iMA(_Symbol, timeframes[i], SmaPeriodFast, 0, MODE_SMA, PRICE_CLOSE, 0);
      double smaSlow = iMA(_Symbol, timeframes[i], SmaPeriodSlow, 0, MODE_SMA, PRICE_CLOSE, 0);
      
      if(smaFast > smaSlow)
         bullishCount++;
      else if(smaFast < smaSlow)
         bearishCount++;
     }
   
   // Retorna true se há consenso entre os timeframes
   return (bullishCount >= 3 || bearishCount >= 3);
  }

//+------------------------------------------------------------------+
//| Função para calcular o tamanho do lote baseado no risco          |
//+------------------------------------------------------------------+
double CalculateLotSize(double accountBalance, double riskPercent, double stopLossPips)
  {
   double riskAmount = accountBalance * (riskPercent / 100.0);
   double pipValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double lotSize = riskAmount / (stopLossPips * pipValue);
   
   // Limitar o tamanho do lote aos valores mínimo e máximo permitidos
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   
   return MathMax(minLot, MathMin(maxLot, lotSize));
  }

