@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: --- Variáveis de Configuração ---
SET PROJECT_DIR=%~dp0
SET PYTHON_VERSION=python
SET NODE_VERSION=node

ECHO ==================================================
ECHO           Instalador do Sistema de Trading
ECHO ==================================================
ECHO.

:: --- 1. Verificar Pré-requisitos ---
ECHO [1/7] Verificando pré-requisitos (Python e Node.js)...
%PYTHON_VERSION% --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Erro: Python nao encontrado. Por favor, instale Python %PYTHON_VERSION% ou superior.
    ECHO Download: https://www.python.org/downloads/
    PAUSE
    EXIT /B 1
)
%NODE_VERSION% --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Erro: Node.js nao encontrado. Por favor, instale Node.js %NODE_VERSION% ou superior.
    ECHO Download: https://nodejs.org/en/download/
    PAUSE
    EXIT /B 1
)
ECHO Pré-requisitos verificados com sucesso.
ECHO.

:: --- 2. Configurar Backend (Python) ---
ECHO [2/7] Configurando o Backend (Python)...
CD "%PROJECT_DIR%trading-backend"

ECHO Criando ambiente virtual Python...
%PYTHON_VERSION% -m venv venv
IF %ERRORLEVEL% NEQ 0 (
    ECHO Erro ao criar ambiente virtual Python.
    PAUSE
    EXIT /B 1
)

ECHO Ativando ambiente virtual Python...
CALL venv\Scripts\activate
IF %ERRORLEVEL% NEQ 0 (
    ECHO Erro ao ativar ambiente virtual Python.
    PAUSE
    EXIT /B 1
)

ECHO Instalando dependencias Python...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO Erro ao instalar dependencias Python.
    PAUSE
    EXIT /B 1
)
ECHO Backend configurado com sucesso.
ECHO.

:: --- 3. Configurar Frontend (Node.js) ---
ECHO [3/7] Configurando o Frontend (Node.js)...
CD "%PROJECT_DIR%trading-dashboard"

ECHO Instalando dependencias Node.js...
npm install
IF %ERRORLEVEL% NEQ 0 (
    ECHO Erro ao instalar dependencias Node.js.
    PAUSE
    EXIT /B 1
)
ECHO Frontend configurado com sucesso.
ECHO.

:: --- 4. Configurar Credenciais Kaggle (Opcional, se o modelo precisar de download) ---
ECHO [4/7] Configurando credenciais Kaggle (Opcional).
ECHO Se voce nao pretende baixar dados do Kaggle, pode pular esta etapa.
SET /P KAGGLE_USERNAME="Digite seu nome de usuario Kaggle (deixe em branco para pular): "
IF NOT "%KAGGLE_USERNAME%"=="" (
    SET /P KAGGLE_KEY="Digite sua chave de API Kaggle: "
    ECHO {"username":"%KAGGLE_USERNAME%","key":"%KAGGLE_KEY%"} > "%USERPROFILE%\.kaggle\kaggle.json"
    IF %ERRORLEVEL% NEQ 0 (
        ECHO Erro ao salvar credenciais Kaggle.
        PAUSE
        EXIT /B 1
    )
    ECHO Credenciais Kaggle salvas em %%USERPROFILE%%\.kaggle\kaggle.json
) ELSE (
    ECHO Configuracao Kaggle pulada.
)
ECHO.

:: --- 5. Copiar Modelo Treinado ---
ECHO [5/7] Copiando o modelo treinado (lightweight_trading_model.pkl)...
ECHO Certifique-se de que o arquivo lightweight_trading_model.pkl esteja na mesma pasta que este script.
IF EXIST "%PROJECT_DIR%lightweight_trading_model.pkl" (
    COPY "%PROJECT_DIR%lightweight_trading_model.pkl" "%PROJECT_DIR%trading-backend\lightweight_trading_model.pkl"
    IF %ERRORLEVEL% NEQ 0 (
        ECHO Erro ao copiar o modelo treinado.
        PAUSE
        EXIT /B 1
    )
    ECHO Modelo treinado copiado com sucesso.
) ELSE (
    ECHO Aviso: lightweight_trading_model.pkl nao encontrado na pasta do script.
    ECHO O sistema funcionara com dados simulados se o modelo nao for fornecido.
)
ECHO.

:: --- 6. Instrucoes para Iniciar os Servidores ---
ECHO [6/7] Instrucoes para iniciar os servidores:
ECHO.
ECHO Para iniciar o Backend (Flask):
ECHO   Abra um novo Prompt de Comando, navegue ate a pasta 'trading-backend\src' e execute:
ECHO     python main.py
ECHO.
ECHO Para iniciar o Frontend (React):
ECHO   Abra outro Prompt de Comando, navegue ate a pasta 'trading-dashboard' e execute:
ECHO     npm run dev
ECHO.
ECHO O frontend estara acessivel em http://localhost:5173
ECHO O backend estara acessivel em http://localhost:5000
ECHO.

:: --- 7. Conclusao ---
ECHO [7/7] Instalacao concluida com sucesso!
ECHO.
ECHO Pressione qualquer tecla para sair.
PAUSE
EXIT /B 0


