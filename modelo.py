import pygame
import os
import random
pygame.init()

# Constantes Globais
SCREEN_HEIGHT = 600  # Altura da tela
SCREEN_WIDTH = 1100  # Largura da tela
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Configura a tela do jogo

# Carrega as imagens do dinossauro
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

# Carrega as imagens dos cactos pequenos
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

# Carrega as imagens dos cactos grandes
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

# Carrega as imagens dos pássaros
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

# Carrega a imagem das nuvens
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

# Carrega a imagem do fundo do jogo
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80  # Posição X inicial do dinossauro
    Y_POS = 310  # Posição Y inicial do dinossauro
    Y_POS_DUCK = 340  # Posição Y do dinossauro quando abaixado
    JUMP_VEL = 8.5  # Velocidade do pulo do dinossauro

    def __init__(self):
        self.duck_img = DUCKING  # Imagens do dinossauro abaixado
        self.run_img = RUNNING  # Imagens do dinossauro correndo
        self.jump_img = JUMPING  # Imagem do dinossauro pulando

        self.dino_duck = False  # Estado do dinossauro abaixado
        self.dino_run = True  # Estado do dinossauro correndo
        self.dino_jump = False  # Estado do dinossauro pulando

        self.step_index = 0  # Índice de passo para animação
        self.jump_vel = self.JUMP_VEL  # Velocidade do pulo atual
        self.image = self.run_img[0]  # Imagem atual do dinossauro
        self.dino_rect = self.image.get_rect()  # Retângulo da imagem do dinossauro
        self.dino_rect.x = self.X_POS  # Define a posição X do retângulo do dinossauro
        self.dino_rect.y = self.Y_POS  # Define a posição Y do retângulo do dinossauro

    # Atualiza o estado do dinossauro
    def update(self, userInput):
        # Decide a ação do dinossauro com base nos obstáculos e pontuação
        action = self.decide_action(self.dino_rect, obstacles, points)
        
        # Atualiza os estados do dinossauro com base na ação decidida
        if action == "duck":
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif action == "jump" and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True

        # Executa a ação correspondente
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        # Reinicia o índice de passo para garantir a continuidade das animações
        if self.step_index >= 10:
            self.step_index = 0

        # Verifica a entrada do usuário e atualiza os estados do dinossauro conforme necessário
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    # Decide a ação do dinossauro com base na posição dos obstáculos e na pontuação
    def decide_action(self, dino_rect, obstacles, points):
        # Se não houver obstáculos, retorna uma string vazia (nenhuma ação específica)
        if not obstacles:
            return ""

        # Define a distância base para pular
        base_jump_distance = 200
        # Pega o primeiro obstáculo da lista (o mais próximo)
        obstacle = obstacles[0]
        # Calcula a distância entre o dinossauro e o obstáculo
        distance = obstacle.rect.x - dino_rect.x
        # Ajusta a distância de pulo com base na pontuação (quanto maior a pontuação, maior a distância de pulo)
        distanceJump = base_jump_distance + (points // 60) * 2

        # Se a distância até o obstáculo for menor que a distância ajustada
        if distance < distanceJump:
            # Se o obstáculo for um pássaro
            if isinstance(obstacle, Bird):
                # Se o pássaro estiver abaixo de 300 na coordenada Y, retorna "duck" para abaixar
                if obstacle.rect.y < 300:
                    return "duck"
                else:
                    # Caso contrário, retorna "jump" para pular
                    return "jump"
            else:
                # Se o obstáculo não for um pássaro (é um cacto), retorna "jump" para pular
                return "jump"
        # Se a distância até o obstáculo não for menor que a distância ajustada, retorna uma string vazia (nenhuma ação específica)
        return ""
    
    # Muda o estado do dinossauro para abaixado
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    # Muda o estado do dinossauro para correndo
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    # Muda o estado do dinossauro para pulando
    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    # Desenha o dinossauro na tela
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)  # Posição X inicial da nuvem
        self.y = random.randint(50, 100)  # Posição Y inicial da nuvem
        self.image = CLOUD  # Imagem da nuvem
        self.width = self.image.get_width()  # Largura da imagem da nuvem

    # Atualiza a posição da nuvem
    def update(self):
        self.x -= game_speed  # Move a nuvem para a esquerda com a velocidade do jogo
        if self.x < -self.width:  # Se a nuvem sair da tela
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)  # Redefine a posição X da nuvem
            self.y = random.randint(50, 100)  # Redefine a posição Y da nuvem

    # Desenha a nuvem na tela
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))  # Desenha a nuvem na posição atual


class Obstacle:
    def __init__(self, image, type):
        self.image = image  # Imagem do obstáculo
        self.type = type  # Tipo de obstáculo (índice da imagem)
        self.rect = self.image[self.type].get_rect()  # Retângulo do obstáculo
        self.rect.x = SCREEN_WIDTH  # Posição X inicial do obstáculo

    # Atualiza a posição do obstáculo
    def update(self):
        self.rect.x -= game_speed  # Move o obstáculo para a esquerda com a velocidade do jogo
        if self.rect.x < -self.rect.width:  # Se o obstáculo sair da tela
            obstacles.pop()  # Remove o obstáculo da lista

    # Desenha o obstáculo na tela
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)  # Desenha o obstáculo na posição atual


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)  # Define um tipo aleatório de cacto pequeno
        super().__init__(image, self.type)  # Chama o construtor da classe pai (Obstacle)
        self.rect.y = 325  # Define a posição Y do cacto pequeno


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)  # Define um tipo aleatório de cacto grande
        super().__init__(image, self.type)  # Chama o construtor da classe pai (Obstacle)
        self.rect.y = 300  # Define a posição Y do cacto grande


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0  # Define o tipo do pássaro
        super().__init__(image, self.type)  # Chama o construtor da classe pai (Obstacle)
        self.rect.y = random.choice([250, 300])  # Define uma posição Y aleatória para o pássaro
        self.index = 0  # Índice para animação do pássaro

    # Desenha o pássaro na tela
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)  # Desenha a imagem correspondente à animação
        self.index += 1  # Incrementa o índice para a próxima imagem


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()  # Relógio para controlar o tempo do jogo
    player = Dinosaur()  # Cria um dinossauro
    cloud = Cloud()  # Cria uma nuvem
    game_speed = 20  # Velocidade inicial do jogo
    x_pos_bg = 0  # Posição X inicial do fundo
    y_pos_bg = 380  # Posição Y inicial do fundo
    points = 0  # Pontuação inicial
    font = pygame.font.Font('freesansbold.ttf', 20)  # Fonte para desenhar a pontuação
    obstacles = []  # Lista de obstáculos
    death_count = 0  # Contador de mortes

    # Função para atualizar a pontuação
    def score():
        global points, game_speed
        points += 1  # Incrementa a pontuação
        if points % 100 == 0:  # A cada 100 pontos
            game_speed += 1  # Aumenta a velocidade do jogo

        text = font.render("Pontuação: " + str(points), True, (0, 0, 0))  # Renderiza a pontuação
        textRect = text.get_rect()
        textRect.center = (1000, 40)  # Define a posição do texto da pontuação
        SCREEN.blit(text, textRect)  # Desenha a pontuação na tela

    # Função para atualizar o fundo
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()  # Largura da imagem do fundo
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))  # Desenha o fundo na posição atual
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))  # Desenha a continuação do fundo
        if x_pos_bg <= -image_width:  # Se o fundo sair da tela
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))  # Redesenha a continuação do fundo
            x_pos_bg = 0  # Reseta a posição X do fundo
        x_pos_bg -= game_speed  # Move o fundo para a esquerda com a velocidade do jogo

    # Loop principal do jogo
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))  # Preenche a tela com branco
        userInput = pygame.key.get_pressed()  # Obtém a entrada do usuário

        player.draw(SCREEN)  # Desenha o dinossauro na tela
        player.update(userInput)  # Atualiza o estado do dinossauro com base na entrada do usuário

        if len(obstacles) == 0:  # Se não houver obstáculos na lista
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))  # Adiciona um cacto pequeno
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))  # Adiciona um cacto grande
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))  # Adiciona um pássaro

        for obstacle in obstacles:
            obstacle.draw(SCREEN)  # Desenha o obstáculo na tela
            obstacle.update()  # Atualiza a posição do obstáculo
            if player.dino_rect.colliderect(obstacle.rect):  # Verifica colisão entre dinossauro e obstáculo
                pygame.time.delay(100)  # Pausa por 100 milissegundos
                death_count += 1  # Incrementa o contador de mortes
                menu(death_count)  # Chama o menu

        background()  # Atualiza o fundo

        cloud.draw(SCREEN)  # Desenha a nuvem na tela
        cloud.update()  # Atualiza a posição da nuvem

        score()  # Atualiza e desenha a pontuação

        clock.tick(30)  # Controla a taxa de quadros por segundo
        pygame.display.update()  # Atualiza a tela


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))  # Preenche a tela com branco
        font = pygame.font.Font('freesansbold.ttf', 30)  # Fonte para desenhar o texto

        if death_count == 0:
            text = font.render("Aperte qualquer tecla para começar", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Aperte qualquer tecla para recomeçar", True, (0, 0, 0))
            score = font.render("Pontuação: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)  # Posição do texto da pontuação
            SCREEN.blit(score, scoreRect)  # Desenha a pontuação na tela
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Posição do texto do menu
        SCREEN.blit(text, textRect)  # Desenha o texto do menu na tela
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))  # Desenha o dinossauro no menu
        pygame.display.update()  # Atualiza a tela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()  # Inicia o jogo


menu(death_count=0)  # Chama o menu para iniciar o jogo
