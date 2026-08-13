import random

def mostrar_arte():
         arte = r"""
         .:'                                  `:.                                   
        ::'                                    `::                                   
       :: :.                                 .: ::                                  
        `:. `:.             .             .:'  .:'                                   
         `::. `::           !           ::' .::'                                     
             `::.`::.    .' ! `.    .::'.::'                                         
               `:.  `::::'':!:``::::'   ::'                                          
               :'*:::.  .:' ! `:.  .:::*`:                                           
              :: HHH::.   ` ! '   .::HHH ::                                          
             ::: `H TH::.  `!'  .::HT H' :::                                         
             ::..  `THHH:`:   :':HHHT'  ..::                                         
             `::      `T: `. .' :T'      ::'                                         
               `:. .   :         :   . .:'                                           
                 `::'               `::'                                             
                   :'  .`.  .  .'.  `:                                               
                   :' ::.       .:: `:                                               
                   :' `:::     :::' `:                                               
                    `.  ``     ''  .'                                                
                     :`...........':                                                 
                     ` :`.     .': '                                                 
                      `:  `"""'  :'
     


         print(arte)
         print("\n                 Seja Bem vindo ao sensipg")


def menu_do_jogo():
      while True:
            mostrar_arte()
            print("1-Novo Jogo\n2-Continuar\n3-Sair")
            escolha = input("Selecione:")
            match escolha:
                  case "1":
                        print("\niniciando novo jogo...\n")
                        return novo_jogo()
                  case "2":
                        print("Continuando o jogo passado...")
                  case "3":
                        sair_do_jogo()
                        exit(0)
                  case _:
                        print("escolha 1,2 ou 3")
         
def novo_jogo():
      Hp = 100 
      level = random.randint(1,10)
      forca = random.randint(1,10)
      exp = random.randint(0,50)
      mochila = []
      estado = "vivo"
      
      
      print("Crie seu perosnagem:")
      jogador = str(input("digite o nome do seu personagem:"))
      if estado == 'vivo':
            print("\nSeja Bem vindo ao mundo",jogador, "Vamos ao jogo\n")
            print("\nSeus stats sao:" "\nHp:",Hp,"\nLevel:",level,"\nForca:",forca,"\nExp:",exp,"\n ------------")
            Hp, level, forca, exp, mochila, estado = escolhas_no_jogo(jogador, Hp, level, forca, exp, mochila, estado)
      else:
            mensagens_de_morte = ['\nSua mae foi engolida por uma jacare enquanto gestava de voce,voce nao nasceu\n','\nsua mae morreu de fome antes de voce nascer.\n','\nsua mae caiu num rio e morreu,voce nao nasceu.\n','\nVoce nasceu! porem a parteira deixou voce cair durante o parto e vocce morreu.\n']
            print(random.choice(mensagens_de_morte))
            return menu_do_jogo()

      return Hp,level,forca,exp,mochila,estado

def sortear_monstro(level):
    rato = ['Rato',5,1,5]
    slime = ["slime", 10, 2, 10]
    goblin = ["goblin", 20, 4, 20]
    troll = ["troll", 40, 8, 40]
    orc = ["orc", 80, 16, 80]
    mumia = ["múmia", 160, 32, 160]
    quimera = ["quimera", 320, 64, 320]
    dragao = ["dragão", 1000, 100, 1000]

    if level < 5:
            monstro_sorteado = random.choice([slime,rato,goblin])
    elif level < 10:
          monstro_sorteado = random.choice([troll,orc,mumia])
    else:
            monstro_sorteado = random.choice([quimera,dragao])

    return monstro_sorteado
def game_over():
      print("O jogo terminou")
      print(" obrigado por jogar")
      ques = input("quer jogar novamente? sim/nao:")
      match ques:
            case "sim":
                  return novo_jogo()
            case "nao":
                  return menu_do_jogo()
            case _:     
                   exit(0)

def sair_do_jogo():
      print("Tchau!!")
     
      
def escolhas_no_jogo(jogador, Hp, level, forca, exp, mochila, estado):
      while estado == "vivo":
            print("1-lutar\n2-Explorar\n3-inventario\n4-sair")
            escolha = input("Escolha: ") 
            match escolha:
                  case "1":
                        monstro_sorteado = sortear_monstro(level)
                        print(f"Voce encontrou um {monstro_sorteado[0]}")
                        monstro_hp, monstro_vivo = atacar(jogador, forca, monstro_sorteado[0], monstro_sorteado[1], monstro_sorteado[2])
                        if not monstro_vivo:
                              exp = exp + monstro_sorteado[3]
                              print(f"Voce ganhou {monstro_sorteado[3]} de exp")
                  case "2":
                        explorar()
                  case "3":
                        mostrar_inventario(mochila)
                  case "4":
                        sair_do_jogo()
                        return Hp, level, forca, exp, mochila, estado
                  case _:
                        print("escolha 1, 2, 3 ou 4")

      return Hp, level, forca, exp, mochila, estado

def atacar(atacante_nome,atacante_forca,defensor_nome,defensor_hp,defensor_forca):
      defensor_sorte = random.randint(0,20)
      atacante_sorte = random.randint(0,20 )
      
      if atacante_sorte == 20:
            print(f" {atacante_nome} acertou um ataque critico")
      elif atacante_sorte > 0:
            print(f" {atacante_nome} acertou um golpe")
      else:
            print(f" {atacante_nome} errou feio o golpe")

      dano = atacante_sorte * atacante_forca - defensor_forca * defensor_sorte
      
      if dano > 0:
            print(f" {atacante_nome} deu um dano de {dano}")
            defensor_hp = defensor_hp - dano
            print(f"agora  {defensor_nome} tem {defensor_hp} de hp")
            if defensor_hp > 0:
                  print("a luta continua")
            else:
                  print(f"o {defensor_nome} foi derrotado") 
                  return 0, False

      else:
            print(f"o {atacante_nome} nao causou dano")
      if defensor_hp <= 0:
            print(f"o {defensor_nome} morreu")
            return 0, False
      
def calcular_level(jogador_lv,jogador_exp,jogador_hp,jogafor_forca,exp_monstro):


      

      
def explorar():
      print("Sistema de exploracao..")        
def mostrar_inventario(mochila):
      print(mochila)         
                  
            

if __name__ == "__main__":
      Hp, level, forca, exp, mochila, estado = menu_do_jogo()
      
