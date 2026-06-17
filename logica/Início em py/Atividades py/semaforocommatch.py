print("--semaforo--")
cor = input("qual é a cor do semaforo?")
match cor:
        case "verde" | "Verde" :
         print("pode passar")
        case "amarelo" | "Amarelo":
         print("Atencao")
        case "vermelho" | "Vermelho":
         print("nao passe")
        case _:
         print("digite uma cor(verde vermelho ou amarelo)")
      
        