import pandas as pd
from datetime import datetime

# consulta os + vendidos do mês
def consultar_mais_vendidos(arquivo_csv, top_n=None):
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

        if top_n:
            # agrupa e soma as quantidades, ordena e seleciona os top_n produtos
            produtos_mais_vendidos = dados_mes.groupby('Produto')['Quantidade'].sum()
            produtos_mais_vendidos = produtos_mais_vendidos.sort_values(ascending=False).head(top_n)
            print(f"\n *** Os {top_n} produtos mais vendidos do mês:""\n")
        else:
            produtos_mais_vendidos = dados_mes.groupby('Produto')['Quantidade'].sum()
            print("\n *** Todos os produtos vendidos no mês:""\n")
        
        for produto, quantidade in produtos_mais_vendidos.items():
            print(f"{produto}: {quantidade}")

    except Exception as e:
        print(f"Erro ao consultar produtos: {e}")

def main():
    csv_file = 'vendas.csv'
    
    while True:
        resposta = input("\nDeseja consultar as vendas do mês? (s/n): ").strip().lower()
        
        if resposta == 's':
            escolha = input("\nEscolha uma opção:\n\n1. Os 10 produtos mais vendidos do mês\n2. Todos os produtos vendidos no mês\n\nDigite 1 ou 2: ").strip()    
            if escolha == '1':
                consultar_mais_vendidos(csv_file, top_n=10)
            elif escolha == '2':
                consultar_mais_vendidos(csv_file, top_n=None)
            else:
                print("Opção inválida, sessão encerrada.")
        
            break  
        elif resposta == 'n':
            print()
            break  
        else:
            print("Resposta inválida. Digite 's' para sim ou 'n' para não.")
    
    print()

if __name__ == "__main__":
    main()
