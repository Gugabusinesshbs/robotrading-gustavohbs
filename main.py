from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.trading import trading_bp
import os

app = Flask(__name__)
CORS(app)

# Registrar as rotas de trading
app.register_blueprint(trading_bp, url_prefix='/api/trading')

# Servir arquivos estáticos do frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join('static', path)):
        return send_from_directory('static', path)
    else:
        return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

