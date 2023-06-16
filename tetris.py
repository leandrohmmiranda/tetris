import pygame
import random

# Define as cores usadas no jogo
colors = [
    (0, 0, 0),              # Preto
    (120, 37, 179),         # Roxo
    (100, 179, 179),        # Azul esverdeado
    (80, 34, 22),           # Marrom
    (80, 134, 22),          # Verde claro
    (180, 34, 22),          # Vermelho escuro
    (180, 34, 122),         # Roxo claro
]

# Define a classe Figure que representa as peças do Tetris
class Figure:
    x = 0
    y = 0

    # Define as peças disponíveis no jogo
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # Peça L
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # Peça Z
        [[6, 7, 9, 10], [1, 5, 6, 10]], # Peça S
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # Peça T
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # Peça L invertido
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # Peça quadrada
        [[1, 2, 5, 6]], # Peça linha
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1) # Escolhe aleatoriamente uma peça
        self.color = random.randint(1, len(colors) - 1)      # Escolhe aleatoriamente uma cor para a peça
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation] # Retorna a forma atual da peça

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type]) # Gira a peça

# Define a classe Tetris que representa o jogo em si
class Tetris:
    def __init__(self, height, width):
        # Configurações iniciais do jogo
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
    
        # Define a altura e a largura do campo e o preenche com zeros
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        # Cria uma nova figura aleatória para ser controlada pelo jogador
        self.figure = Figure(3, 0)

    def intersects(self):
        # Verifica se há interseção entre a figura controlada pelo jogador e o campo de jogo
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        # Verifica se há linhas completas no campo de jogo e as remove
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        # Move a figura controlada pelo jogador para a posição mais baixa possível
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        # Move a figura controlada pelo jogador uma posição para baixo
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        # Congela a figura controlada pelo jogador no campo de jogo
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        # Move a figura controlada pelo jogador para a direita ou esquerda
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        # Rotaciona a figura controlada pelo jogador
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

# Inicializa o motor do jogo
pygame.init()

# Define algumas cores
BLACK = (0, 0, 0)  # Cor preta
WHITE = (255, 255, 255) # Cor branca
GRAY = (128, 128, 128) # Cor cinza

size = (400, 500) # Tamanho da tela
screen = pygame.display.set_mode(size) # Define a tela do jogo com o tamanho especificado

pygame.display.set_caption("Tetris") # Define o título da janela do jogo como "Tetris"

# Loop até o usuário clicar no botão de fechar.
done = False # Define a variável "done" como falsa
clock = pygame.time.Clock() # Define o objeto "clock" para controlar o tempo 
fps = 25 # Define a taxa de quadros por segundo
game = Tetris(20, 10) # Cria um objeto Tetris com 20 linhas e 10 colunas
counter = 0 # Define a variável "counter" como 0
pressing_down = False # Define a variável "pressing_down" como falsa

while not done: # Loop principal do jogo
    if game.figure is None: # Se não houver figura no jogo
        game.new_figure() # Cria uma nova figura
    counter += 1 # Incrementa o contador de tempo
    if counter > 100000: # Se o contador de tempo ultrapassar um valor muito grande
        counter = 0 # Reinicia o contador de tempo
    if counter % (fps // game.level // 2) == 0 or pressing_down: # Se o contador de tempo atingir um determinado valor ou se a tecla de seta para baixo estiver pressionada
        if game.state == "start": # Se o estado do jogo for "start"
            game.go_down() # Move a figura para baixo

    for event in pygame.event.get(): # Loop de eventos do Pygame
        if event.type == pygame.QUIT: # Se o evento for de fechar o jogo
            done = True # Define a variável "done" como verdadeira
        if event.type == pygame.KEYDOWN: # Se uma tecla for pressionada
            if event.key == pygame.K_UP: # Se a tecla de seta para cima for pressionada
                game.rotate() # Rotaciona a figura
            if event.key == pygame.K_DOWN: # Se a tecla de seta para baixo for pressionada
                pressing_down = True # Define a variável "pressing_down" como verdadeira
            if event.key == pygame.K_LEFT: # Se a tecla de seta para a esquerda for pressionada
                game.go_side(-1) # Move a figura para a esquerda
            if event.key == pygame.K_RIGHT: # Se a tecla de seta para a direita for pressionada
                game.go_side(1) # Move a figura para a direita
            if event.key == pygame.K_SPACE: # Se a tecla de espaço for pressionada
                game.go_space() # Move a figura para o espaço livre abaixo
            if event.key == pygame.K_ESCAPE: # Se a tecla de escape for pressionada
                game.__init__(20, 10) # reinicia o jogo com 20 colunas e 10 linhas

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False # marca que a tecla de seta para baixo foi solta

    screen.fill(WHITE) # preenche a tela com a cor branca

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1) # desenha o tabuleiro do jogo
            if game.field[i][j] > 0: # se há uma peça em uma determinada posição do tabuleiro
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1]) # desenha a peça na posição correspondente do tabuleiro

    if game.figure is not None: # se há uma figura em jogo
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2]) # desenha a figura na posição correspondente do tabuleiro

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK) # exibe a pontuação do jogador
    text_game_over = font1.render("Game Over", True, (255, 125, 0)) # exibe o texto "Game Over"
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0)) # exibe o texto "Press ESC"

    screen.blit(text, [0, 0]) # exibe a pontuação na tela
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200]) # exibe o texto "Game Over" na tela
        screen.blit(text_game_over1, [25, 265]) # exibe o texto "Press ESC" na tela

    pygame.display.flip() # atualiza a tela
    clock.tick(fps) # espera o tempo necessário para manter o FPS

pygame.quit() # finaliza o jogo