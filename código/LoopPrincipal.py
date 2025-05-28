#Inicialização --------------------------------------------------------------------------------------------------------------
import pygame, random, math, classes, Functions, Niveis#bibliotecas
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

def main():
    #mostra a tela de início
    if not Functions.title_screen():
        return False
    
    #Define o jogador 1 dentro da classse Player
    player1_images = {
        "up": "Assets/Characters/Azulcima-1.png.png",
        "down": "Assets/Characters/Azulbaixo-1.png.png",
        "left": "Assets/Characters/Azulesquerda-1.png.png",
        "right": "Assets/Characters/Azuldireita-1.png.png"}
    player1 = classes.Player(100, HEIGHT // 2, player1_images, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], pygame.K_SPACE, 0)

    #Define o jogador 2 dentro da classse Player
    player2_images = {
        "up": "Assets/Characters/Vermelhocima-1.png.png",
        "down": "Assets/Characters/Vermelhobaixo-1.png.png",
        "left": "Assets/Characters/Vermelhoesquerda-1.png.png",
        "right": "Assets/Characters/Vermelhodireita-1.png.png"}
    player2 = classes.Player(WIDTH - 130, HEIGHT // 2, player2_images, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], pygame.K_RETURN, 0)
    
    #Define os níveis do jogo, reinicando as condições dos players e calculando a pontuação a cada level
    levels = [Niveis.level_1, Niveis.level_2, Niveis.level_3, Niveis.level_4, Niveis.level_5]
    for level in levels:
        player1.lives = 3
        player2.lives = 3
        player1.bullets.empty()
        player2.bullets.empty()
        
        result = level(player1, player2)
        
        if result == 1:
            player1.score += 1
        elif result == 2:
            player2.score += 1
        
        pygame.time.delay(1000)

    #Define o vencedor e a tela de fundo condizente
    final_winner = 1 if player1.score > player2.score else 2 if player2.score > player1.score else 0
    Functions.show_game_over(final_winner)
    pygame.quit()

#Chama a função do loop principal
if __name__ == "__main__":
    main()