from questoes import *

if __name__ == "__main__":

    while True:
        try:
            opt = int(input("Escolha a questão para rodar:\n\n1- Questão 1\n2- Questão 2\n3- Questão 3\n0- Sair\n\nSua escolha: "))
            match(opt):
                case 1:
                    filepath = "data/Market_Basket_Optimisation.csv"
                    questao1(filepath, min_support=300, min_confidence=0.3)
                    input("\nPressione enter para escolher outra opção.")

                case 2:
                    df_result = questao2(n_samples=500, noise=0.06, eps=0.2, min_samples=5, random_state=23)
                    print(df_result['cluster'].value_counts())

                    input("\nPressione enter para escolher outra opção.")

                case 3:
                    df_clusters = questao3()
                    print(df_clusters['cluster'].value_counts())

                    input("\nPressione enter para escolher outra opção.")

                case 0:
                    print("\"O correr da vida embrulha tudo, a vida é assim:")
                    print("esquenta e esfria, aperta e dai afrouxa, sossega e depois desinquieta.")
                    print("O que ela quer da gente é coragem.\" João Guimarães Rosa")
                    print("\nSaindo...")
                    exit()
                case _:
                    input("Valor Inválido! Pressione ENTER e tente novamente.\n")

        except Exception as e:
            input(f"{e}\nPressione ENTER e tente novamente.\n")