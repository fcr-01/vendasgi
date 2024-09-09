import pandas as pd
import os
from datetime import datetime

def main():
    # caminhos dos arquivos
    vendas_file = 'vendas.csv'
    year = datetime.now().year
    new_vendas_file = f'vendas{year}.csv'
    
    # verifica se o arquivo de vendas para o ano corrente já existe
    if os.path.exists(new_vendas_file):
        print(f'O arquivo {new_vendas_file} já existe. Abortando o processo.')
        return
    
    # Verificar a data atual
    today = datetime.now()
    if today.month != 1 or today.day != 1:
        print()
        print("A data atual ainda não é a ideal para essa operação.")
        print("Uma tabela backup do ano corrente será criada e a tabela de vendas atual será zerada.")
        print()
        print("*** Depois de confirmada essa operação não pode ser desfeita ***")
        print()
        print("Deseja continuar? (s/n)")
        resposta = input().strip().lower()
        if resposta != 's':
            print("Processo abortado.")
            return
    
    # Ler a tabela 
    try:
        vendas_df = pd.read_csv(vendas_file, encoding='cp1252', delimiter=';')
    except Exception as e:
        print(f"Erro ao ler o arquivo vendas.csv: {e}")
        return
    
    # cria bkp da tabela para vendas + ano corrente
    try:
        vendas_df.to_csv(new_vendas_file, index=False, encoding='cp1252', sep=';')
        print()
        print(f'Arquivo {new_vendas_file} criado com sucesso.')
    except Exception as e:
        print(f"Erro ao criar o arquivo {new_vendas_file}: {e}")
        return
    
    # manter a linha 1 da tabela
    try:
        
        header = vendas_df.head(0)
        header.to_csv(vendas_file, index=False, encoding='cp1252', sep=';')
        print()
        print(f'Arquivo {vendas_file} foi zerado para o ano corrente.')
    except Exception as e:
        print(f"Erro ao zerar o arquivo vendas.csv: {e}")

if __name__ == "__main__":
    main()
