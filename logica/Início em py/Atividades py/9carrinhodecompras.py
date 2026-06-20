print("--- Carrinho de Compras ---")

compras = []

while True:
    resposta = input("Deseja adicionar algo ao carrinho? (S/n) ")
    match resposta:
        case "S" | 's':
            produto = input("O que quer adicionar? ")
            compras.append(produto)
        case "n" | "N":
            break
        case _:
            print("Digite apenas S ou n.")
print("Carrinho final:", compras)

while True:
    resposta = input("Deseja remover algo do carrinho? (S/n) ")
    match resposta:
        case "S" | "s":
            produto = input("O que quer remover? ")
            compras.remove(produto)
        case "n" | "N":
            break
        case _:
            print("Digite apenas S ou n.")

print("Carrinho final:", compras)