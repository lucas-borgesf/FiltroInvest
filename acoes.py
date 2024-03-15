import requests
from bs4 import BeautifulSoup
import pandas as pd


class Acoes:
    def __init__(self, dataset):
        self.dataset = dataset

    def obter_dados_acoes(self):
        url = "https://www.fundamentus.com.br/resultado.php"
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
            acao = {
                "Papel": cols[0].text.strip(),
                "Cotacao": cols[2].text.strip().replace(".", "").replace(",", "."),
                "PL": cols[3].text.strip().replace(".", "").replace(",", "."),
                "PVP": cols[5].text.strip().replace(",", "."),
                "DividendYield": cols[4]
                .text.strip()
                .replace(".", "")
                .replace(",", "."),
                "PAtivo": cols[6].text.strip().replace(".", "").replace(",", "."),
                "PCapGiro": cols[7].text.strip().replace(".", "").replace(",", "."),
                "PEbit": cols[8].text.strip().replace(".", "").replace(",", "."),
                "PAtivoCirc": cols[9].text.strip().replace(".", "").replace(",", "."),
                "EVEbit": cols[10].text.strip().replace(".", "").replace(",", "."),
                "EVEbita": cols[11].text.strip().replace(".", "").replace(",", "."),
                "MrgEbit": cols[12].text.strip().replace(".", "").replace(",", "."),
                "MrgLiq": cols[13].text.strip().replace(".", "").replace(",", "."),
                "LiqCorrente": cols[14].text.strip().replace(".", "").replace(",", "."),
                "ROIC": cols[15].text.strip().replace(".", "").replace(",", "."),
                "ROE": cols[16].text.strip().replace(".", "").replace(",", "."),
                "Liq2Meses": cols[17].text.strip().replace(".", "").replace(",", "."),
                "PatriLiquido": cols[18]
                .text.strip()
                .replace(".", "")
                .replace(",", "."),
                "DivBruta_por_Patri": cols[19]
                .text.strip()
                .replace(".", "")
                .replace(",", "."),
                "Cresc_5a": cols[20].text.strip().replace(".", "").replace(",", "."),
            }
            resumo.append(acao)

        self.dataset = pd.DataFrame(resumo)

    def filtro_buffett(self):
        self.dataset["ROE"] = self.dataset["ROE"].str.replace("%", "")
        return self.dataset[
            (self.dataset["PL"].astype(float) <= 22.5)
            & (self.dataset["ROE"].astype(float) >= 15)
            & (self.dataset["DividendYield"].astype(float) >= 2.5)
        ]

    def filtro_graham(self):
        self.dataset["PVP"] = (
            self.dataset["PVP"]
            .str.replace("%", "")
            .str.replace(".", "")
            .str.replace(",", "")
            .astype(float)
        )
        self.dataset["ROE"] = self.dataset["ROE"].str.replace("%", "")
        return self.dataset[
            (self.dataset["PL"].astype(float) <= 15)
            & (self.dataset["PVP"] <= 1)
            & (self.dataset["ROE"].astype(float) >= 10)
        ]

    def filtro_barsi(self):
        return self.dataset[
            (self.dataset["DividendYield"].astype(float) >= 6)
            & (self.dataset["PVP"].astype(float) <= 0.5)
        ]

    def filtro_lynch(self):
        self.dataset["Cresc_5a"] = self.dataset["Cresc_5a"].str.rstrip("%")
        return self.dataset[
            (self.dataset["Cresc_5a"].astype(float) > 20)
            & (
                self.dataset["PL"].astype(float)
                < self.dataset["Cresc_5a"].astype(float)
            )
        ]

    def filtro_fisher(self):
        self.dataset["ROE"] = self.dataset["ROE"].str.replace("%", "")
        return self.dataset[
            (self.dataset["ROE"].astype(float) > 15)
            & (self.dataset["LiqCorrente"].astype(float) > 1.5)
        ]

    def filtro_greenblatt(self):
        self.dataset["ROIC"] = self.dataset["ROIC"].str.rstrip("%")
        self.dataset["Liq2Meses"] = self.dataset["Liq2Meses"].str.rstrip("%")
        return self.dataset[
            (
                self.dataset["ROIC"].astype(float)
                > self.dataset["Liq2Meses"].astype(float)
            )
        ]
