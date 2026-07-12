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
         print("1-Novo Jogo\n2-Continuar\n3-Sair")
         escolha = int(input("Selecione:"))
         match escolha:
                case 1:
                    print("\niniciando novo jogo...\n")
                    return novo_jogo()
                
                case 2:
                      print("Continuando o jogo passado...")
                case 3:
                      print("Saindo...")
                      game_over()
                case _:
                      print("escolha 1,2 ou 3")
         
def novo_jogo():
      Hp = 100 
      level = random.randint(1,10)
      forca = random.randint(0,10)
      exp = random.randint(0,50)
      inventario = []
      status = ['vivo', 'morto']
      estado = random.choice(status)
      
      
      print("Crie seu perosnagem:")
      jogador = str(input("digite o nome do seu personagem:"))
      if estado == 'vivo':
            print("\nSeja Bem vindo ao mundo",jogador, "Vamos ao jogo\n")
            print("\nSeus stats sao:" "\nHp:",Hp,"\nLevel:",level,"\nForca:",forca,"\nExp:",exp,"\n ------------")
            escolhas_no_jogo()
      else:
            mensagens_de_morte = ['\nSua mae foi engolida por uma jacare enquanto gestava de voce,voce nao nasceu\n','\nsua mae morreu de fome antes de voce nascer.\n','\nsua mae caiu num rio e morreu,voce nao nasceu.\n','\nVoce nasceu! porem a parteira deixou voce cair durante o parto e vocce morreu.\n']
            print(random.choice(mensagens_de_morte))
            menu_do_jogo()

      return Hp,level,forca,exp,inventario,estado

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
      exit(0)
      
def escolhas_no_jogo():
      print("1-lutar\n2-Explorar\n3-inventario")
      escolha = int(input("Escolha: ")) 
      match escolha :
            case 1:
                  lutar()
            case 2:
                  explorar()
            case 3:
                  print(inventario)

def lutar():
      print("sistema de lutas")
      
def explorar():
      print("Sistema de exploracao..")                 
                  
            
mostrar_arte()
Hp, level, forca, exp, inventario, estado = menu_do_jogo()
monstro_sorteado = sortear_monstro(level)
print(monstro_sorteado)
      



