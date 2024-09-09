import pandas as pd
from datetime import datetime

# consulta todos os produtos vendidos no mês
def consultar_produtos_vendidos(arquivo_csv):
    try:
        dados = pd.read_csv(arquivo_csv, encoding='latin1', delimiter=';')
        
        dados.columns = dados.columns.str.strip()  
        dados.columns = dados.columns.str.replace(' ', '_')  

        # verifica colunas 
        colunas_necessarias = {'Produto', 'Quantidade', 'Data'}
        if not colunas_necessarias.issubset(dados.columns):
            raise ValueError(f"O arquivo CSV deve conter as colunas {colunas_necessarias}.")

        # Converte Data para datetime
        formatos_possiveis = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']
        datas_convertidas = None

        for formato in formatos_possiveis:
            try:
                datas_convertidas_temp = pd.to_datetime(dados['Data'], format=formato, errors='coerce')
                if datas_convertidas_temp.notnull().all():
                    datas_convertidas = datas_convertidas_temp
                    break
            except ValueError:
                continue

        if datas_convertidas is None:
            raise ValueError("Algumas datas não puderam ser convertidas. Verifique o formato da coluna 'Data'.")

        dados['Data'] = datas_convertidas

        # filtra os dados do mês atual
        mes_atual = datetime.now().strftime('%m-%Y')
        dados_mes = dados[dados['Data'].dt.strftime('%m-%Y') == mes_atual]

        if dados_mes.empty:
            print("Ainda não há vendas registradas para o mês atual.")
            return

        # agrupa e soma as quantidades
        produtos_vendidos = dados_mes.groupby('Produto')['Quantidade'].sum()
        print("\n *** Todos os produtos vendidos no mês:""\n")
        
        for produto, quantidade in produtos_vendidos.items():
            print(f"{produto}: {quantidade}")

    except Exception as e:
        print(f"Erro ao consultar produtos: {e}")

def main():
    csv_file = 'vendas.csv'
    consultar_produtos_vendidos(csv_file)

if __name__ == "__main__":
    main()
