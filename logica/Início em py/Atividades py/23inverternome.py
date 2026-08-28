nome = input("qual é seu nome? ")

inverso = ""
for i in range(len(nome) - 1, -1, -1):
	inverso += nome[i]

print("Nome invertido:", inverso)

