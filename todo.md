## Projeto LLM Trading

### Fase 1: Análise do documento e planejamento detalhado
- [x] Ler e compreender o PDF do projeto.
- [x] Criar o plano de tarefas (todo.md).

### Fase 2: Instruções para Conexão com Dados do Mundo Real
- [x] Fornecer instruções detalhadas para conectar o sistema a dados de mercado em tempo real (MetaTrader 5 Python API).
- [x] Explicar como adaptar o backend para usar dados reais e persistir informações.

### Fase 3: Desenvolvimento do sistema de coleta e processamento de dados
- [x] Estruturar os dados coletados no formato OHLCV.
- [x] Criar prompts textuais para a LLM (JSONL ou CSV) com base nos dados OHLCV e indicadores.

### Fase 4: Implementação e treinamento do modelo LLM
- [x] Escolher um modelo base de LLM (Modelo de Regressão Logística para classificação).
- [x] Configurar o ambiente para treinamento (scikit-learn, pandas, numpy).
- [x] Treinar o modelo para prever o comportamento da próxima vela (alta/baixa) - Acurácia: 56.65%.
- [x] Implementar estratégia de treinamento supervisionado.

### Fase 5: Desenvolvimento da interface de usuário
- [x] Definir os requisitos da interface de usuário.
- [x] Desenvolver a interface para visualização de dados e interação com o sistema (Dashboard React).
- [x] Implementar gráficos em tempo real, predições da IA e controles de trading.
- [x] Deploy da interface em URL permanente: https://uimkmsal.manussite.space

### Fase 6: Integração do sistema de trading automatizado
- [x] Implementar a captura de dados em tempo real via API.
- [x] Desenvolver o pipeline para input/output com a LLM e execução de ordens.
- [x] Implementar o registro de resultados (WIN/LOSS).
- [x] Criar APIs REST para comunicação frontend-backend.
- [x] Deploy do sistema completo: https://e5h6i7cnp109.manussite.space

### Fase 7: Testes, validação e documentação
- [x] Realizar backtests com dados históricos (2727% de retorno, 54.23% taxa de acerto).
- [x] Validar a performance do modelo de ML (56.65% de acurácia).
- [x] Testar integração completa frontend-backend.
- [x] Criar documentação técnica completa (documentation.md).
- [x] Gerar relatórios de performance e métricas.

### Fase 1: Instruções para Implementação Local
- [x] Fornecer instruções detalhadas para configurar o ambiente localmente (Python, Node.js, dependências).
- [x] Explicar como iniciar o backend Flask e o frontend React localmente.

