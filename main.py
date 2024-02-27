import requests
from bs4 import BeautifulSoup
import pandas as pd

def obter_dados():
    url = "https://www.fundamentus.com.br/fii_resultado.php"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    table = soup.find('table')
    rows = table.find_all('tr')[1:]

    resumo = []

    for row in rows:
        cols = row.find_all('td')
        cotacao = cols[2].text.strip().replace('.', '').replace(',', '.')
        ffo_yield = cols[3].text.strip().replace('.', '').replace(',', '.').replace('%', '')
        dividend_yield = cols[4].text.strip().replace('.', '').replace(',', '.').replace('%', '')
        pvp = cols[5].text.strip().replace(',', '.')
        fundo = {
            "Papel": cols[0].text.strip(),
            "Segmento": cols[1].text.strip(),
            "Cotação": float(cotacao),
            "FFO Yield": float(ffo_yield),
            "Dividend Yield": float(dividend_yield),
            "P/VP": float(pvp),
            "Valor de Mercado": cols[6].text.strip(),
            "Liquidez Diária": cols[7].text.strip(),
            "Quantidade de Imóveis": cols[8].text.strip(),
            "Preço/m²": cols[9].text.strip(),
            "Aluguel/m²": cols[10].text.strip(),
            "Cap Rate": cols[11].text.strip(),
            "Vacância Média": cols[12].text.strip()
        }
        resumo.append(fundo)

    return pd.DataFrame(resumo)

def filtros(dataset, opcao):
    if opcao == 1:
        filtro = (dataset['Dividend Yield'] >= 12)
    elif opcao == 2:
        filtro = (dataset['Liquidez Diária'].str.replace('.', '').astype(float) >= 500000)
    elif opcao == 3:
        filtro = (dataset['P/VP'] <= 1.05)
    elif opcao == 4:
        filtro = (dataset['Dividend Yield'] >= 12) & (dataset['Liquidez Diária'].str.replace('.', '').astype(float) >= 500000)
    elif opcao == 5:
        filtro = (dataset['Dividend Yield'] >= 12) & (dataset['Liquidez Diária'].str.replace('.', '').astype(float) >= 500000) & (dataset['P/VP'] <= 1.05) 
    else:
        print("Opção inválida.")
        return

    dadosFiltrados = dataset[filtro]
    if opcao == 5:
        print("Total de registros encontrados para a opção 5:", len(dadosFiltrados))  # Imprimir total de registros
    print(dadosFiltrados)

def main():
    dataset = obter_dados()
    while True:
        print("\n1. Fundos que pagam mais de 1% ao mês")
        print("2. Liquidez diária maior que R$500k")
        print("3. Fundos com P/VP < 1.05")
        print("4. DY > 12% e Liquidez Diária > R$500k")
        print("5. Com todos os parâmetros anteriores (os mais tops)")
        print("0. Sair")
        opcao = int(input("Escolha uma opção: "))
        if opcao == 0:
            print("Saindo...")
            break
        filtros(dataset, opcao)

if __name__ == "__main__":
    main()
