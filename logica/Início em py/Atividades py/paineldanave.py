print("--Painel da nave--\n 1-Verificar combustivel\n 2-Ativar escudo de protecão \n 3-\Ativar modo de auto destruicão")
escolha = int(input("Digite uma opcão:"))
while True:
    match escolha:
     case 1:
        combustivel = int(input("qual é a porcentagem do tanque?"))
        if combustivel < 20:
            print("Baixo combustivel!!")
        else:
            print("Nivel de combustivel seguro")
            break
     case 2:
        mtr = str(input("Há meteoros por perto S ou n?")).lower()
        if mtr == 's':
            print("Escudo ativado")
        elif mtr == 'n':
            print("Ok, os escudos nao são necessarios!")
            break
        else:
            print('Digite S/n')
            break
     case 3:
        print("MODO DE DESTRUICÃO ATIVADO, DESTRUICÃO EM 3,2,1...")
        break
     case "_":
        print("digite 1,2 ou 3")