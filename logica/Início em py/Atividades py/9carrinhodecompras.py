print("--- Carrinho de Compras ---")

compras = []

while True:
    resposta = input("Deseja adicionar algo ao carrinho? (S/n) ")

    match resposta:
        case "S":
            produto = input("O que quer adicionar? ")
            compras.append(produto)

        case "n":
            break

        case _:
            print("Digite apenas S ou n.")

print("Carrinho final:", compras)