from questoes import *

if __name__ == "__main__":

    while True:
        try:
            opt = int(input("Escolha a questão para rodar:\n\n1- Questão 1\n2- Questão 2\n3- Questão 3\n0- Sair\n\nSua escolha: "))
            match(opt):
                case 1:
                    arquivo = "data/Market_Basket_Optimisation.csv"
                    top_items, freq_sets, rules = questao1(arquivo, min_support=300, min_confidence=0.3)

                    print("Itens mais frequentes")
                    print(top_items.head(10))

                    print("\nConjuntos de itens frequentes")
                    print(freq_sets.sort_values(by="support", ascending=False).head(10))
                    print("\nPressione enter para escolher outra opção.")
                case 2:
                    pass
                case 3:
                    pass
                case 0:
                    print("\nSaindo...")
                    exit()
                case _:
                    input("Valor Inválido! Pressione ENTER e tente novamente.\n")

        except Exception as e:
            input(f"{e}\nPressione ENTER e tente novamente.\n")