import random

danototal = 0
qntgolpes = int(input("quantos golpes voce quer deferir?"))

for qntgolpes in  range(qntgolpes,0, -1):
   
    dano = random.randint(5,15)
    print(f"golpe N {qntgolpes} o dano foi de {dano}")
    danototal = danototal+dano

print(f"o dano total foi de {danototal}")
