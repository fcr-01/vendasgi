import csv
from datetime import datetime
import os

def obter_mes_atual():
    hoje = datetime.now()
    return hoje.strftime("%m/%Y")  

def listar_vendas_mes_atual(nome_arquivo):
    mes_atual = obter_mes_atual()
    try:
        with open(nome_arquivo, mode='r', encoding='latin-1') as file:
            reader = csv.DictReader(file, delimiter=';')
            vendas = [linha for linha in reader if datetime.strptime(linha['Data'], '%d/%m/%Y').strftime('%m/%Y') == mes_atual]
            return vendas
    except FileNotFoundError:
        print(f'O arquivo {nome_arquivo} não foi encontrado.')
        return []
    except Exception as e:
        print(f"Erro ao listar vendas: {e}")
        return []

def exibir_vendas(vendas):
    if not vendas:
        print("Nenhuma venda encontrada para o mês atual.")
        return
    print()
    print("Vendas do mês atual:")
    print()
    for i, venda in enumerate(vendas):
        print(f"{i + 1}. Data: {venda['Data']}, Produto: {venda['Produto']}, Quantidade: {venda['Quantidade']}, Preço: {venda['Preço']}")

def remover_venda(nome_arquivo, indice_venda):
    try:
        with open(nome_arquivo, mode='r', encoding='latin-1') as file:
            reader = csv.DictReader(file, delimiter=';')
            vendas = list(reader)

        mes_atual = obter_mes_atual()
        vendas_mes_atual = [venda for venda in vendas if datetime.strptime(venda['Data'], '%d/%m/%Y').strftime('%m/%Y') == mes_atual]

        if 0 <= indice_venda < len(vendas_mes_atual):
            venda_a_remover = vendas_mes_atual[indice_venda]

            # Confirmação antes de remover
            confirmar = input(f" \n > Tem certeza que deseja excluir a venda?\n\nData: {venda_a_remover['Data']}\nProduto: {venda_a_remover['Produto']}\nQuantidade: {venda_a_remover['Quantidade']}\nPreço: {venda_a_remover['Preço']}\n\n > Digite 's' para confirmar: ").strip().lower()
            if confirmar == 's':
                vendas.remove(venda_a_remover)
                with open(nome_arquivo, mode='w', newline='', encoding='latin-1') as file:
                    writer = csv.DictWriter(file, fieldnames=["Data", "Produto", "Quantidade", "Preço"], delimiter=';')
                    writer.writeheader()
                    writer.writerows(vendas)
                print()
                print("Venda removida com sucesso.")
                return True
            else:
                print()
                print("Entrada inválida. Exclusão abortada.")
                return False
        else:
            print()
            print("Índice de venda inválido.")
            return False
    except FileNotFoundError:
        print()
        print(f'O arquivo {nome_arquivo} não foi encontrado.')
        return False
    except Exception as e:
        print()
        print(f"Erro ao remover a venda: {e}")
        return False

def excluir_venda():
    nome_arquivo_vendas = 'vendas.csv'
    
    while True:
        vendas_mes_atual = listar_vendas_mes_atual(nome_arquivo_vendas)
        exibir_vendas(vendas_mes_atual)
        print()
        if not vendas_mes_atual:
            print()
            print("Processo encerrado.")
            break
            
        escolha = input("Escolha o número da venda para excluir ou pressione 'ENTER' para sair: ").strip()
        if escolha == '':
            print()
            print("Saindo sem realizar nenhuma exclusão.")
            break

        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(vendas_mes_atual):
                if remover_venda(nome_arquivo_vendas, indice):
                    break
                else:
                    break
            else:
                print()
                print("Índice de venda inválido. Por favor, insira um número válido.")
        except ValueError:
            print()
            print("Entrada inválida. Por favor, insira um número válido ou pressione 'ENTER' para sair.")


excluir_venda()
