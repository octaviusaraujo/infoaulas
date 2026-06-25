print("--Painel da nave--\n 1-Verificar combustivel\n 2-Ativar escudo de protecão \n 3- Ativar modo de auto destruicão")
escolha = str(input("Digite uma opcão:"))
while True:
    match escolha:
     case "1":
        combustivel = str(input("qual é a porcentagem do tanque?"))
        if combustivel < 20:
            print("Baixo combustivel!!")
        else:
            print("combustivel alto")
     case "2":
        mtr = input("Há meteoros por perto S/n?")
        if mtr == 's':
            print("Escudo ativado")
        else:
            print("Ok, os escudos nao são necessarios!")
            break
     case "3":
        print("MODO DE DESTRUICÃO ATIVADO, DESTRUICÃO EM 3,2,1...")
        break
     case "_":
        print("")