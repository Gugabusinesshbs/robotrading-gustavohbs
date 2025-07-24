import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import json

class TradingBacktest:
    """Sistema de backtest para validar estratégias de trading"""
    
    def __init__(self, initial_balance=1000, trade_amount=50):
        self.initial_balance = initial_balance
        self.trade_amount = trade_amount
        self.balance = initial_balance
        self.trades = []
        self.equity_curve = []
        
    def load_data(self, csv_file):
        """Carrega dados históricos para backtest"""
        print(f"Carregando dados de {csv_file}...")
        
        # Carregar apenas uma amostra para o backtest
        chunk_size = 10000
        df = pd.read_csv(csv_file, nrows=chunk_size)
        
        print(f"Dados carregados: {len(df)} registros")
        return df
    
    def simulate_predictions(self, df):
        """Simula predições baseadas em indicadores técnicos"""
        predictions = []
        
        for i in range(len(df)):
            row = df.iloc[i]
            
            # Estratégia simples baseada em médias móveis
            if pd.notna(row.get('sma_5')) and pd.notna(row.get('sma_20')):
                if row['sma_5'] > row['sma_20']:
                    direction = 'ALTA'
                    confidence = 0.6 + (row.get('rsi', 50) - 50) / 100 * 0.3
                else:
                    direction = 'BAIXA'
                    confidence = 0.6 + (50 - row.get('rsi', 50)) / 100 * 0.3
            else:
                direction = 'ALTA' if np.random.random() > 0.5 else 'BAIXA'
                confidence = 0.5 + np.random.random() * 0.3
            
            # Garantir que a confiança está entre 0.5 e 0.9
            confidence = max(0.5, min(0.9, confidence))
            
            predictions.append({
                'direction': direction,
                'confidence': confidence
            })
        
        return predictions
    
    def run_backtest(self, df, predictions, min_confidence=0.7):
        """Executa o backtest com as predições"""
        print(f"Executando backtest com {len(df)} registros...")
        print(f"Confiança mínima: {min_confidence}")
        
        for i in range(len(df) - 1):
            current_row = df.iloc[i]
            next_row = df.iloc[i + 1]
            prediction = predictions[i]
            
            # Verificar se a predição atende ao critério de confiança
            if prediction['confidence'] < min_confidence:
                continue
            
            # Verificar se há dados válidos
            if pd.isna(current_row['close']) or pd.isna(next_row['close']):
                continue
            
            # Determinar o resultado real
            actual_direction = 'ALTA' if next_row['close'] > current_row['close'] else 'BAIXA'
            is_correct = prediction['direction'] == actual_direction
            
            # Calcular lucro/prejuízo
            if is_correct:
                profit = self.trade_amount * 0.8  # 80% de retorno
            else:
                profit = -self.trade_amount * 0.5  # 50% de perda
            
            # Atualizar saldo
            self.balance += profit
            
            # Registrar trade
            trade = {
                'timestamp': current_row.get('timestamp', i),
                'entry_price': current_row['close'],
                'exit_price': next_row['close'],
                'direction': prediction['direction'],
                'confidence': prediction['confidence'],
                'actual_direction': actual_direction,
                'result': 'WIN' if is_correct else 'LOSS',
                'profit': profit,
                'balance': self.balance
            }
            
            self.trades.append(trade)
            self.equity_curve.append({
                'index': i,
                'balance': self.balance,
                'timestamp': current_row.get('timestamp', i)
            })
        
        print(f"Backtest concluído. Total de trades: {len(self.trades)}")
    
    def calculate_metrics(self):
        """Calcula métricas de performance"""
        if not self.trades:
            return {}
        
        # Métricas básicas
        total_trades = len(self.trades)
        winning_trades = sum(1 for trade in self.trades if trade['result'] == 'WIN')
        losing_trades = total_trades - winning_trades
        
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        # Lucros e perdas
        total_profit = sum(trade['profit'] for trade in self.trades)
        total_return = (self.balance - self.initial_balance) / self.initial_balance * 100
        
        avg_profit_per_trade = total_profit / total_trades if total_trades > 0 else 0
        
        # Drawdown máximo
        peak = self.initial_balance
        max_drawdown = 0
        
        for point in self.equity_curve:
            if point['balance'] > peak:
                peak = point['balance']
            
            drawdown = (peak - point['balance']) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # Sharpe Ratio simplificado
        returns = [trade['profit'] / self.trade_amount for trade in self.trades]
        if len(returns) > 1:
            avg_return = np.mean(returns)
            std_return = np.std(returns)
            sharpe_ratio = avg_return / std_return if std_return > 0 else 0
        else:
            sharpe_ratio = 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'total_return': total_return,
            'avg_profit_per_trade': avg_profit_per_trade,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'final_balance': self.balance
        }
    
    def generate_report(self):
        """Gera relatório detalhado do backtest"""
        metrics = self.calculate_metrics()
        
        print("\n" + "="*50)
        print("RELATÓRIO DE BACKTEST")
        print("="*50)
        
        print(f"Saldo Inicial: ${self.initial_balance:.2f}")
        print(f"Saldo Final: ${metrics['final_balance']:.2f}")
        print(f"Lucro Total: ${metrics['total_profit']:.2f}")
        print(f"Retorno Total: {metrics['total_return']:.2f}%")
        
        print(f"\nTotal de Trades: {metrics['total_trades']}")
        print(f"Trades Vencedores: {metrics['winning_trades']}")
        print(f"Trades Perdedores: {metrics['losing_trades']}")
        print(f"Taxa de Acerto: {metrics['win_rate']:.2%}")
        
        print(f"\nLucro Médio por Trade: ${metrics['avg_profit_per_trade']:.2f}")
        print(f"Drawdown Máximo: {metrics['max_drawdown']:.2f}%")
        print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")
        
        return metrics
    
    def plot_equity_curve(self, save_path=None):
        """Plota a curva de equity"""
        if not self.equity_curve:
            print("Nenhum dado de equity para plotar")
            return
        
        plt.figure(figsize=(12, 6))
        
        indices = [point['index'] for point in self.equity_curve]
        balances = [point['balance'] for point in self.equity_curve]
        
        plt.plot(indices, balances, 'b-', linewidth=2, label='Saldo')
        plt.axhline(y=self.initial_balance, color='r', linestyle='--', label='Saldo Inicial')
        
        plt.title('Curva de Equity - Backtest')
        plt.xlabel('Número do Trade')
        plt.ylabel('Saldo ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico salvo em: {save_path}")
        
        plt.show()
    
    def save_results(self, filename):
        """Salva os resultados do backtest em JSON"""
        results = {
            'metrics': self.calculate_metrics(),
            'trades': self.trades,
            'equity_curve': self.equity_curve,
            'parameters': {
                'initial_balance': self.initial_balance,
                'trade_amount': self.trade_amount
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Resultados salvos em: {filename}")

def main():
    """Função principal para executar o backtest"""
    print("=== Sistema de Backtest de Trading ===\n")
    
    # Inicializar backtest
    backtest = TradingBacktest(initial_balance=1000, trade_amount=50)
    
    # Carregar dados
    try:
        df = backtest.load_data('processed_btc_data.csv')
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. Criando dados simulados...")
        # Criar dados simulados para demonstração
        dates = pd.date_range(start='2024-01-01', periods=1000, freq='1H')
        df = pd.DataFrame({
            'timestamp': dates,
            'close': 50000 + np.cumsum(np.random.randn(1000) * 100),
            'sma_5': None,
            'sma_20': None,
            'rsi': 50 + np.random.randn(1000) * 15
        })
        
        # Calcular médias móveis
        df['sma_5'] = df['close'].rolling(window=5).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
    
    # Gerar predições
    predictions = backtest.simulate_predictions(df)
    
    # Executar backtest
    backtest.run_backtest(df, predictions, min_confidence=0.7)
    
    # Gerar relatório
    metrics = backtest.generate_report()
    
    # Plotar curva de equity
    try:
        backtest.plot_equity_curve('equity_curve.png')
    except Exception as e:
        print(f"Erro ao plotar gráfico: {e}")
    
    # Salvar resultados
    backtest.save_results('backtest_results.json')
    
    return metrics

if __name__ == "__main__":
    main()

