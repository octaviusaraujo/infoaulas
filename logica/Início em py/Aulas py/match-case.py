nome = input(str("Qual é seu nome?"))

match nome:
    case "miguel" :
        print("oi", nome)
    case _:
        print("sei nem quem é tu")