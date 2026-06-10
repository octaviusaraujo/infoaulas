esc = 0
HP = int(input("digite a vida do seu personagem:"))

if HP == 30:
	esc = esc + 20

if HP <= 0:
	print("game over")
else:
	print("jogo continua")
