@echo off

cls
chcp 65001 > nul 2>&1
echo ===============================================================================
echo                                HOJE: %date%
echo =============================================================================== 
echo ::: ATENÇÃO ::: este processo limpa a tabela de vendas para um novo ano fiscal.
echo ===============================================================================
echo                LEIA AS INFORMAÇÕES A SEGUIR ANTES DE CONTINUAR
echo ===============================================================================
pause
cls
python novoano.py
