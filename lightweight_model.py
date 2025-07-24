import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import joblib
import json

class LightweightTradingModel:
    def __init__(self):
        self.model = None
        self.imputer = None
        self.scaler = None
        self.feature_columns = []
        
    def prepare_sample_data(self, csv_file, sample_size=50000):
        """Prepara uma amostra dos dados para treinamento mais rápido"""
        print(f"Carregando dados de {csv_file}...")
        
        # Carregar apenas as colunas necessárias
        columns_needed = ['timestamp', 'close', 'sma_5', 'sma_10', 'sma_20', 'rsi', 'macd', 'macd_signal', 'bb_upper', 'bb_middle', 'bb_lower', 'volume_sma', 'volume']
        
        # Ler o arquivo em chunks para economizar memória
        chunk_size = 100000
        chunks = []
        
        for chunk in pd.read_csv(csv_file, chunksize=chunk_size, usecols=columns_needed):
            chunks.append(chunk)
            if len(chunks) * chunk_size >= sample_size * 2:  # Pegar mais dados para ter margem
                break
        
        df = pd.concat(chunks, ignore_index=True)
        
        # Pegar uma amostra aleatória
        if len(df) > sample_size:
            df = df.sample(n=sample_size, random_state=42).sort_values('timestamp')
        
        print(f"Dados carregados: {len(df)} registros")
        
        features = []
        labels = []
        
        for i in range(1, len(df) - 1):
            current_row = df.iloc[i]
            next_row = df.iloc[i + 1]
            
            # Verificar se há dados válidos para close
            if pd.isna(current_row['close']) or pd.isna(next_row['close']):
                continue
            
            # Features: indicadores técnicos atuais
            feature_row = [
                current_row['sma_5'],
                current_row['sma_10'],
                current_row['sma_20'],
                current_row['rsi'],
                current_row['macd'],
                current_row['macd_signal'],
                current_row['bb_upper'],
                current_row['bb_middle'],
                current_row['bb_lower'],
                current_row['volume_sma'],
                current_row['close'],
                current_row['volume']
            ]
            
            # Label: 1 se próximo close > close atual, 0 caso contrário
            label = 1 if next_row['close'] > current_row['close'] else 0
            
            features.append(feature_row)
            labels.append(label)
        
        self.feature_columns = [
            'sma_5', 'sma_10', 'sma_20', 'rsi', 'macd', 'macd_signal',
            'bb_upper', 'bb_middle', 'bb_lower', 'volume_sma', 'close', 'volume'
        ]
        
        return np.array(features), np.array(labels)
    
    def train_model(self, features, labels, test_size=0.2):
        """Treina um modelo logístico (mais rápido que Random Forest)"""
        print(f"Preparando dados para treinamento...")
        print(f"Features shape: {features.shape}")
        print(f"Labels shape: {labels.shape}")
        print(f"Distribuição - BAIXA: {np.sum(labels == 0)}, ALTA: {np.sum(labels == 1)}")
        
        # Tratar valores NaN com imputer
        print("Tratando valores ausentes...")
        self.imputer = SimpleImputer(strategy='median')
        features_imputed = self.imputer.fit_transform(features)
        
        # Normalizar features
        print("Normalizando features...")
        self.scaler = StandardScaler()
        features_scaled = self.scaler.fit_transform(features_imputed)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            features_scaled, labels, test_size=test_size, random_state=42, stratify=labels
        )
        
        # Treinar modelo logístico
        print("Treinando modelo de Regressão Logística...")
        self.model = LogisticRegression(
            random_state=42,
            max_iter=1000,
            solver='liblinear'
        )
        
        self.model.fit(X_train, y_train)
        
        # Avaliar modelo
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nAcurácia do modelo: {accuracy:.4f}")
        print("\nRelatório de classificação:")
        print(classification_report(y_test, y_pred, target_names=['BAIXA', 'ALTA']))
        
        return accuracy
    
    def predict(self, features):
        """Faz predição para novas features"""
        if self.model is None:
            raise ValueError("Modelo não foi treinado ainda")
        
        # Garantir que features é um array 2D
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        # Aplicar imputer e scaler
        features_imputed = self.imputer.transform(features)
        features_scaled = self.scaler.transform(features_imputed)
        
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        direction = "ALTA" if prediction == 1 else "BAIXA"
        confidence = max(probability)
        
        return direction, confidence
    
    def save_model(self, filename="lightweight_trading_model.pkl"):
        """Salva o modelo treinado"""
        if self.model is None:
            raise ValueError("Modelo não foi treinado ainda")
        
        model_data = {
            'model': self.model,
            'imputer': self.imputer,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }
        
        joblib.dump(model_data, filename)
        print(f"Modelo salvo em {filename}")
    
    def load_model(self, filename="lightweight_trading_model.pkl"):
        """Carrega um modelo salvo"""
        model_data = joblib.load(filename)
        self.model = model_data['model']
        self.imputer = model_data['imputer']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        print(f"Modelo carregado de {filename}")

class TradingPredictor:
    """Classe para fazer predições em tempo real"""
    
    def __init__(self, model_file="lightweight_trading_model.pkl"):
        self.model = LightweightTradingModel()
        self.model.load_model(model_file)
    
    def predict_next_candle(self, current_data):
        """
        Prediz a direção da próxima vela
        current_data deve ser um dict com as chaves:
        ['sma_5', 'sma_10', 'sma_20', 'rsi', 'macd', 'macd_signal',
         'bb_upper', 'bb_middle', 'bb_lower', 'volume_sma', 'close', 'volume']
        """
        features = np.array([
            current_data.get('sma_5', np.nan),
            current_data.get('sma_10', np.nan),
            current_data.get('sma_20', np.nan),
            current_data.get('rsi', np.nan),
            current_data.get('macd', np.nan),
            current_data.get('macd_signal', np.nan),
            current_data.get('bb_upper', np.nan),
            current_data.get('bb_middle', np.nan),
            current_data.get('bb_lower', np.nan),
            current_data.get('volume_sma', np.nan),
            current_data['close'],
            current_data['volume']
        ])
        
        direction, confidence = self.model.predict(features)
        
        return {
            'direction': direction,
            'confidence': confidence,
            'timestamp': current_data.get('timestamp', 'N/A')
        }

def main():
    print("=== Treinamento de Modelo Leve de Trading ===\n")
    
    model = LightweightTradingModel()
    
    # Treinar com uma amostra menor dos dados
    if pd.io.common.file_exists('processed_btc_data.csv'):
        features, labels = model.prepare_sample_data('processed_btc_data.csv', sample_size=10000)
        
        if len(features) > 0:
            accuracy = model.train_model(features, labels)
            model.save_model()
            
            print(f"\n✅ Modelo treinado com sucesso!")
            print(f"📊 Acurácia: {accuracy:.4f}")
            print(f"💾 Modelo salvo como 'lightweight_trading_model.pkl'")
            
            # Teste de predição
            print("\n🔮 Teste de predição:")
            sample_data = {
                'close': 50000,
                'volume': 1000,
                'sma_5': 49800,
                'sma_10': 49500,
                'sma_20': 49000,
                'rsi': 65,
                'macd': 100,
                'macd_signal': 80,
                'bb_upper': 51000,
                'bb_middle': 50000,
                'bb_lower': 49000,
                'volume_sma': 1200
            }
            
            predictor = TradingPredictor()
            result = predictor.predict_next_candle(sample_data)
            
            print(f"Predição: {result['direction']} (Confiança: {result['confidence']:.2f})")
            
        else:
            print("❌ Erro: Não foi possível preparar os dados para treinamento")
    else:
        print("❌ Erro: Arquivo 'processed_btc_data.csv' não encontrado")

if __name__ == "__main__":
    main()

