import random
   
hp_heroi = random.randint(20,50)
hp_monster = random.randint(20,50)

print("--- MOTOR RPG ---\n1 - Atacar com Espada\n2 - Usar Poção de Cura\n3 - Exolorar o mundo\n")

opc = int(input("digite uma opçao 1,2 ou 3: "))
match opc:
    case 1:
        while hp_heroi > 0 and hp_monster > 0:
            