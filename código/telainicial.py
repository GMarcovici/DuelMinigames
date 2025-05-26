#Inicialização --------------------------------------------------------------------------------------------------------------
import pygame, random, math #bibliotecas

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
#------------------------------------------------------------------------------------------------------------------------Funções





# Loop principal -----------------------------------------------------------------------------------------------------------------
def main():
    #mostra a tela de início
    if not title_screen():
        return False
    
if __name__ == "__main__":
    main()