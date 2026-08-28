#1.
#Filtro de Chat Anti-Toxidade (replace e lower):
#Crie um programa que lê a mensagem de um jogador no chat. O programa deve transformar tudo em letras minúsculas (para padronizar) e, se encontrar a palavra "noob", deve substituí-la por "***" (censura).
#Exemplo de entrada: "Você é muito NOOB!"
#Saída esperada: "você é muito ***!"


msg = input("envie uma mensagem: ").lower()

msgmoderada = msg.replace("noob","te amo")

print(msgmoderada)