import random
import time

print("=" * 40)
print("Bem vindo ao desafio do chefao")
print("=" * 40)
print()


#config inicial
hp_chefao = 100
turnos = 0

print(f"Um dragao apareceu! Hp do chefao : {hp_chefao}\n")   

#laço de repeticçao
#o jogo continua enquant o hp do chefaofor maipor que zero

# cargas iniciais da magia "bola de fogo"
boladefogo = 3

while hp_chefao > 0:
      turnos = turnos + 1  # ou turnos += 1 contador

      print(f"--- TURNO {turnos}---")

      print("escolha seu ataquee:")
      print("1 - Ataque rapido (espada)")
      print("2 - Magia de Fogo")

      opcao = input("digite o numero da sua açao:")

      #logica de ataque

      if opcao == "1":
            dano = random.randint(10,20)
            print(f"\n Voce desferiu um golpe de espada Dano:{dano}")
      elif opcao == "2":
            # Verifica se ainda tem cargas da bola de fogo
            if boladefogo > 0:
                  dano = random.randint(5,30)
                  boladefogo -= 1
                  print(f"\nVocê lançou uma bola de fogo! Dano: {dano} (restam {boladefogo})")
                  if boladefogo == 0:
                        print("Você usou todas as bolas de fogo.")
            else:
                  dano = 0
                  print("\nVocê não tem bolas de fogo restantes!")
           



      else:
            dano = 0
            print(f"\n VOce s atrapalhou nos comandos e errou o ataque Dano : 0")

            #atualizar  a vida do chefao (acumulador)
      hp_chefao = hp_chefao - dano

      # garantir  que a via  nao exiba  valores negativposs 
      if hp_chefao < 0:
            hp_chefao = 0

      print(f"HP restante do Chefão: {hp_chefao}")
      print("-" * 30)

    # Pausa dramática de 1.5 segundos para dar clima de jogo
      time.sleep(1.5)
      print()

#Fim do Laço / Tela de Vitória
print("🎉 " * 10)
print(f"VI TÓ RI A! O Dragão foi derrotado em {turnos} turnos!")
print("🎉 " * 10)


