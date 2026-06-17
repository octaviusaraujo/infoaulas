print("---dia util?---")
dia = input("qual é o dia da semana?")
match dia:
    case "segunda" | "terca" | "quarta" | "quinta" | "sexta":
        print("dia util")
    case "sabado" | "domingo":
        print("dia nao util")
    case _:
        print("digite um dia da semana valido")