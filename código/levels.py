#Inicialização --------------------------------------------------------------------------------------------------------------
import pygame, random, math #bibliotecas
from classes import *
from telainicial import *

# Tela
pygame.init()
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duel Minigames")

# Cores e Fontes
WHITE, BLACK, RED, BLUE, GREEN, YELLOW, ORANGE = ((255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 165, 0))
font = pygame.font.SysFont('Arial', 30)
big_font = pygame.font.SysFont('Arial', 50)
clock = pygame.time.Clock()
FPS = 60
#--------------------------------------------------------------------------------------------------------------------Inicialização

#Funções --------------------------------------------------------------------------------------------------------------------
#função pra desenhar textos na tela
def draw_text(text, font, color, x, y, surface, centered=True):
    text_surface = font.render(text, True, color)
    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)


#Níveis -------------------------------------------------------------------------------------------------------------------
def level_1(player1, player2):
    #Define as posições dos obstaculos
    obstacles = [
        Obstacle(0, 0, 20, HEIGHT),
        Obstacle(0, 0, WIDTH, 20),
        Obstacle(WIDTH-20, 0, 20, HEIGHT),
        Obstacle(0, HEIGHT-20, WIDTH, 20),
        Obstacle(0, HEIGHT*0.6, WIDTH*0.35, 50),
        Obstacle(110, HEIGHT*0.79, WIDTH*0.32, 60),
        Obstacle(WIDTH*0.55, HEIGHT*0.45, 50, HEIGHT*0.40),
        Obstacle(WIDTH*0.18, HEIGHT*0.20, WIDTH*0.39, 60),
        Obstacle(WIDTH*0.34, 220, 50, HEIGHT*0.20),
        Obstacle(WIDTH*0.69, 100, WIDTH*0.20, HEIGHT*0.35),
        Obstacle(WIDTH*0.15, HEIGHT*0.40, 100, 90)]
    
    # Acha locais validos para spawnar inimigos
    valid_positions = []
    for x, y in [(100,100),(900,100),(200,300),(700,200),
                (300,400),(600,100),(100,600),(800,600),
                (400,700),(700,500)]:
        temp_rect = pygame.Rect(x, y, 25, 25)
        if not any(temp_rect.colliderect(o.rect) for o in obstacles):
            valid_positions.append((x, y))
    
    enemies = pygame.sprite.Group()
    enemies_to_spawn = [Enemy(*random.choice(valid_positions)) for _ in range(5)]
    enemy_spawn_timer = 3 * FPS
    
    # Posiciona os jogadores em locais aleatórios que não colidam com obstáculos
    for player in [player1, player2]:
        while True:
            player.rect.x = random.randint(0, WIDTH - player.rect.width)
            player.rect.y = random.randint(0, HEIGHT - player.rect.height)
            if not any(player.rect.colliderect(o.rect) for o in obstacles):
                break
    
    #Define o plano de fundo do nível
    FundoLevel1= pygame.image.load('Assets/Background/Fundo1.png').convert()
    FundoLevel1 = pygame.transform.scale(FundoLevel1, (WIDTH*1.09, HEIGHT*1.8))

    #Loop do nível
    running = True
    while running:
        #Desenha tela de fundo
        screen.fill(BLACK)
        screen.blit(FundoLevel1, (-WIDTH*0.03, -HEIGHT*0.5))

        #Recebe os inputs do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == player1.shoot_key:
                    player1.shoot()
                if event.key == player2.shoot_key:
                    player2.shoot()
        
        player1.update(obstacles)
        player2.update(obstacles)
        
        player1.update_bullets(obstacles, enemies, player2)
        player2.update_bullets(obstacles, enemies, player1)
        
        if enemy_spawn_timer > 0:
            enemy_spawn_timer -= 1
        elif enemies_to_spawn:
            enemies.add(enemies_to_spawn.pop())
            enemy_spawn_timer = 1 * FPS
        
        for enemy in enemies:
            enemy.update([player1, player2])
            enemy.shoot()
            enemy.update_bullets([player1, player2], obstacles)
        
        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)
        
        enemies.draw(screen)
        screen.blit(player1.image, player1.rect)
        screen.blit(player2.image, player2.rect)
        
        player1.draw_lives(screen)
        player2.draw_lives(screen)
        
        player1.bullets.draw(screen)
        player2.bullets.draw(screen)
        for enemy in enemies:
            enemy.bullets.draw(screen)
        
        #Desenha a pontuação dos jogadores
        draw_text(f"J1 : {player1_score}", font, BLUE, WIDTH*0.25, HEIGHT*0.02, screen)
        draw_text(f"J2 - {player2_score}", font, RED, WIDTH*0.75, HEIGHT*0.02, screen)
        
        #Acaba o nível se um dos jogadores perder todas as vidas
        if player1.lives <= 0 or player2.lives <= 0:
            running = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # Retorna o resultado do nível
    return 1 if player1.lives > 0 and player2.lives <= 0 else 2 if player2.lives > 0 and player1.lives <= 0 else 0



# Loop principal -----------------------------------------------------------------------------------------------------------------
def main():

    #Implementa a pontuação dos jogadores como variaveis globais
    global player1_score, player2_score
    player1_score = 0
    player2_score = 0

    #mostra a tela de início
    if not title_screen():
        return False
    
    #Define o jogador 1 dentro da classse Player
    player1_images = {
        "up": "Assets/Characters/Azulcima-1.png.png",
        "down": "Assets/Characters/Azulbaixo-1.png.png",
        "left": "Assets/Characters/Azulesquerda-1.png.png",
        "right": "Assets/Characters/Azuldireita-1.png.png"}
    player1 = Player(100, HEIGHT // 2, player1_images, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], pygame.K_SPACE)

    #Define o jogador 2 dentro da classse Player
    player2_images = {
        "up": "Assets/Characters/Vermelhocima-1.png.png",
        "down": "Assets/Characters/Vermelhobaixo-1.png.png",
        "left": "Assets/Characters/Vermelhoesquerda-1.png.png",
        "right": "Assets/Characters/Vermelhodireita-1.png.png"}
    player2 = Player(WIDTH - 130, HEIGHT // 2, player2_images, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], pygame.K_RETURN)
    
    #Define os níveis do jogo, reinicando as condições dos players e calculando a pontuação a cada level
    levels = [level_1]
    for level in levels:
        player1.lives = 3
        player2.lives = 3
        player1.bullets.empty()
        player2.bullets.empty()
        
        result = level(player1, player2)
        
        if result == 1:
            player1_score += 1
        elif result == 2:
            player2_score += 1
        
        pygame.time.delay(1000)

    pygame.quit()

#Chama a função do loop principal
if __name__ == "__main__":
    main()