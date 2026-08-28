#2. O Processador de Comandos (.split ef-strings):
#Em jogos de texto (MUDs), o jogador digita ações. Peça para o aluno capturar um comando duplo no input, como "comprar poção".
#O programa deve usar o .split() para separar a ação ("comprar") do item ("poção"). Em seguida, usando uma f-string, o programa deve imprimir de forma bonitinha:
#"Ação reconhecida: Você escolheu {acao} o item {item}."


compra = input("Oque seseja fazer?")

resultado = compra.split()

acao = resultado[0]
item = resultado[1]

print(f"Voce escolheu {acao} o item {item}" )