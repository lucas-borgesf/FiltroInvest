from acoes import *
from fundo import *


class Main:
    def __init__(self):
        self.dataset_acoes = None
        self.dataset_fundos = None
        self.acoes = None
        self.fundos = None

    def carregar_acoes(self):
        if self.dataset_acoes is None:
            self.acoes = Acoes(None)
            self.acoes.obter_dados_acoes()
            self.dataset_acoes = self.acoes.dataset

    def carregar_fundos(self):
        if self.dataset_fundos is None:
            self.dataset_fundos = obter_dados()

    def menu_principal(self):
        print("\n=== MENU PRINCIPAL ===")
        print("1--> Para Açãoes")
        print("2--> Para Fundos")
        print("00--> Para Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            self.carregar_acoes()
            self.menu_acoes()
        elif opcao == "2":
            self.carregar_fundos()
            self.menu_fundos()
        elif opcao == "00":
            print("Saindo...")
            return
        else:
            print("Opção inválida. Tente novamente.")
            self.menu_principal()

    def menu_acoes(self):
        print("\n=== MENU DE AÇÕES ===")
        print("1--> Filtrar por Buffett")
        print("2--> Filtrar por Graham")
        print("3--> Filtrar por Barsi")
        print("4--> Filtrar por Lynch")
        print("5--> Filtrar por Fisher")
        print("6--> Filtrar por Greenblatt")
        print("00--> Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao in {"1", "2", "3", "4", "5", "6"}:
            if opcao == "1":
                resultado = self.acoes.filtro_buffett()
            elif opcao == "2":
                resultado = self.acoes.filtro_graham()
            elif opcao == "3":
                resultado = self.acoes.filtro_barsi()
            elif opcao == "4":
                resultado = self.acoes.filtro_lynch()
            elif opcao == "5":
                resultado = self.acoes.filtro_fisher()
            elif opcao == "6":
                resultado = self.acoes.filtro_greenblatt()

            print(resultado.to_string(index=False))
            print(f"\nForam encontrados {len(resultado)} resultados.")
            self.menu_acoes()
        elif opcao == "00":
            self.menu_principal()
        else:
            print("Opção inválida. Tente novamente.")
            self.menu_acoes()

    def menu_fundos(self):
        print("\n=== MENU DE FUNDOS ===")
        print("1--> Filtrar por DY")
        print("2--> Filtrar por Liquidez Diária")
        print("3--> Filtrar por P/VP")
        print("4--> Filtrar por DY e Liquidez Diária")
        print("5--> Filtrar por DY, Liquidez Diária e P/VP")
        print("00--> Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao in {"1", "2", "3", "4", "5"}:
            opcao = int(opcao)
            filtros(self.dataset_fundos, opcao)
            self.menu_fundos()
        elif opcao == "00":
            self.menu_principal()
        else:
            print("Opção inválida. Tente novamente.")
            self.menu_fundos()


if __name__ == "__main__":
    main = Main()
    main.menu_principal()
