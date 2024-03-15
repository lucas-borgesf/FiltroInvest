import requests
from bs4 import BeautifulSoup
import pandas as pd

def obter_dados():
    url = "https://www.fundamentus.com.br/fii_resultado.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")[1:]

    resumo = []

    for row in rows:
        cols = row.find_all("td")
        cotacao = cols[2].text.strip().replace(".", "").replace(",", ".")
        ffo_yield = cols[3].text.strip().replace(".", "").replace(",", ".").replace("%", "")
        dividend_yield = cols[4].text.strip().replace(".", "").replace(",", ".").replace("%", "")
        pvp = cols[5].text.strip().replace(",", ".")
        fundo = {
            "papel": cols[0].text.strip(),
            "segmento": cols[1].text.strip(),
            "cotacao": cotacao,
            "ffoyield": ffo_yield,
            "dy": dividend_yield,
            "pvp": pvp,
            "valorMercado": cols[6].text.strip(),
            "liquidezDiaria": cols[7].text.strip(),
            "qntdImoveis": cols[8].text.strip(),
            "precoM2": cols[9].text.strip(),
            "aluguelM2": cols[10].text.strip(),
            "capRate": cols[11].text.strip(),
            "vacanciaMedia": cols[12].text.strip(),
        }
        resumo.append(fundo)

    return pd.DataFrame(resumo)

def filtros(dataset, opcao):
    if opcao == 1:
        dy_limite = float(input("DY maior que: "))
        filtro = (dataset['dy'].astype(float) >= dy_limite)
    elif opcao == 2:
        liquidez_limite = float(input("Liquidez diária maior que: "))
        filtro = (dataset['liquidezDiaria'].str.replace('.', '').astype(float) >= liquidez_limite)
    elif opcao == 3:
        pvp_limite = float(input("Limitede de P/VP: "))
        filtro = (dataset['pvp'].astype(float) <= pvp_limite)
    elif opcao == 4:
        dy_limite = float(input("DY maior que: "))
        liquidez_limite = float(input("Liquidez diária maior que: "))
        filtro = (dataset['dy'].astype(float) >= dy_limite) & (dataset['liquidezDiaria'].str.replace('.', '').astype(float) >= liquidez_limite)
    elif opcao == 5:
        dy_limite = float(input("DY maior que: "))
        liquidez_limite = float(input("Liquidez diária maior que: "))
        pvp_limite = float(input("Limite de P/VP: "))
        filtro = (dataset['dy'].astype(float) >= dy_limite) & (dataset['liquidezDiaria'].str.replace('.', '').astype(float) >= liquidez_limite) & (dataset['pvp'].astype(float) <= pvp_limite)
    else:
        print("Opção inválida.")
        return

    dadosFiltrados = dataset[filtro]
    if opcao == 5:
        print("Fundos com todos os filtros:", len(dadosFiltrados)) 
    print(dadosFiltrados)
