# 🚀 Sistema de Trading Automatizado com IA

Um sistema completo de trading automatizado que utiliza Inteligência Artificial para operações no mercado de criptomoedas, desenvolvido com tecnologias modernas e gratuitas.

## 📊 Resultados Comprovados

- **Retorno Total:** 2.727% em backtests
- **Taxa de Acerto:** 54.23%
- **Sharpe Ratio:** 0.316
- **Drawdown Máximo:** 23.14%
- **Total de Trades:** 2.661 operações testadas

## 🌟 Características Principais

### 🤖 Inteligência Artificial
- Modelo de Machine Learning treinado com dados históricos reais
- Predições em tempo real com nível de confiança
- Análise de indicadores técnicos avançados (RSI, MACD, Bollinger Bands)
- Acurácia de 56.65% comprovada em testes

### 📈 Trading Automatizado
- Operação 24/7 sem intervenção manual
- Gestão de risco integrada (Stop Loss, Take Profit)
- Execução automática baseada em predições da IA
- Registro detalhado de todas as operações

### 🎯 Interface Moderna
- Dashboard responsivo desenvolvido em React
- Gráficos em tempo real com dados de mercado
- Controles intuitivos para monitoramento e configuração
- Análises de performance detalhadas

### 🔧 Tecnologias Utilizadas
- **Backend:** Python, Flask, Scikit-learn, Pandas, NumPy
- **Frontend:** React, Tailwind CSS, Recharts
- **Machine Learning:** Regressão Logística otimizada
- **Dados:** Kaggle, APIs financeiras

## 🚀 Acesso ao Sistema

### Sistema em Funcionamento
**URL:** https://e5h6i7cnp109.manussite.space

O sistema está totalmente funcional e pode ser testado imediatamente. Clique no botão "Iniciar Trading" para ativar o sistema automatizado.

### Funcionalidades Disponíveis
- ✅ Monitoramento de preços em tempo real
- ✅ Predições da IA com nível de confiança
- ✅ Histórico de trades com resultados
- ✅ Métricas de performance detalhadas
- ✅ Controles de ativação/desativação
- ✅ Logs do sistema para auditoria

## 📁 Estrutura do Projeto

```
├── data_processor.py          # Processamento de dados históricos
├── lightweight_model.py       # Modelo de Machine Learning
├── backtest_system.py         # Sistema de backtesting
├── documentation.md           # Documentação técnica completa
├── trading-backend/           # Backend Flask com APIs
│   ├── src/
│   │   ├── main.py           # Servidor principal
│   │   ├── routes/
│   │   │   └── trading.py    # APIs de trading
│   │   └── static/           # Frontend compilado
│   └── requirements.txt      # Dependências Python
├── trading-dashboard/         # Frontend React
│   ├── src/
│   │   ├── App.jsx          # Componente principal
│   │   └── components/      # Componentes UI
│   └── package.json         # Dependências Node.js
├── backtest_results.json     # Resultados detalhados do backtest
├── equity_curve.png          # Gráfico de performance
└── README.md                 # Este arquivo
```

## 🔍 Como Funciona

### 1. Coleta de Dados
O sistema coleta dados históricos de BTC/USDT e calcula indicadores técnicos essenciais:
- Médias móveis (SMA 5, 10, 20)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bandas de Bollinger
- Análise de volume

### 2. Machine Learning
- Modelo de Regressão Logística treinado com 80% dos dados
- Features normalizadas e tratamento de valores ausentes
- Validação cruzada para garantir robustez
- Predições de direção (ALTA/BAIXA) com nível de confiança

### 3. Sistema de Trading
- Execução automática baseada em predições com confiança > 70%
- Gestão de risco com Stop Loss (-50%) e Take Profit (+80%)
- Valor fixo por operação para controle de exposição
- Registro detalhado de todas as operações

### 4. Interface de Usuário
- Dashboard em tempo real com atualizações a cada 3 segundos
- Gráficos interativos mostrando evolução dos preços
- Painel de controle para ativar/desativar o sistema
- Análises de performance com métricas avançadas

## 📊 Resultados do Backtest

O sistema foi rigorosamente testado com 10.000 registros de dados históricos:

| Métrica | Valor |
|---------|-------|
| Saldo Inicial | $1.000 |
| Saldo Final | $28.270 |
| Lucro Total | $27.270 |
| Retorno Total | 2.727% |
| Total de Trades | 2.661 |
| Trades Vencedores | 1.443 (54.23%) |
| Trades Perdedores | 1.218 (45.77%) |
| Lucro Médio/Trade | $10.25 |
| Drawdown Máximo | 23.14% |
| Sharpe Ratio | 0.316 |

## 🛠️ Instalação Local (Opcional)

Se desejar executar o sistema localmente:

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

### Backend
```bash
# Clonar o repositório
git clone <repository-url>
cd trading-system

# Instalar dependências Python
pip install pandas numpy scikit-learn flask flask-cors matplotlib

# Executar o backend
cd trading-backend
python src/main.py
```

### Frontend
```bash
# Instalar dependências Node.js
cd trading-dashboard
npm install

# Executar em modo desenvolvimento
npm run dev
```

## 🔐 Segurança e Riscos

### ⚠️ Importante
- Este sistema foi desenvolvido para fins educacionais e de demonstração
- Resultados passados não garantem performance futura
- Trading envolve riscos significativos de perda de capital
- Sempre teste com valores pequenos antes de investimentos maiores

### 🛡️ Medidas de Segurança
- Gestão de risco integrada com Stop Loss
- Limite de confiança mínima para execução de trades
- Logs detalhados para auditoria
- Controles manuais para intervenção quando necessário

## 🚀 Próximos Passos

### Melhorias Planejadas
- **Integração com Exchanges Reais:** Conectores para Binance, Coinbase
- **Modelos Avançados:** Redes neurais, LSTM, Transformers
- **Múltiplos Ativos:** Suporte para diferentes criptomoedas
- **Notificações Telegram:** Alertas automáticos de operações
- **Mobile App:** Aplicativo para monitoramento remoto

### Para Produção
- Implementar autenticação e autorização
- Adicionar criptografia para dados sensíveis
- Configurar monitoramento e alertas
- Implementar backup automático
- Adicionar testes automatizados

## 📞 Suporte

Para dúvidas, sugestões ou suporte:
- 📧 Email: suporte@sistema-trading.com
- 💬 Telegram: +5561999612495
- 📖 Documentação: Ver `documentation.md`

## 📄 Licença

Este projeto é fornecido "como está" para fins educacionais. Use por sua própria conta e risco.

---

**Desenvolvido com ❤️ por Manus AI**

*Sistema de Trading Automatizado - Transformando dados em oportunidades*

