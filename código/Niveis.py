#Inicialização --------------------------------------------------------------------------------------------------------------
import pygame, random, math, classes, Functions, LoopPrincipal #bibliotecas
# Tela
from Functions import draw_text
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


def level_1(player1, player2):
    #Define as posições dos obstaculos
    obstacles = [
        classes.Obstacle(0, 0, 20, HEIGHT),
        classes.Obstacle(0, 0, WIDTH, 20),
        classes.Obstacle(WIDTH-20, 0, 20, HEIGHT),
        classes.Obstacle(0, HEIGHT-20, WIDTH, 20),
        classes.Obstacle(0, HEIGHT*0.6, WIDTH*0.35, 50),
        classes.Obstacle(110, HEIGHT*0.79, WIDTH*0.32, 60),
        classes.Obstacle(WIDTH*0.55, HEIGHT*0.45, 50, HEIGHT*0.40),
        classes.Obstacle(WIDTH*0.18, HEIGHT*0.20, WIDTH*0.39, 60),
        classes.Obstacle(WIDTH*0.34, 220, 50, HEIGHT*0.20),
        classes.Obstacle(WIDTH*0.69, 100, WIDTH*0.20, HEIGHT*0.35),
        classes.Obstacle(WIDTH*0.15, HEIGHT*0.40, 100, 90)]
    
    # Acha locais validos para spawnar inimigos
    valid_positions = []
    for x, y in [(100,100),(900,100),(200,300),(700,200),
                (300,400),(600,100),(100,600),(800,600),
                (400,700),(700,500)]:
        temp_rect = pygame.Rect(x, y, 25, 25)
        if not any(temp_rect.colliderect(o.rect) for o in obstacles):
            valid_positions.append((x, y))
    
    enemies = pygame.sprite.Group()
    enemies_to_spawn = [classes.Enemy(*random.choice(valid_positions)) for _ in range(5)]
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
        Functions.draw_text(f"J1 : {player1.score}", font, BLUE, WIDTH*0.25, HEIGHT*0.02, screen)
        Functions.draw_text(f"J2 - {player2.score}", font, RED, WIDTH*0.75, HEIGHT*0.02, screen)
        
        #Acaba o nível se um dos jogadores perder todas as vidas
        if player1.lives <= 0 or player2.lives <= 0:
            running = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # Retorna o resultado do nível
    return 1 if player1.lives > 0 and player2.lives <= 0 else 2 if player2.lives > 0 and player1.lives <= 0 else 0

def level_2(player1, player2):
    #Define a posição e direção inicial dos jogadores
    player1.rect.x = WIDTH // 2 - player1.rect.width // 2
    player1.rect.y = HEIGHT - 50
    player1.direction = "up"
    player1.image = player1.images["up"]
    player2.rect.x = WIDTH // 2 - player2.rect.width // 2
    player2.rect.y = 20
    player2.direction = "down"
    player2.image = player2.images["down"]
    
    #Define o objeto boss da classe Boss
    boss = classes.Boss()
    
    #Plano de Fundo
    FundoLevel2= pygame.image.load('Assets/Background/Fundo1.png').convert()
    FundoLevel2 = pygame.transform.scale(FundoLevel2, (WIDTH*1.09, HEIGHT*1.8))

    #Loop do nível
    running = True
    while running:
        #Desenha a tela de fundo
        screen.fill(BLACK)
        screen.blit(FundoLevel2, (-WIDTH*0.03, -HEIGHT*0.5))
        
        #Input dos jogadores
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == player1.shoot_key:
                    player1.shoot()
                if event.key == player2.shoot_key:
                    player2.shoot()
        
        keys = pygame.key.get_pressed()
        
        #Define que os jogadores só andam pra direita e esquerda
        if keys[player1.controls[2]]: 
            player1.rect.x = max(0, player1.rect.x - player1.speed)
        if keys[player1.controls[3]]:  
            player1.rect.x = min(WIDTH - player1.rect.width, player1.rect.x + player1.speed)
        if keys[player2.controls[2]]:  
            player2.rect.x = max(0, player2.rect.x - player2.speed)
        if keys[player2.controls[3]]: 
            player2.rect.x = min(WIDTH - player2.rect.width, player2.rect.x + player2.speed)
        
        player1.update_bullets([], None, player2)
        player2.update_bullets([], None, player1)
        
        for bullet in player1.bullets:
            if bullet.rect.colliderect(boss.rect):
                boss.take_hit()
                bullet.kill()
        
        for bullet in player2.bullets:
            if bullet.rect.colliderect(boss.rect):
                boss.take_hit()
                bullet.kill()
        
        boss.update()
        boss.shoot()
        boss.update_bullets([player1, player2])
        
        screen.blit(player1.image, player1.rect)
        screen.blit(player2.image, player2.rect)
        screen.blit(boss.image, boss.rect)
        
        player1.draw_lives(screen)
        player2.draw_lives(screen)
        boss.draw_health(screen)

        player1.bullets.draw(screen)
        player2.bullets.draw(screen)
        boss.bullets.draw(screen)
        
        #Desenha a pontuação geral
        Functions.draw_text(f"J1 : {player1.score}", font, BLUE, WIDTH*0.25, HEIGHT*0.02, screen)
        Functions.draw_text(f"J2 - {player2.score}", font, RED, WIDTH*0.75, HEIGHT*0.02, screen)
        
        #Acaba o nível se um dos jogadores perder todas as vidas ou se o boss for derrotado
        if player1.lives <= 0 or player2.lives <= 0 or boss.health <= 0:
            running = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # Retorna o resultado do nível
    if player1.lives > 0 and player2.lives <= 0:
        return 1
    elif player2.lives > 0 and player1.lives <= 0:
        return 2
    else:
        return 1 if player1.lives > player2.lives else 2 if player2.lives > player1.lives else 0

def level_3(player1, player2):
    # Posição dos jogadores e direção inicial
    player1.rect.x = WIDTH // 4 - player1.rect.width // 2
    player1.rect.y = HEIGHT // 2 - player1.rect.height // 2
    player1.direction = "right"
    player1.image = player1.images["right"]
    player2.rect.x = 3 * WIDTH // 4 - player2.rect.width // 2
    player2.rect.y = HEIGHT // 2 - player2.rect.height // 2
    player2.direction = "left"
    player2.image = player2.images["left"]

    barrels = pygame.sprite.Group()
    barrel_spawn_timer = 0.1 * FPS 
    max_barrels = 100

    #Plano de Fundo
    FundoLevel3 = pygame.image.load('Assets/Background/fundodeserto.png').convert()
    FundoLevel3 = pygame.transform.scale(FundoLevel3, (WIDTH * 1.09, HEIGHT * 1.7))

    # Loop do nível 3
    running = True
    while running:
        # Desenha a tela de fundo
        screen.fill(BLACK)
        screen.blit(FundoLevel3, (-WIDTH * 0.03, -HEIGHT * 0.4))
        
        #Se apertam o botão de fechar, o nivel acaba em empata e passa pro próximo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            
        #Atualiza os jogadores
        player1.update([])
        player2.update([])

        # Spawna os barris
        if barrel_spawn_timer <= 0 and len(barrels) < max_barrels:
            edge = random.randint(0, 3)
            if edge == 0:
                x = random.randint(0, WIDTH - 30)
                y = 0
            elif edge == 1: 
                x = random.randint(0, WIDTH - 30)
                y = HEIGHT - 30
            elif edge == 2:
                x = 0
                y = random.randint(0, HEIGHT - 30)
            else:
                x = WIDTH - 30
                y = random.randint(0, HEIGHT - 30)

            #Vai em direção ao jogador mais próximo ao spawnar
            closest_player = min([player1, player2], key=lambda p: math.hypot(
                x - p.rect.centerx, y - p.rect.centery))
            dx = closest_player.rect.centerx - x
            dy = closest_player.rect.centery - y
            dist = max(1, math.hypot(dx, dy))
            dx, dy = dx / dist, dy / dist

            barrels.add(Barrel(x, y, dx, dy))
            barrel_spawn_timer = 0.8 * FPS
        else:
            barrel_spawn_timer -= 1

        # Atualiza os barris
        barrels.update()

        #Checa colisão com jogadores
        for block in barrels:
            if block.rect.colliderect(player1.rect):
                pygame.mixer.Sound('Assets/Sounds/player_hit.wav').play()
                player1.lives -= 1
                block.kill()
            if block.rect.colliderect(player2.rect):
                pygame.mixer.Sound('Assets/Sounds/player_hit.wav').play()
                player2.lives -= 1
                block.kill()

        screen.blit(player1.image, player1.rect)
        screen.blit(player2.image, player2.rect)
        
        player1.draw_lives(screen)
        player2.draw_lives(screen)
        
        barrels.draw(screen)

        draw_text(f"J1 : {player1.score}", font, BLUE, WIDTH*0.25, HEIGHT*0.02, screen)
        draw_text(f"J2 - {player2.score}", font, RED, WIDTH*0.75, HEIGHT*0.02, screen)
        
        if player1.lives <= 0 or player2.lives <= 0:
            running = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return 1 if player2.lives <= 0 else 2 if player1.lives <= 0 else 0

def level_4(player1, player2):
    #Posição dos jogadores e direção inicial
    player1.rect.x = WIDTH // 4 - player1.rect.width // 2
    player1.rect.y = HEIGHT // 2 - player1.rect.height // 2
    player1.direction = "right"
    player1.image = player1.images["right"]
    player2.rect.x = 3 * WIDTH // 4 - player2.rect.width // 2
    player2.rect.y = HEIGHT // 2 - player2.rect.height // 2
    player2.direction = "left"
    player2.image = player2.images["left"]
    
    square_size = 50
    square = pygame.Rect(WIDTH*0.5 - square_size*1.7, HEIGHT*0.5 - square_size*3.5, square_size, square_size)
    square_color = RED
    square_change_time = random.randint(2, 4) * FPS
    square_timer = 0
    can_shoot = False#Não pode atirar até o farol ficar verde
    winner = 0
    shot_fired = False#Não pode atirar até o farol ficar verde
    
    #Define a imagem do farol verde e vermelho
    green_square = pygame.image.load('Assets/Objetos/farolverde-1.png.png').convert_alpha()
    green_square = pygame.transform.scale(green_square, (150, 150))
    red_square = pygame.image.load('Assets/Objetos/farolvermelho-1.png.png').convert_alpha()
    red_square = pygame.transform.scale(red_square, (150, 150))

    #Plano de fundo
    FundoLevel4 = pygame.image.load('Assets/Background/fundodeserto.png').convert()
    FundoLevel4 = pygame.transform.scale(FundoLevel4, (WIDTH*1.09, HEIGHT*1.7))

    #Loop do nível 4
    running = True
    while running:
        #Desenha a tela de fundo
        screen.fill(BLACK)
        screen.blit(FundoLevel4, (-WIDTH*0.03, -HEIGHT*0.4))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            
            if can_shoot and not shot_fired and event.type == pygame.KEYDOWN:
                if event.key == player1.shoot_key:
                    player1.shoot()
                    shot_fired = True
                
                if event.key == player2.shoot_key:
                    player2.shoot()
                    shot_fired = True
        
        square_timer += 1
        if square_timer >= square_change_time:
            #Altera o farol vermelho pelo verde e permite atirar
            if square_color == RED:
                square_color = GREEN
                can_shoot = True
                shot_fired = False
                square_change_time = 1 * FPS
            #Altera o farol verde pelo vermelho e não permite atirar
            else:
                square_color = RED
                can_shoot = False
                square_change_time = random.randint(2, 4) * FPS
            square_timer = 0
        
        #Atualiza os tiros
        player1.update_bullets([], None, player2)
        player2.update_bullets([], None, player1)
        
        #Checa colisão dos tiros com os jogadores
        if shot_fired:
            for bullet in player1.bullets:
                if bullet.rect.colliderect(player2.rect):
                    winner = 1
                    running = False
            
            for bullet in player2.bullets:
                if bullet.rect.colliderect(player1.rect):
                    winner = 2
                    running = False
        
        if player1.lives <= 0 or player2.lives <= 0:
            running = False
        
        #Desenha os jogadores e tiros
        screen.blit(player1.image, player1.rect)
        screen.blit(player2.image, player2.rect)
        player1.bullets.draw(screen)
        player2.bullets.draw(screen)
        
        player1.draw_lives(screen)
        player2.draw_lives(screen)
        
        #Desenha os faróis
        if square_color == GREEN:
            pygame.mixer.Sound('Assets/Sounds/hit.wav').play()#som se o farol ficar verde
            screen.blit(green_square, square)
        else:
            screen.blit(red_square, square)
        
        if can_shoot and not shot_fired:
            draw_text("ATIRE AGORA!", font, WHITE, WIDTH//2, HEIGHT//2 + 70, screen)
        
        draw_text(f"J1 : {player1.score}", font, BLUE, WIDTH*0.25, HEIGHT*0.02, screen)
        draw_text(f"J2 - {player2.score}", font, RED, WIDTH*0.75, HEIGHT*0.02, screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    #retorna o vencedor
    return 1 if player2.lives <= 0 else 2 if player1.lives <= 0 else 0
