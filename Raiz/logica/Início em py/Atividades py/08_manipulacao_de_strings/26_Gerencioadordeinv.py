itens = ["Poçâo","Escudo","Vazio","Vazio","Chave"]

escolha = input(f"Os itens disponiveis sâo {itens} adicione o que deseja adicionar ao inventario:")

posicao = int(input("Digite a posiçao do novo item:"))

if itens[posicao] != "Vazio":
    desicao = input(f"o item {itens[posicao]} ja esta ocupando esse slot, deseja substituir S/n? ").lower()
    if desicao == "s":
        print(f"O item {itens[posicao]} foi substituido com sucesso")
    elif desicao == "n":
        print("O item nao foi substituido") 

else:
    itens[posicao] = escolha
    print("O item foi adicionado com sucesso!!")

for indice in range (0, len(itens),1):
    print(itens[indice])












