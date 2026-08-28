import pygame

pygame.init()

janela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("RPG Py")

imagemfundo = pygame.image.load(
    "/Users/migueldasensi/infoaulas/logica/Python com frameworks/pygame/imgs/Fundo.png"
)

loop = True

while loop:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            loop = False

    janela.blit(imagemfundo, (0, 0))
    pygame.display.update()

pygame.quit()