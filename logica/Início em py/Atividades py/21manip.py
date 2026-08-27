
while True:
 nome = input("Qual é o nome do personagem?")
 classe = input("Qual é a sua classe?")

 print(f"Seu nome possui {len(nome)} carcateres")

 caracteresdomome = len(nome) 

 if caracteresdomome < 3:
  print("Nome muito pequeno")
 else:
  break