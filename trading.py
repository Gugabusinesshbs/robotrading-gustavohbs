from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import json
from datetime import datetime, timedelta
import random
import time
import threading

trading_bp = Blueprint('trading', __name__)

# Estado global do sistema
trading_state = {
    'is_active': False,
    'current_price': 50000,
    'balance': 1000,
    'total_trades': 0,
    'win_rate': 0.75,
    'recent_trades': [],
    'price_history': [],
    'current_prediction': {'direction': 'ALTA', 'confidence': 0.75}
}

# Inicializar dados históricos
def initialize_price_history():
    base_time = datetime.now() - timedelta(minutes=10)
    for i in range(10):
        trading_state['price_history'].append({
            'time': (base_time + timedelta(minutes=i)).strftime('%H:%M'),
            'price': 49800 + i * 25 + random.randint(-50, 50),
            'volume': 1000 + random.randint(-200, 300)
        })

initialize_price_history()

# Simulador de dados em tempo real
def price_simulator():
    while True:
        if trading_state['is_active']:
            # Simular mudança de preço
            change = random.uniform(-100, 100)
            trading_state['current_price'] = max(trading_state['current_price'] + change, 45000)
            
            # Atualizar histórico de preços
            current_time = datetime.now().strftime('%H:%M')
            new_data = {
                'time': current_time,
                'price': trading_state['current_price'],
                'volume': 1000 + random.randint(-200, 300)
            }
            
            trading_state['price_history'].append(new_data)
            if len(trading_state['price_history']) > 20:
                trading_state['price_history'].pop(0)
            
            # Simular nova predição
            trading_state['current_prediction'] = {
                'direction': random.choice(['ALTA', 'BAIXA']),
                'confidence': 0.5 + random.random() * 0.4
            }
            
            # Simular trade ocasional
            if random.random() < 0.1:  # 10% de chance de fazer um trade
                execute_simulated_trade()
        
        time.sleep(3)  # Atualizar a cada 3 segundos

def execute_simulated_trade():
    """Simula a execução de um trade baseado na predição"""
    prediction = trading_state['current_prediction']
    
    # Simular resultado do trade (75% de acerto baseado na confiança)
    success_probability = prediction['confidence']
    is_win = random.random() < success_probability
    
    # Calcular lucro/prejuízo
    trade_amount = 50  # Valor fixo por trade
    if is_win:
        profit = trade_amount * 0.8  # 80% de retorno
    else:
        profit = -trade_amount * 0.5  # 50% de perda
    
    # Atualizar saldo
    trading_state['balance'] += profit
    trading_state['total_trades'] += 1
    
    # Adicionar aos trades recentes
    new_trade = {
        'id': trading_state['total_trades'],
        'time': datetime.now().strftime('%H:%M'),
        'direction': prediction['direction'],
        'result': 'WIN' if is_win else 'LOSS',
        'profit': profit
    }
    
    trading_state['recent_trades'].insert(0, new_trade)
    if len(trading_state['recent_trades']) > 10:
        trading_state['recent_trades'].pop()
    
    # Recalcular win rate
    wins = sum(1 for trade in trading_state['recent_trades'] if trade['result'] == 'WIN')
    trading_state['win_rate'] = wins / len(trading_state['recent_trades']) if trading_state['recent_trades'] else 0.75

# Iniciar simulador em thread separada
simulator_thread = threading.Thread(target=price_simulator, daemon=True)
simulator_thread.start()

@trading_bp.route('/status', methods=['GET'])
@cross_origin()
def get_status():
    """Retorna o status atual do sistema de trading"""
    return jsonify({
        'is_active': trading_state['is_active'],
        'current_price': round(trading_state['current_price'], 2),
        'balance': round(trading_state['balance'], 2),
        'total_trades': trading_state['total_trades'],
        'win_rate': round(trading_state['win_rate'], 4),
        'model_available': True
    })

@trading_bp.route('/toggle', methods=['POST'])
@cross_origin()
def toggle_trading():
    """Liga/desliga o sistema de trading"""
    trading_state['is_active'] = not trading_state['is_active']
    
    return jsonify({
        'is_active': trading_state['is_active'],
        'message': 'Trading ativado' if trading_state['is_active'] else 'Trading desativado'
    })

@trading_bp.route('/prediction', methods=['GET'])
@cross_origin()
def get_prediction():
    """Retorna a predição atual da IA"""
    return jsonify(trading_state['current_prediction'])

@trading_bp.route('/price-history', methods=['GET'])
@cross_origin()
def get_price_history():
    """Retorna o histórico de preços"""
    return jsonify(trading_state['price_history'])

@trading_bp.route('/recent-trades', methods=['GET'])
@cross_origin()
def get_recent_trades():
    """Retorna os trades recentes"""
    return jsonify(trading_state['recent_trades'])

@trading_bp.route('/analytics', methods=['GET'])
@cross_origin()
def get_analytics():
    """Retorna dados analíticos do sistema"""
    total_profit = sum(trade['profit'] for trade in trading_state['recent_trades'])
    
    return jsonify({
        'total_return': round((total_profit / 1000) * 100, 2),  # Percentual baseado no saldo inicial
        'sharpe_ratio': round(0.85 + random.uniform(-0.1, 0.1), 2),
        'max_drawdown': round(-5.2 + random.uniform(-1, 1), 2),
        'total_profit': round(total_profit, 2),
        'avg_profit_per_trade': round(total_profit / max(len(trading_state['recent_trades']), 1), 2)
    })

@trading_bp.route('/settings', methods=['GET'])
@cross_origin()
def get_settings():
    """Retorna as configurações atuais do sistema"""
    return jsonify({
        'trade_amount': 50.00,
        'stop_loss': 2.0,
        'take_profit': 3.0,
        'min_confidence': 0.70,
        'max_trades_per_day': 20,
        'risk_management': 'medium'
    })

@trading_bp.route('/settings', methods=['POST'])
@cross_origin()
def update_settings():
    """Atualiza as configurações do sistema"""
    data = request.get_json()
    
    # Aqui você implementaria a lógica para salvar as configurações
    # Por enquanto, apenas retornamos sucesso
    
    return jsonify({
        'success': True,
        'message': 'Configurações atualizadas com sucesso',
        'settings': data
    })

@trading_bp.route('/logs', methods=['GET'])
@cross_origin()
def get_logs():
    """Retorna os logs do sistema"""
    logs = [
        {'timestamp': '09:05:23', 'level': 'INFO', 'message': 'Sistema iniciado com sucesso'},
        {'timestamp': '09:05:24', 'level': 'INFO', 'message': 'Conectado à API de dados'},
        {'timestamp': '09:05:25', 'level': 'WARNING', 'message': 'Modelo carregado - Disponível: True'},
        {'timestamp': '09:05:26', 'level': 'INFO', 'message': f'Trading {"ativado" if trading_state["is_active"] else "desativado"}'},
        {'timestamp': '09:05:27', 'level': 'INFO', 'message': 'Aguardando próximo sinal...'}
    ]
    
    return jsonify(logs)

@trading_bp.route('/manual-trade', methods=['POST'])
@cross_origin()
def manual_trade():
    """Executa um trade manual"""
    data = request.get_json()
    direction = data.get('direction', 'ALTA')
    amount = data.get('amount', 50)
    
    # Simular execução do trade manual
    is_win = random.random() < 0.6  # 60% de chance de sucesso para trades manuais
    profit = amount * 0.8 if is_win else -amount * 0.5
    
    trading_state['balance'] += profit
    trading_state['total_trades'] += 1
    
    new_trade = {
        'id': trading_state['total_trades'],
        'time': datetime.now().strftime('%H:%M'),
        'direction': direction,
        'result': 'WIN' if is_win else 'LOSS',
        'profit': profit,
        'type': 'MANUAL'
    }
    
    trading_state['recent_trades'].insert(0, new_trade)
    if len(trading_state['recent_trades']) > 10:
        trading_state['recent_trades'].pop()
    
    return jsonify({
        'success': True,
        'trade': new_trade,
        'new_balance': round(trading_state['balance'], 2)
    })

