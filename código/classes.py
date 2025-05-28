#Inicialização --------------------------------------------------------------------------------------------------------------
import pygame, random, math, Functions, Niveis#bibliotecas
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


#Classe dos jogadores
class Player(pygame.sprite.Sprite):
    #Recebe a posição em x e y, o dicionário com as imagens de direção, os controles(Varia pra cada player) e tecla de tiro(Varia pra cada Player).
    def __init__(self, x, y, destinatario, controls, shoot_key, score):
        super().__init__()
        self.images = {
            "up": pygame.image.load(destinatario["up"]).convert_alpha(),
            "down": pygame.image.load(destinatario["down"]).convert_alpha(),
            "left": pygame.image.load(destinatario["left"]).convert_alpha(),
            "right": pygame.image.load(destinatario["right"]).convert_alpha(),
        }
        #Define as imagens para o mesmo tamanho
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (50, 50))
    
        self.image = self.images["right"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.controls = controls 
        self.shoot_key = shoot_key
        self.direction = "right"
        self.lives = 3
        self.cooldown = 0
        self.cooldown_max = 15
        self.bullets = pygame.sprite.Group()
        self.score = 0
    
    def update(self, obstacles):
        keys = pygame.key.get_pressed()
        new_rect = self.rect.copy()
        
        if keys[self.controls[0]]:  # cima
            new_rect.y -= self.speed
            self.direction = "up"
        if keys[self.controls[1]]:  # baixo
            new_rect.y += self.speed
            self.direction = "down"
        if keys[self.controls[2]]:  # esquerda
            new_rect.x -= self.speed
            self.direction = "left"
        if keys[self.controls[3]]:  # direita
            new_rect.x += self.speed
            self.direction = "right"
        
        # Atualizar a imagem com base na direção
        self.image = self.images[self.direction]
    
        # Analiza se houve colisão com obstáculos
        can_move = True
        for obstacle in obstacles:
            if new_rect.colliderect(obstacle.rect):
                can_move = False
                break
        
        #Não permite que o jogador saia da tela
        if can_move:
            new_rect.x = max(0, min(WIDTH - self.rect.width, new_rect.x))
            new_rect.y = max(0, min(HEIGHT - self.rect.height, new_rect.y))
            self.rect = new_rect
    
    def shoot(self):
        if self.cooldown <= 0:
            
            pygame.mixer.Sound('Assets/Sounds/shoot.wav').play()

            bullet_speed = 7
            if self.direction == "right":
                bullet = Bullet(self.rect.right, self.rect.centery - 2, bullet_speed, 0)
            elif self.direction == "left":
                bullet = Bullet(self.rect.left - 5, self.rect.centery - 2, -bullet_speed, 0)
            elif self.direction == "up":
                bullet = Bullet(self.rect.centerx - 2, self.rect.top - 5, 0, -bullet_speed)
            elif self.direction == "down":
                bullet = Bullet(self.rect.centerx - 2, self.rect.bottom, 0, bullet_speed)
            
            self.bullets.add(bullet)
            self.cooldown = self.cooldown_max
    
    def update_bullets(self, obstacles, enemies=None, other_player=None):
        if self.cooldown > 0:
            self.cooldown -= 1
        
        self.bullets.update()
        
        #Destrói as balas que saem da tela
        for bullet in self.bullets.copy():
            if (bullet.rect.right < 0 or bullet.rect.left > WIDTH or
                bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT):
                bullet.kill()
        
        # Checa colisões com obstáculos	
        for obstacle in obstacles:
            pygame.sprite.spritecollide(obstacle, self.bullets, True)
        
        # Checa colisões com inimigos
        if enemies:
            for enemy in enemies:
                if pygame.sprite.spritecollide(enemy, self.bullets, True):
                    pygame.mixer.Sound('Assets/Sounds/player_hit.wav').play()
                    pygame.mixer.Sound('Assets/Sounds/enemy_death.wav').play()
                    enemy.kill()
        
        # Checa colisões com o outro jogador
        if other_player:
            if pygame.sprite.spritecollide(other_player, self.bullets, True):
                pygame.mixer.Sound('Assets/Sounds/player_hit.wav').play()
                other_player.lives -= 1
    
    def draw_lives(self, surface):
        life_color = GREEN if self.lives >= 3 else YELLOW if self.lives == 2 else RED
        for i in range(self.lives):
            pygame.draw.rect(surface, life_color, (self.rect.x + i * 10, self.rect.y - 15, 8, 8))

# Classe da bala
class Bullet(pygame.sprite.Sprite):
    #Recebe a posição em x e y e a velocidade em x e y
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.image.load('Assets/Objetos/Bala.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy
    
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

# Classe do obstáculo
class Obstacle(pygame.sprite.Sprite):
    #Recebe a posição em x e y e a largura e a altura do obstáculo
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = WHITE

#Classe do inimigo
class Enemy(pygame.sprite.Sprite):
    #Recebe sua posição em x e y
    def __init__(self, x, y):
        super().__init__()
        # Animação do inimigo
        self.animation_frames = [
            pygame.image.load(f'Assets/Characters/bosspygame/sprite_{i}.png').convert_alpha()
            for i in range(0, 70)#70 frames de animação
        ]
        self.animation_frames = [pygame.transform.scale(frame, (50, 50)) for frame in self.animation_frames]
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10 

        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.bullets = pygame.sprite.Group()
        self.cooldown = random.randint(30, 90)

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            for i in range(len(self.animation_frames)):
                if i == self.current_frame:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                    break
            self.image = self.animation_frames[self.current_frame]

    def update(self, players):
        self.update_animation()  # Atualiza a animação do inimigo

        # Vair atrás do jogador mais próximo
        closest_player = min(players, key=lambda p: math.hypot(
            self.rect.centerx - p.rect.centerx, 
            self.rect.centery - p.rect.centery))
        
        dx = closest_player.rect.centerx - self.rect.centerx
        dy = closest_player.rect.centery - self.rect.centery
        dist = max(1, math.hypot(dx, dy))
        
        self.rect.x += (dx / dist) * self.speed
        self.rect.y += (dy / dist) * self.speed

    def shoot(self):
        if self.cooldown <= 0:
            bullet_speed = 4
            # Atira nas quatro direções
            self.bullets.add(
                Bullet(self.rect.centerx, self.rect.top, 0, -bullet_speed),
                Bullet(self.rect.centerx, self.rect.bottom, 0, bullet_speed),
                Bullet(self.rect.left, self.rect.centery, -bullet_speed, 0),
                Bullet(self.rect.right, self.rect.centery, bullet_speed, 0
                )
            )
            self.cooldown = random.randint(60, 120)
        else:
            self.cooldown -= 1
    
    def update_bullets(self, players, obstacles):
        self.bullets.update()
        
        #Elimina as balas que sairam da tela
        for bullet in self.bullets.copy():
            if (bullet.rect.right < 0 or bullet.rect.left > WIDTH or
                bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT):
                bullet.kill()
        
        for obstacle in obstacles:
            pygame.sprite.spritecollide(obstacle, self.bullets, True)
        
        for player in players:
            if pygame.sprite.spritecollide(player, self.bullets, True):
                player.lives -= 1


#Classe do Boss
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Animação do boss
        self.animation_frames = [
            pygame.image.load(f'Assets/Characters/bosspygame/sprite_{i}.png').convert_alpha()
            for i in range(0, 70)#70 frames de animação
        ]
        self.animation_frames = [pygame.transform.scale(frame, (100, 100)) for frame in self.animation_frames]
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10

        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - 50
        self.rect.y = HEIGHT // 2 - 50
        self.speed = 4
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0
        self.cooldown_max = 30
        self.health = 20
        self.move_direction = 1
        self.start_delay = 2 * FPS

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            for i in range(len(self.animation_frames)):
                if i == self.current_frame:
                    self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                    break
            self.image = self.animation_frames[self.current_frame]

    def update(self):
        self.update_animation() 

        if self.start_delay > 0:
            self.start_delay -= 1
            return False

        #Define o movimento do boss, sendo que ele só se move na horizontal   
        self.rect.x += self.speed * self.move_direction
        if self.rect.left <= 0:
            self.move_direction = 1
        elif self.rect.right >= WIDTH:
            self.move_direction = -1

    def shoot(self):
        if self.start_delay > 0:
            return False
            
        if self.cooldown <= 0:
            bullet_speed = 5
            num_bullets = 12

            #Som de tiro do boss
            pygame.mixer.Sound('Assets/Sounds/boss_shoot.wav').play()

            #Tiros em círculo
            for i in range(num_bullets):
                angle = (2 * math.pi / num_bullets) * i
                dx = math.cos(angle) * bullet_speed
                dy = math.sin(angle) * bullet_speed
                
                self.bullets.add(Bullet(
                    self.rect.centerx,
                    self.rect.centery,
                    dx, dy
                ))
            
            self.cooldown = self.cooldown_max
        else:
            self.cooldown -= 1
    
    def update_bullets(self, players):
        self.bullets.update()
        
        #Elimina as balas que sairam da tela
        for bullet in self.bullets.copy():
            if (bullet.rect.right < 0 or bullet.rect.left > WIDTH or
                bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT):
                bullet.kill()
        
        #Colisão com o jogador
        for player in players:
            if pygame.sprite.spritecollide(player, self.bullets, True):
                player.lives -= 1
    
    def take_hit(self):
        self.health -= 1
        pygame.mixer.Sound('Assets/Sounds/boss_hit.wav').play()
        if self.health < 1:
            pygame.mixer.Sound('Assets/Sounds/enemy_death.wav').play()
            
    
    def draw_health(self, surface):
        health_width = self.rect.width * (self.health / 20)
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, health_width, 5))

#Classe dos barris
class Barrel(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, speed=3):
        super().__init__()
        self.image = pygame.image.load('Assets/Objetos/Barrel.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = dx * speed
        self.dy = dy * speed

    def update(self, players=None):
        # Se move em linha reta
        self.rect.x += self.dx
        self.rect.y += self.dy

        #Quica nas bordas da tela e muda de direção
        if self.rect.left <= 0:
            self.dx = abs(self.dx)  
        if self.rect.right >= WIDTH:
            self.dx = -abs(self.dx) 
        if self.rect.top <= 0:
            self.dy = abs(self.dy) 
        if self.rect.bottom >= HEIGHT:
            self.dy = -abs(self.dy)

        #Não deixa sair da tela
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carrega a imagem da bola de futebol
        self.image = pygame.image.load('Assets/Objetos/bolafutebolpygame-1.png.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Ajusta o tamanho para 30x30
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2 - 15
        self.rect.y = HEIGHT//2 - 15
        self.dx = random.choice([-4, -3, 3, 4])
        self.dy = random.choice([-4, -3, 3, 4])
    
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        #Quica nas bordas da tela
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        
        #Mantém a bola na tela
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))