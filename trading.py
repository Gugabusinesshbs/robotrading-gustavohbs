from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import random
import time

trading_bp = Blueprint('trading', __name__)

# Carregar o modelo treinado (você precisa ter este arquivo)
try:
    model = joblib.load('lightweight_trading_model.pkl')
except:
    model = None

# Variáveis globais para simular estado
is_trading_active = False
current_balance = 1000.0
total_trades = 0
win_rate = 0.54

@trading_bp.route('/status', methods=['GET'])
def get_status():
    global is_trading_active, current_balance, total_trades, win_rate
    
    # Simular preço atual do BTC
    current_price = 50000 + random.uniform(-1000, 1000)
    
    return jsonify({
        'is_active': is_trading_active,
        'current_price': current_price,
        'balance': current_balance,
        'total_trades': total_trades,
        'win_rate': win_rate
    })

@trading_bp.route('/prediction', methods=['GET'])
def get_prediction():
    # Simular predição da IA
    directions = ['ALTA', 'BAIXA']
    direction = random.choice(directions)
    confidence = random.uniform(0.6, 0.9)
    
    return jsonify({
        'direction': direction,
        'confidence': confidence
    })

@trading_bp.route('/price-history', methods=['GET'])
def get_price_history():
    # Simular histórico de preços
    data = []
    base_price = 50000
    
    for i in range(50):
        price = base_price + random.uniform(-2000, 2000)
        data.append({
            'time': f'{i:02d}:00',
            'price': price
        })
    
    return jsonify(data)

@trading_bp.route('/recent-trades', methods=['GET'])
def get_recent_trades():
    # Simular trades recentes
    trades = []
    for i in range(10):
        trade = {
            'id': i,
            'direction': random.choice(['ALTA', 'BAIXA']),
            'time': f'{random.randint(10, 23):02d}:{random.randint(0, 59):02d}',
            'result': random.choice(['WIN', 'LOSS']),
            'profit': random.uniform(-50, 100),
            'type': 'AUTO'
        }
        trades.append(trade)
    
    return jsonify(trades)

@trading_bp.route('/analytics', methods=['GET'])
def get_analytics():
    return jsonify({
        'total_return': 2727,
        'sharpe_ratio': 0.316,
        'max_drawdown': 23.14,
        'total_profit': 27270,
        'avg_profit_per_trade': 10.25
    })

@trading_bp.route('/settings', methods=['GET'])
def get_settings():
    return jsonify({
        'trade_amount': 100,
        'stop_loss': 50,
        'take_profit': 80,
        'min_confidence': 0.70,
        'max_trades_per_day': 20
    })

@trading_bp.route('/logs', methods=['GET'])
def get_logs():
    logs = [
        {'timestamp': '14:30:15', 'level': 'INFO', 'message': 'Sistema iniciado'},
        {'timestamp': '14:30:20', 'level': 'INFO', 'message': 'Modelo carregado com sucesso'},
        {'timestamp': '14:31:00', 'level': 'INFO', 'message': 'Predição: ALTA (75.2%)'},
        {'timestamp': '14:32:15', 'level': 'SUCCESS', 'message': 'Trade executado: +$25.50'},
        {'timestamp': '14:33:00', 'level': 'INFO', 'message': 'Aguardando próximo sinal'}
    ]
    return jsonify(logs)

@trading_bp.route('/toggle', methods=['POST'])
def toggle_trading():
    global is_trading_active
    is_trading_active = not is_trading_active
    
    return jsonify({
        'is_active': is_trading_active,
        'message': 'Trading ativado' if is_trading_active else 'Trading desativado'
    })

