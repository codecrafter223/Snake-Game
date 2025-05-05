import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1000, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE GAME")
CLOCK = pygame.time.Clock()
BLOCK_SIZE = 20
FONT = pygame.font.SysFont("Arial", 25)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Función para inicializar variables
def inicializar_variables():
    snake_head_pos = [WIDTH // 2, HEIGHT // 2]
    snake_body_pos = [list(snake_head_pos)]
    direction = "UP"
    score = 0
    food_pos = generar_comida(snake_body_pos)
    return snake_head_pos, snake_body_pos, food_pos, direction, score

# Función para generar comida en una posición válida
def generar_comida(snake_body_pos):
    while True:
        food_pos = [
            random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
        ]
        if food_pos not in snake_body_pos:
            return food_pos

# Función para dibujar el puntaje
def draw_score(score):
    score_text = FONT.render(f"Puntaje: {score}", True, WHITE)
    SCREEN.blit(score_text, (10, 10))

# Función para dibujar la serpiente
def draw_snake(snake_body_pos):
    for i, segment in enumerate(snake_body_pos):
        if i == 0:  # Cabeza en verde
            pygame.draw.rect(SCREEN, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
        else:  # Cuerpo en blanco
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

# Función para dibujar la comida
def draw_food(food_pos):
    pygame.draw.rect(SCREEN, BLUE, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

# Función para mover la serpiente
def snake_move(snake_head_pos, snake_body_pos, food_pos, direction):
    if direction == "UP":
        snake_head_pos[1] -= BLOCK_SIZE
    elif direction == "DOWN":
        snake_head_pos[1] += BLOCK_SIZE
    elif direction == "LEFT":
        snake_head_pos[0] -= BLOCK_SIZE
    elif direction == "RIGHT":
        snake_head_pos[0] += BLOCK_SIZE

    snake_body_pos.insert(0, list(snake_head_pos))
    
    if snake_head_pos == food_pos:
        return True  # La serpiente crece
    else:
        snake_body_pos.pop()
        return False

# Función para detectar colisiones
def detectar_colisiones(snake_head_pos, snake_body_pos):
    if (
        snake_head_pos[0] < 0 or snake_head_pos[0] >= WIDTH or 
        snake_head_pos[1] < 0 or snake_head_pos[1] >= HEIGHT
    ):
        return True
    if snake_head_pos in snake_body_pos[1:]:
        return True
    return False

# Función para la pantalla de "Game Over"
def game_over_screen(score):
    SCREEN.fill(BLACK)
    game_over_text = FONT.render(f"¡Game Over! Puntaje: {score}", True, RED)
    restart_text = FONT.render("Presiona R para reiniciar o Q para salir", True, WHITE)
    SCREEN.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
    SCREEN.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 20))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

# Bucle principal del juego
while True:
    jugando = True
    snake_head_pos, snake_body_pos, food_pos, direction, score = inicializar_variables()

    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # Mover la serpiente y verificar si come
        if snake_move(snake_head_pos, snake_body_pos, food_pos, direction):
            food_pos = generar_comida(snake_body_pos)
            score += 1

        # Detectar colisiones
        if detectar_colisiones(snake_head_pos, snake_body_pos):
            jugando = False

        # Dibujar todo en la pantalla
        SCREEN.fill(BLACK)
        draw_score(score)
        draw_snake(snake_body_pos)
        draw_food(food_pos)
        pygame.display.flip()

        # Velocidad dinámica (aumenta con el puntaje)
        CLOCK.tick(10 + score // 5)

    # Mostrar pantalla de "Game Over" y decidir si reiniciar
    if not game_over_screen(score):
        break

pygame.quit()