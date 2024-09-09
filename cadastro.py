import csv
from datetime import datetime

def carregar_produtos(nome_arquivo):
    produtos = set()
    try:
        with open(nome_arquivo, mode='r', encoding='latin-1') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  
            for linha in reader:
                if linha:
                    produtos.add(linha[0])
    except FileNotFoundError:
        print(f'O arquivo {nome_arquivo} não foi encontrado.')
    return sorted(produtos)   

# formata para moeda 
def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Adiciona venda 
def adicionar_venda(nome_arquivo, data, produto, quantidade, preco):
    preco_formatado = formatar_valor(preco)
    try:
        with open(nome_arquivo, mode='a', newline='', encoding='latin-1') as file:
            writer = csv.DictWriter(file, fieldnames=["Data", "Produto", "Quantidade", "Preço"], delimiter=';')
            # nova linha de venda
            writer.writerow({"Data": data, "Produto": produto, "Quantidade": quantidade, "Preço": preco_formatado})
    except PermissionError as e:
        print(f"Erro ao acessar o arquivo {nome_arquivo}: {e}")
    except Exception as e:
        print(f"Erro ao escrever no arquivo {nome_arquivo}: {e}")

# data no formato dd/mm/aaaa
def obter_data_atual():
    hoje = datetime.now()
    return hoje.strftime("%d/%m/%Y")

## Ler dados e adicionar a venda
def registrar_venda(produtos_efetivos):
    print()
    data = obter_data_atual()
    print(f"Data atual: {data}")
    print()
    print("Produtos disponíveis:")
    print()
    for i, produto in enumerate(produtos_efetivos, start=1):
        print(f"{i}. {produto}")
        
    escolha = int(input("\nEscolha o número do produto: ")) - 1
    if escolha < 0 or escolha >= len(produtos_efetivos):
        print("Escolha inválida.")
        return

    produto = produtos_efetivos[escolha]
    quantidade = int(input("Digite a quantidade: "))
    preco = float(input("Digite o preço: "))

    nome_arquivo_vendas = 'vendas.csv'
    adicionar_venda(nome_arquivo_vendas, data, produto, quantidade, preco)
    print("\n" f'Cadastrado com sucesso em {nome_arquivo_vendas}')


nome_arquivo_produtos = 'produtos.csv'
produtos_efetivos = carregar_produtos(nome_arquivo_produtos)

# verifica arquivo de vendas, cria com cabeçalho
nome_arquivo_vendas = 'vendas.csv'
try:
    with open(nome_arquivo_vendas, mode='x', newline='', encoding='latin-1') as file:
        writer = csv.DictWriter(file, fieldnames=["Data", "Produto", "Quantidade", "Preço"], delimiter=';')
        writer.writeheader()
except FileExistsError:
    pass
except PermissionError as e:
    print(f"Erro ao acessar o arquivo {nome_arquivo_vendas}: {e}")

# Registra nova venda
registrar_venda(produtos_efetivos)



import subprocess
import sys

def main():
    print()

    # chama consulta
    subprocess.run([sys.executable, 'consulta.py'])
    
    
    sys.exit()

if __name__ == "__main__":
    main()
