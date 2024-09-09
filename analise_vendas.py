import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv('vendas.csv', encoding='cp1252', sep=';', usecols=['Data', 'Produto', 'Quantidade', 'Preço'])

# Renomear coluna Preço Valor
df.rename(columns={'Preço': 'Valor'}, inplace=True)

# campo Valor numérico
df['Valor'] = df['Valor'].str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

# total de vendas
total_vendas = df['Valor'].sum()

# quantidade de produtos vendidos
total_quantidade_vendas = df['Quantidade'].sum()

# Formata moeda
def format_currency(value):
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

print(f'\n > Valor total das vendas: {format_currency(total_vendas)}')
print()
print(f' > Número total de vendas: {total_quantidade_vendas}')

# Produtos mais vendidos
produtos_mais_vendidos = df.groupby('Produto')['Quantidade'].sum().sort_values(ascending=False)

# limita produtos mais vendidos
produtos_mais_vendidos = produtos_mais_vendidos.head(10)  

print("\n OS 10 PRODUTOS MAIS VENDIDOS: \n")
print(produtos_mais_vendidos.to_frame())

# Cria coluna 'Mes' e agrupa vendas mensais
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, format='%d/%m/%Y')
df['Mes'] = df['Data'].dt.to_period('M')

# receita mensal
receita_mensal = df.groupby('Mes')['Valor'].sum()

receita_mensal_formatada = receita_mensal.apply(format_currency)

receita_mensal_formatada_df = pd.DataFrame({
    'Mês': [m.strftime('%m/%Y') for m in receita_mensal.index.to_timestamp()],
    'Valor': receita_mensal_formatada
})

max_mes_length = receita_mensal_formatada_df['Mês'].str.len().max()
max_valor_length = receita_mensal_formatada_df['Valor'].str.len().max()

print("\n RECEITA MENSAL:\n")

print(receita_mensal_formatada_df.to_string(index=False, col_space=[max_mes_length + 5, max_valor_length + 5]))
print()

resposta = input(" Deseja exibir os gráficos? (s/n): ").strip().lower()

if resposta == 's':
    # gráfico dos produtos mais vendidos
    produtos_mais_vendidos.plot(kind='bar', title='Produtos mais vendidos', color='skyblue')
    plt.xlabel('Produto')
    plt.ylabel('Quantidade Vendida')
    plt.xticks(rotation=45, ha='right')  
    plt.tight_layout(pad=2.0)  
    plt.show()

    # Gráfico receita mensal
    fig, ax = plt.subplots()
    ax.plot(receita_mensal.index.astype(str), receita_mensal, marker='o', color='green')

    ax.set_title('Receita Mensal')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Receita')
    ax.grid(True)  

    
    ax.set_xticks(range(len(receita_mensal)))
    ax.set_xticklabels([m.strftime('%m/%Y') for m in receita_mensal.index.to_timestamp()], rotation=45)

    plt.tight_layout(pad=2.0)   
    plt.show()

else:
    print()
