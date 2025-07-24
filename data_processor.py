import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime
import json

class DataProcessor:
    def __init__(self, data_dir="/home/ubuntu/data/btc_data"):
        self.data_dir = data_dir
        self.processed_data = None
        
    def load_all_csv_files(self):
        """Carrega todos os arquivos CSV do diretório de dados"""
        csv_files = glob.glob(os.path.join(self.data_dir, "*.csv"))
        print(f"Encontrados {len(csv_files)} arquivos CSV")
        
        all_data = []
        for file in sorted(csv_files):
            try:
                df = pd.read_csv(file)
                all_data.append(df)
                print(f"Carregado: {os.path.basename(file)} - {len(df)} registros")
            except Exception as e:
                print(f"Erro ao carregar {file}: {e}")
        
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            print(f"Total de registros combinados: {len(combined_data)}")
            return combined_data
        else:
            print("Nenhum dado foi carregado")
            return None
    
    def clean_and_structure_data(self, df):
        """Limpa e estrutura os dados OHLCV"""
        if df is None:
            return None
            
        # Verificar se as colunas existem
        available_columns = df.columns.tolist()
        print(f"Colunas disponíveis: {available_columns}")
        
        # Selecionar apenas as colunas OHLCV necessárias
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df_clean = df[required_columns].copy()
        
        # Converter timestamp para datetime com formato flexível
        try:
            df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], format='mixed')
        except:
            try:
                df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'])
            except:
                print("Erro ao converter timestamp, tentando formato ISO8601")
                df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], format='ISO8601')
        
        # Remover duplicatas
        df_clean = df_clean.drop_duplicates(subset=['timestamp'])
        
        # Ordenar por timestamp
        df_clean = df_clean.sort_values('timestamp')
        
        # Remover valores nulos
        df_clean = df_clean.dropna()
        
        # Converter colunas numéricas
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Remover linhas com valores inválidos após conversão
        df_clean = df_clean.dropna()
        
        print(f"Dados limpos: {len(df_clean)} registros")
        return df_clean
    
    def add_technical_indicators(self, df):
        """Adiciona indicadores técnicos aos dados"""
        if df is None:
            return None
            
        df = df.copy()
        
        # Médias móveis
        df['sma_5'] = df['close'].rolling(window=5).mean()
        df['sma_10'] = df['close'].rolling(window=10).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        
        # RSI (Relative Strength Index)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close'].ewm(span=12).mean()
        exp2 = df['close'].ewm(span=26).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # Volume médio
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        
        print("Indicadores técnicos adicionados")
        return df
    
    def create_training_prompts(self, df, lookback_window=60):
        """Cria prompts estruturados para treinamento da LLM"""
        if df is None:
            return None
            
        prompts = []
        
        for i in range(lookback_window, len(df)):
            # Dados históricos (janela de lookback)
            historical_data = df.iloc[i-lookback_window:i]
            
            # Próxima vela (target)
            next_candle = df.iloc[i]
            
            # Determinar direção (alta/baixa)
            current_close = historical_data.iloc[-1]['close']
            next_close = next_candle['close']
            direction = "ALTA" if next_close > current_close else "BAIXA"
            
            # Criar prompt estruturado
            prompt_data = {
                "timestamp": next_candle['timestamp'].isoformat(),
                "historical_candles": [],
                "indicators": {},
                "target_direction": direction,
                "price_change": float(next_close - current_close),
                "price_change_percent": float((next_close - current_close) / current_close * 100)
            }
            
            # Adicionar dados históricos das últimas 10 velas
            for j in range(-10, 0):
                candle = historical_data.iloc[j]
                prompt_data["historical_candles"].append({
                    "timestamp": candle['timestamp'].isoformat(),
                    "open": float(candle['open']),
                    "high": float(candle['high']),
                    "low": float(candle['low']),
                    "close": float(candle['close']),
                    "volume": float(candle['volume'])
                })
            
            # Adicionar indicadores técnicos atuais
            last_candle = historical_data.iloc[-1]
            prompt_data["indicators"] = {
                "sma_5": float(last_candle['sma_5']) if not pd.isna(last_candle['sma_5']) else None,
                "sma_10": float(last_candle['sma_10']) if not pd.isna(last_candle['sma_10']) else None,
                "sma_20": float(last_candle['sma_20']) if not pd.isna(last_candle['sma_20']) else None,
                "rsi": float(last_candle['rsi']) if not pd.isna(last_candle['rsi']) else None,
                "macd": float(last_candle['macd']) if not pd.isna(last_candle['macd']) else None,
                "macd_signal": float(last_candle['macd_signal']) if not pd.isna(last_candle['macd_signal']) else None,
                "bb_upper": float(last_candle['bb_upper']) if not pd.isna(last_candle['bb_upper']) else None,
                "bb_middle": float(last_candle['bb_middle']) if not pd.isna(last_candle['bb_middle']) else None,
                "bb_lower": float(last_candle['bb_lower']) if not pd.isna(last_candle['bb_lower']) else None
            }
            
            prompts.append(prompt_data)
        
        print(f"Criados {len(prompts)} prompts de treinamento")
        return prompts
    
    def save_training_data(self, prompts, output_file="training_data.jsonl"):
        """Salva os dados de treinamento em formato JSONL"""
        if not prompts:
            return
            
        with open(output_file, 'w') as f:
            for prompt in prompts:
                # Criar prompt textual para a LLM
                text_prompt = self.create_text_prompt(prompt)
                
                training_example = {
                    "prompt": text_prompt,
                    "completion": prompt["target_direction"],
                    "metadata": {
                        "timestamp": prompt["timestamp"],
                        "price_change": prompt["price_change"],
                        "price_change_percent": prompt["price_change_percent"]
                    }
                }
                
                f.write(json.dumps(training_example) + '\n')
        
        print(f"Dados de treinamento salvos em {output_file}")
    
    def create_text_prompt(self, prompt_data):
        """Cria um prompt textual estruturado para a LLM"""
        text = "Análise de mercado BTC/USDT:\n\n"
        
        # Adicionar dados das últimas velas
        text += "Últimas 5 velas (OHLCV):\n"
        for i, candle in enumerate(prompt_data["historical_candles"][-5:]):
            text += f"Vela {i+1}: O={candle['open']:.2f}, H={candle['high']:.2f}, L={candle['low']:.2f}, C={candle['close']:.2f}, V={candle['volume']:.2f}\n"
        
        # Adicionar indicadores técnicos
        text += "\nIndicadores técnicos atuais:\n"
        indicators = prompt_data["indicators"]
        if indicators["sma_5"]:
            text += f"SMA 5: {indicators['sma_5']:.2f}\n"
        if indicators["sma_10"]:
            text += f"SMA 10: {indicators['sma_10']:.2f}\n"
        if indicators["sma_20"]:
            text += f"SMA 20: {indicators['sma_20']:.2f}\n"
        if indicators["rsi"]:
            text += f"RSI: {indicators['rsi']:.2f}\n"
        if indicators["macd"]:
            text += f"MACD: {indicators['macd']:.4f}\n"
        if indicators["macd_signal"]:
            text += f"MACD Signal: {indicators['macd_signal']:.4f}\n"
        
        text += "\nCom base na análise price action e indicadores técnicos, qual será a direção da próxima vela?"
        
        return text
    
    def process_all_data(self):
        """Executa todo o pipeline de processamento de dados"""
        print("Iniciando processamento de dados...")
        
        # 1. Carregar dados
        raw_data = self.load_all_csv_files()
        if raw_data is None:
            return None
        
        # 2. Limpar e estruturar
        clean_data = self.clean_and_structure_data(raw_data)
        if clean_data is None:
            return None
        
        # 3. Adicionar indicadores técnicos
        enhanced_data = self.add_technical_indicators(clean_data)
        
        # 4. Criar prompts de treinamento (usando apenas uma amostra para economizar tempo)
        sample_size = min(100000, len(enhanced_data))  # Usar no máximo 100k registros para prompts
        sample_data = enhanced_data.tail(sample_size)
        training_prompts = self.create_training_prompts(sample_data)
        
        # 5. Salvar dados de treinamento
        self.save_training_data(training_prompts)
        
        # 6. Salvar dados processados
        enhanced_data.to_csv('processed_btc_data.csv', index=False)
        print("Dados processados salvos em processed_btc_data.csv")
        
        self.processed_data = enhanced_data
        return enhanced_data

if __name__ == "__main__":
    processor = DataProcessor()
    processed_data = processor.process_all_data()
    
    if processed_data is not None:
        print(f"\nResumo dos dados processados:")
        print(f"Período: {processed_data['timestamp'].min()} a {processed_data['timestamp'].max()}")
        print(f"Total de registros: {len(processed_data)}")
        print(f"Colunas: {list(processed_data.columns)}")
    else:
        print("Falha no processamento dos dados")

