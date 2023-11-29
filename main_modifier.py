# Importer les modules nécessaires
import pygame
import random
import sys

# Initialiser pygame
pygame.init()

# Définir les constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.3
PIPE_GAP = 150
PIPE_SPEED = 5
BIRD_SIZE = 50
BIRD_JUMP = 8
FONT = pygame.font.SysFont('Arial', 32)

# Créer la fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Charger les images
bird = pygame.image.load('bird.png')
bird = pygame.transform.scale(bird, (BIRD_SIZE, BIRD_SIZE))
pipe = pygame.image.load('pipe.png')
pipe = pygame.transform.scale(pipe, (100, SCREEN_HEIGHT))
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Définir les variables
bird_x = 100
bird_y = 300
bird_speed = 0
pipes = []
score = 0
game_over = False

# Créer une fonction pour afficher le score
def show_score():
    texte = FONT.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(texte, (10, 10))

# Créer une fonction pour afficher le message de fin de partie
def show_game_over():
    if game_over:
        text = FONT.render('Game Over', True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

# Créer une fonction pour ajouter un nouveau tuyau
def add_pipe():
    # Ajouter un nouveau tuyau uniquement si la distance au dernier tuyau est suffisante
    if not pipes or pipes[-1]['x'] < SCREEN_WIDTH - 300:
        # Choisir une hauteur aléatoire pour le tuyau du haut
        top_height = random.randint(50, SCREEN_HEIGHT - 50 - PIPE_GAP)
        # Calculer la hauteur du tuyau du bas
        bottom_height = SCREEN_HEIGHT - top_height - PIPE_GAP
        # Créer un dictionnaire pour stocker les informations du tuyau
        pipe_info = {'x': SCREEN_WIDTH, 'top_height': top_height, 'bottom_height': bottom_height}
        # Ajouter le dictionnaire à la liste des tuyaux
        pipes.append(pipe_info)

# Créer une fonction pour mettre à jour les tuyaux
def update_pipes():
    global pipes, score, game_over
    # Parcourir la liste des tuyaux
    for pipe_info in pipes:
        # Déplacer le tuyau vers la gauche
        pipe_info['x'] -= PIPE_SPEED
        # Vérifier si le tuyau est sorti de l'écran
        if pipe_info['x'] < -100:
            # Supprimer le tuyau de la liste
            pipes.remove(pipe_info)
            # Augmenter le score de 1
            score += 1
    # Vérifier si le joueur a perdu
    for pipe_info in pipes:
        if (
            bird_x < pipe_info['x'] + 100
            and bird_x + BIRD_SIZE > pipe_info['x']
            and (bird_y < pipe_info['top_height'] or bird_y + BIRD_SIZE > SCREEN_HEIGHT - pipe_info['bottom_height'])
        ):
            # Mettre fin à la partie
            game_over = True
            # Réinitialiser le jeu après un court délai
            pygame.time.delay(1000)
            reset_game()

# Créer une fonction pour afficher les tuyaux
def show_pipes():
    global pipes
    # Parcourir la liste des tuyaux
    for pipe_info in pipes:
        # Afficher le tuyau du haut
        screen.blit(pipe, (pipe_info['x'], 0), (0, 0, 100, pipe_info['top_height']))
        # Afficher le tuyau du bas
        screen.blit(pipe, (pipe_info['x'], SCREEN_HEIGHT - pipe_info['bottom_height']), (0, SCREEN_HEIGHT - pipe_info['bottom_height'], 100, pipe_info['bottom_height']))

# Créer une fonction pour réinitialiser le jeu
def reset_game():
    global bird_x, bird_y, bird_speed, pipes, score, game_over
    # Remettre l'oiseau à sa position initiale
    bird_x = 100
    bird_y = 300
    bird_speed = 0
    # Vider la liste des tuyaux
    pipes = []
    # Remettre le score à zéro
    score = 0
    # Remettre la fin de partie à False
    game_over = False

# Créer une boucle principale
while True:
    # Gérer les événements
    for event in pygame.event.get():
        # Si l'utilisateur ferme la fenêtre
        if event.type == pygame.QUIT:
            # Quitter le jeu
            pygame.quit()
            sys.exit()
        # Si l'utilisateur appuie sur une touche
        if event.type == pygame.KEYDOWN:
            # Si la touche est la barre d'espace
            if event.key == pygame.K_SPACE:
                # Faire sauter l'oiseau
                bird_speed = -BIRD_JUMP
            # Si la touche est la touche R
            if event.key == pygame.K_r:
                # Réinitialiser le jeu
                reset_game()

    # Afficher le fond d'écran
    screen.blit(background, (0, 0))
    # Afficher l'oiseau
    screen.blit(bird, (bird_x, bird_y))
    # Mettre à jour la vitesse
    bird_speed += GRAVITY
    # Mettre à jour la position
    bird_y += bird_speed
    # Vérifier si l'oiseau sort de l'écran
    if bird_y < 0 or bird_y + BIRD_SIZE > SCREEN_HEIGHT:
        # Mettre fin à la partie
        game_over = True
        # Réinitialiser le jeu après un court délai
        pygame.time.delay(1000)
        reset_game()
    # Ajouter un nouveau tuyau toutes les 90 frames
    if pygame.time.get_ticks() % 90 == 0:
        add_pipe()
    # Mettre à jour les tuyaux
    update_pipes()
    # Afficher les tuyaux
    show_pipes()
    # Afficher le score
    show_score()
    # Afficher le message de fin de partie
    show_game_over()
    # Rafraîchir l'écran
    pygame.display.flip()
    # Limiter le nombre d'images par seconde
    clock.tick(FPS)
