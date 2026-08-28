print("--- Menu Ticketeria ---\n 1-ingresso inteira(R$ 30,00 ) \n 2-ingresso Meia entrada(R$ 15,00)\n 3-Combo Promoção(Ingresso com pipoca - R$ 45,00) \n ")

opc = int(input("Digite uma opção:"))
match opc:
    case "1":
      idade = int(input("Qual é sua idade?"))
      if idade < 18:
        print("voce precisa de um responsavel")
      else:
        print("Ingresso emitido!")  
    case 2:
      cart = input("Você têm carteira de estudante?").lower()
      if cart == "sim":
        print("Você paga meia.")
      elif cart == "nao":
        print("Você Nao paga meia.")
    case 3:
      print("O vouncher do combo promocional foi emitido")
    case _:
      print("Digite uma opção valida 1,2 ou 3")