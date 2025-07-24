# 💻 Guia de Implementação Local do Sistema de Trading

Este guia detalha os passos necessários para configurar e executar o sistema de trading automatizado localmente em sua máquina. Isso permitirá que você tenha controle total sobre o ambiente e faça modificações conforme suas necessidades.

## 1. Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados em seu sistema:

- **Python 3.11+**: Para o backend Flask e scripts de processamento de dados.
  - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+**: Para o frontend React e suas dependências.
  - [Download Node.js](https://nodejs.org/en/download/)
- **Git**: Para clonar o repositório do projeto.
  - [Download Git](https://git-scm.com/downloads)

## 2. Configuração do Backend (Flask)

O backend é responsável pela lógica de trading, comunicação com o modelo de IA e fornecimento de dados para o frontend.

### 2.1. Clonar o Repositório

Primeiro, você precisará clonar o repositório do projeto para sua máquina local. Se você já tem os arquivos, pode pular esta etapa.

```bash
git clone <URL_DO_REPOSITORIO> # Substitua pela URL real do seu repositório
cd trading-system # Navegue até o diretório raiz do projeto
```

### 2.2. Instalar Dependências

Navegue até o diretório do backend e instale as bibliotecas Python necessárias. É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

```bash
cd trading-backend
python3.11 -m venv venv
source venv/bin/activate # No Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as seguintes dependências:

```
pandas
numpy
scikit-learn
flask
flask-cors
matplotlib
```

### 2.3. Copiar o Modelo Treinado

O modelo de Machine Learning treinado (`lightweight_trading_model.pkl`) precisa estar acessível pelo backend. Certifique-se de que ele esteja no diretório raiz do `trading-backend`.

```bash
cp /caminho/para/lightweight_trading_model.pkl /caminho/para/trading-backend/
```

### 2.4. Iniciar o Servidor Backend

Com as dependências instaladas e o modelo no lugar, você pode iniciar o servidor Flask:

```bash
cd trading-backend
source venv/bin/activate # Ative o ambiente virtual novamente se necessário
python src/main.py
```

O servidor Flask será iniciado e estará acessível em `http://127.0.0.1:5000` por padrão. Você verá mensagens no terminal indicando que o servidor está rodando.

## 3. Configuração do Frontend (React)

O frontend é a interface de usuário que permite visualizar os dados, predições e controlar o sistema.

### 3.1. Instalar Dependências

Abra um novo terminal, navegue até o diretório do frontend e instale as dependências Node.js:

```bash
cd trading-dashboard
npm install
```

### 3.2. Configurar a URL da API

Você precisará garantir que o frontend esteja apontando para o endereço correto do seu backend local. Abra o arquivo `trading-dashboard/src/App.jsx` e verifique a linha que define `API_BASE`:

```javascript
// trading-dashboard/src/App.jsx
const API_BASE = 'http://127.0.0.1:5000/api/trading'; // Certifique-se de que seja este endereço
```

Se o endereço for diferente (por exemplo, se você o alterou para o URL de deploy permanente), mude-o de volta para `http://127.0.0.1:5000/api/trading` para que ele se conecte ao seu backend local.

### 3.3. Iniciar o Servidor Frontend

Com as dependências instaladas e a URL da API configurada, você pode iniciar o servidor de desenvolvimento do React:

```bash
cd trading-dashboard
npm run dev
```

O frontend será iniciado e geralmente estará acessível em `http://localhost:5173` (ou outra porta, se 5173 estiver em uso). O terminal indicará o endereço exato.

## 4. Verificando a Implementação Local

Após iniciar ambos os servidores (backend e frontend):

1. Abra seu navegador e acesse o endereço do frontend (ex: `http://localhost:5173`).
2. Você deverá ver o dashboard de trading carregando e exibindo dados.
3. O botão "Iniciar Trading" deve interagir com o backend, e você poderá ver logs no terminal do backend quando as requisições forem feitas.

## 5. Solução de Problemas Comuns

- **"Network Error" no Frontend:** Verifique se o servidor Flask está rodando e se a `API_BASE` no `App.jsx` está correta (`http://127.0.0.1:5000/api/trading`).
- **Porta em Uso:** Se um dos servidores não iniciar devido a uma porta já em uso, você pode tentar alterar a porta (consulte a documentação do Flask e Vite/React para como fazer isso).
- **Dependências Faltando:** Certifique-se de que todas as dependências foram instaladas corretamente para ambos os projetos (`pip install -r requirements.txt` e `npm install`).

---

**Desenvolvido por Manus AI**

*Este guia é um recurso educacional e não constitui aconselhamento financeiro. O trading envolve riscos.*

