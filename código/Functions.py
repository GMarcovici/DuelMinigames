#Inicialização --------------------------------------------------------------------------------------------------------------
import pygame, random, math, classes, Functions, Niveis#bibliotecas
from Functions import *
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


#função pra desenhar textos na tela
def draw_text(text, font, color, x, y, surface, centered=True):
    text_surface = font.render(text, True, color)
    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)

#Função para exibir tela de início
def title_screen():
    state = "main" #estado inicial

    #imagem de fundo
    TelaInicio= pygame.image.load('Assets/Background/TelaInicio.png').convert()
    TelaInicio = pygame.transform.scale(TelaInicio, (WIDTH, HEIGHT))
    
    # Música de fundo
    pygame.mixer.init()
    pygame.mixer.music.load('Assets/Sounds/background_music.mp3')
    pygame.mixer.music.set_volume(0.30)  
    pygame.mixer.music.play(-1)  

    # Loop do menu
    while True:
        #aplica tela de fundo
        screen.fill(BLACK)
        screen.blit(TelaInicio, (0, 0))

        #muda o estado do menu para exibir instruções
        if state == "instructions":
            screen.fill(BLACK)
            draw_text("Instruções", big_font, WHITE, WIDTH//2, HEIGHT//5, screen)
            draw_text("Jogador 1: WASD para mover, ESPAÇO para atirar", font, BLUE, WIDTH//2, HEIGHT*2//5, screen)
            draw_text("Jogador 2: Setas para mover, ENTER para atirar", font, RED, WIDTH//2, HEIGHT*3//5, screen)
            draw_text("Pressione ENTER para Voltar", font, WHITE, WIDTH//2, HEIGHT*4//5, screen)
        
        #atualiza a tela
        pygame.display.flip()
        
        #Recebe os inputs do usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
                if event.key == pygame.K_RETURN:
                    if state == "main":
                        return True  
                    else:
                        state = "main" 
                if event.key == pygame.K_i and state == "main":
                    state = "instructions"

#Função de fim de jogo
def show_game_over(winner):

    #Música
    pygame.mixer.Sound('Assets/Sounds/victory.wav').play()

    #Tela de fim de jogo
    fimdejogo = pygame.image.load('Assets/Background/TelaFim.png').convert()
    fimdejogo = pygame.transform.scale(fimdejogo, (WIDTH, HEIGHT*1.2))

    #Loop da tela de fim de jogo
    while True:
        screen.fill(BLACK)

        p1 = pygame.image.load('Assets/Characters/Azulbaixo-1.png.png').convert()
        p1 = pygame.transform.scale(p1,(WIDTH*0.3, WIDTH*0.3))#Tamanho do player 1 que aparecerá no game over
        p2 = pygame.image.load('Assets/Characters/Vermelhobaixo-1.png.png').convert()
        p2 = pygame.transform.scale(p2,(WIDTH*0.3, WIDTH*0.3))#Tamanho do player 2 que aparecerá no game over
        
        #Dependendo de quem sai vitorioso, a tela de fim será diferente

        #empate
        if winner == 0:
            screen.blit(fimdejogo, (0, 0))
            draw_text("Empate!", big_font, WHITE, WIDTH//2, HEIGHT//2 - 50, screen)
            screen.blit(p1, ( WIDTH*0.7, HEIGHT*0.3))#Posição do player 1 no game over
            screen.blit(p2, (WIDTH*0.4, HEIGHT*0.3))#Posição do player 2 no game over

        #Vitória do player 1
        elif winner == 1:
            screen.blit(fimdejogo, (0, 0))
            screen.blit(p1, ( WIDTH*0.6, HEIGHT*0.3))#Posição do player 1 no game over

        #Vitória do player 2
        else:
            screen.blit(fimdejogo, (0, 0))
            screen.blit(p2, (WIDTH*0.6, HEIGHT*0.3))#Posição do player 2 no game over

        draw_text("Pressione ENTER para sair", font, WHITE, WIDTH//2, HEIGHT-30, screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return False
        
        clock.tick(FPS)
#------------------------------------------------------------------------------------------------------------------------Funções
