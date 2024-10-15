import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mon Jeu 2D")

# Chargement d'un sprite
player_image = pygame.image.load('player.png')
player_rect = player_image.get_rect()
player_rect.center = (400, 300)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des mouvements
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_UP]:
        player_rect.y -= 5
    if keys[pygame.K_DOWN]:
        player_rect.y += 5

    # Dessiner le fond et le joueur
    screen.fill((0, 0, 0))  # Fond noir
    screen.blit(player_image, player_rect)

    # Actualiser l'affichage
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # 60 FPS

pygame.quit()
sys.exit()
