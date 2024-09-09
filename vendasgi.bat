@echo off

chcp 65001 > nul 2>&1
:MENU
cls
echo.
echo *************************************
echo *   Delícias e Bolos da Gi Ateliê   *
echo *                                   *
echo *   1. Analisar Vendas              *
echo *   2. Cadastrar Venda              *
echo *   3. Consulta Vendas              *      
echo *   4. Apagar Venda                 *
echo *   5. Sair                         *
echo *************************************
echo.
set /p choice=Escolha uma opção: 

if "%choice%"=="1" goto ANALISE_VENDAS
if "%choice%"=="2" goto CADASTRO
if "%choice%"=="3" goto CONSULTA
if "%choice%"=="4" goto APAGA_VENDAS
if "%choice%"=="5" goto EXIT

:ANALISE_VENDAS
cls
echo.
echo ::: ANÁLISE DE VENDAS :::
python analise_vendas.py
echo.
goto MENU

:CADASTRO
cls
echo.
echo ::: CADASTRAR VENDA :::
python cadastro.py
echo.
pause
goto MENU

:CONSULTA
cls
echo.
echo ::: CONSULTA VENDAS DO MÊS :::
python consulta10.py
echo.
pause
goto MENU

:APAGA_VENDAS
cls
echo.
echo ::: CANCELAR UMA VENDA DO MÊS ::: 
python apaga_venda.py
echo.
pause
goto MENU

:EXIT
cls
echo. 
echo Para retornar ao menu digite: vendasgi
exit /b
