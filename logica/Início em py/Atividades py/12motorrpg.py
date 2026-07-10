
hp_heroi = 50
possui_pocao = True
 
while True:
   
 print("--- MOTOR RPG ---\n1 - Atacar com Espada\n2 - Usar Poção de Cura\n3 - Fugir da Batalha\n")

 opc = int(input("digite uma opçao 1,2 ou 3: "))


 match opc:
     case 1:
         dado = int(input("digite um numero e 1 a 20: "))
         if dado > 12:
             print("Ataque certeiro! voce eu 15 de dano mo monstro")
         else:
             print("voce errou\n")
     case 2:
          if possui_pocao == True:
              print("\n++Poçao utilizada++\n")
              possui_pocao = False
          elif possui_pocao == False:
               print("\n---voce nao tem poçao para utilizar---\n")
               break
     case 3:
        print("voce fugiu da batalha com sucesso")
     case _:
        print("comando invalido!")
        break
        
    