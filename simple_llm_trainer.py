import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class SimpleTradingModel:
    def __init__(self):
        self.model = None
        self.feature_columns = []
        
    def prepare_features_from_jsonl(self, jsonl_file):
        """Prepara features a partir do arquivo JSONL de treinamento"""
        features = []
        labels = []
        
        with open(jsonl_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                
                # Extrair features dos indicadores técnicos
                indicators = data['metadata']
                
                feature_row = [
                    indicators.get('price_change', 0),
                    indicators.get('price_change_percent', 0)
                ]
                
                # Adicionar mais features se disponíveis
                features.append(feature_row)
                
                # Label: 1 para ALTA, 0 para BAIXA
                label = 1 if data['completion'] == 'ALTA' else 0
                labels.append(label)
        
        self.feature_columns = ['price_change', 'price_change_percent']
        
        return np.array(features), np.array(labels)
    
    def prepare_features_from_csv(self, csv_file, lookback_window=10):
        """Prepara features a partir do CSV processado"""
        df = pd.read_csv(csv_file)
        
        features = []
        labels = []
        
        for i in range(lookback_window, len(df) - 1):
            # Features: indicadores técnicos atuais
            current_row = df.iloc[i]
            next_row = df.iloc[i + 1]
            
            feature_row = [
                current_row.get('sma_5', 0) or 0,
                current_row.get('sma_10', 0) or 0,
                current_row.get('sma_20', 0) or 0,
                current_row.get('rsi', 50) or 50,
                current_row.get('macd', 0) or 0,
                current_row.get('macd_signal', 0) or 0,
                current_row.get('bb_upper', 0) or 0,
                current_row.get('bb_middle', 0) or 0,
                current_row.get('bb_lower', 0) or 0,
                current_row.get('volume_sma', 0) or 0,
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
        """Treina o modelo de classificação"""
        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            features, labels, test_size=test_size, random_state=42, stratify=labels
        )
        
        # Treinar Random Forest (modelo simples mas eficaz)
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        print("Treinando modelo...")
        self.model.fit(X_train, y_train)
        
        # Avaliar modelo
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Acurácia do modelo: {accuracy:.4f}")
        print("\nRelatório de classificação:")
        print(classification_report(y_test, y_pred, target_names=['BAIXA', 'ALTA']))
        
        # Importância das features
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nImportância das features:")
        print(feature_importance)
        
        return accuracy
    
    def predict(self, features):
        """Faz predição para novas features"""
        if self.model is None:
            raise ValueError("Modelo não foi treinado ainda")
        
        prediction = self.model.predict(features.reshape(1, -1))[0]
        probability = self.model.predict_proba(features.reshape(1, -1))[0]
        
        direction = "ALTA" if prediction == 1 else "BAIXA"
        confidence = max(probability)
        
        return direction, confidence
    
    def save_model(self, filename="trading_model.pkl"):
        """Salva o modelo treinado"""
        if self.model is None:
            raise ValueError("Modelo não foi treinado ainda")
        
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns
        }
        
        joblib.dump(model_data, filename)
        print(f"Modelo salvo em {filename}")
    
    def load_model(self, filename="trading_model.pkl"):
        """Carrega um modelo salvo"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Arquivo {filename} não encontrado")
        
        model_data = joblib.load(filename)
        self.model = model_data['model']
        self.feature_columns = model_data['feature_columns']
        
        print(f"Modelo carregado de {filename}")

class OpenAIFineTuner:
    """Classe para fine-tuning usando OpenAI API (alternativa mais avançada)"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("OPENAI_API_KEY não encontrada. Fine-tuning OpenAI não disponível.")
    
    def prepare_openai_format(self, jsonl_file, output_file="openai_training_data.jsonl"):
        """Converte dados para formato OpenAI fine-tuning"""
        if not self.api_key:
            return None
        
        with open(jsonl_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                data = json.loads(line)
                
                # Formato OpenAI para fine-tuning
                openai_format = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "Você é um especialista em análise técnica de Bitcoin. Analise os dados fornecidos e preveja se a próxima vela será de ALTA ou BAIXA."
                        },
                        {
                            "role": "user",
                            "content": data['prompt']
                        },
                        {
                            "role": "assistant",
                            "content": data['completion']
                        }
                    ]
                }
                
                outfile.write(json.dumps(openai_format) + '\n')
        
        print(f"Dados formatados para OpenAI salvos em {output_file}")
        return output_file
    
    def create_fine_tuning_job(self, training_file):
        """Cria um job de fine-tuning na OpenAI (requer API key válida)"""
        if not self.api_key:
            print("OpenAI API key necessária para fine-tuning")
            return None
        
        try:
            import openai
            openai.api_key = self.api_key
            
            # Upload do arquivo de treinamento
            with open(training_file, 'rb') as f:
                response = openai.File.create(
                    file=f,
                    purpose='fine-tune'
                )
            
            file_id = response['id']
            print(f"Arquivo enviado com ID: {file_id}")
            
            # Criar job de fine-tuning
            fine_tune_response = openai.FineTuningJob.create(
                training_file=file_id,
                model="gpt-3.5-turbo"
            )
            
            job_id = fine_tune_response['id']
            print(f"Job de fine-tuning criado com ID: {job_id}")
            
            return job_id
            
        except Exception as e:
            print(f"Erro no fine-tuning OpenAI: {e}")
            return None

def main():
    print("=== Treinamento de Modelo de Trading ===\n")
    
    # Opção 1: Modelo simples com Random Forest
    print("1. Treinando modelo Random Forest...")
    simple_model = SimpleTradingModel()
    
    # Usar dados do CSV processado
    if os.path.exists('processed_btc_data.csv'):
        print("Carregando dados do CSV processado...")
        features, labels = simple_model.prepare_features_from_csv('processed_btc_data.csv')
        
        print(f"Features shape: {features.shape}")
        print(f"Labels shape: {labels.shape}")
        print(f"Distribuição de labels - BAIXA: {np.sum(labels == 0)}, ALTA: {np.sum(labels == 1)}")
        
        # Treinar modelo
        accuracy = simple_model.train_model(features, labels)
        
        # Salvar modelo
        simple_model.save_model()
        
        print(f"\nModelo Random Forest treinado com acurácia: {accuracy:.4f}")
    
    # Opção 2: Preparar dados para OpenAI fine-tuning
    print("\n2. Preparando dados para OpenAI fine-tuning...")
    openai_tuner = OpenAIFineTuner()
    
    if os.path.exists('training_data.jsonl'):
        openai_file = openai_tuner.prepare_openai_format('training_data.jsonl')
        if openai_file:
            print("Dados preparados para OpenAI. Para fazer fine-tuning:")
            print("1. Configure sua OPENAI_API_KEY")
            print("2. Execute openai_tuner.create_fine_tuning_job('openai_training_data.jsonl')")
    
    print("\n=== Treinamento Concluído ===")

if __name__ == "__main__":
    main()

