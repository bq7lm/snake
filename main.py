import pygame
import sys
import random 

# Константы
WIDTH, HEIGHT = 640, 720 # 640 + 80 из-за меню

class Player:
    def __init__(self):
        self.heart = 4
        self.size_x = 32
        self.size_y = 32
        self.pos_x = 60
        self.pos_y = 60
        self.apple_pos_x = 60
        self.apple_pos_y = 60
        self.see = 1  # 1 - up, 2 - down, 3 - right, 4 - left
        self.image_apple = pygame.image.load('sprites/apple.png')
        self.image_head = pygame.image.load('sprites/head.png')
        self.image_body = pygame.image.load('sprites/body.png')
        self.last_down = 1  # 1 - up, 2 - down, 3 - right, 4 - left

    def draw(self, screen):
        # Рисуем голову игрока
        screen.blit(self.image_head, (self.pos_x, self.pos_y))

    def move(self):
        # Логика движения игрока
        if self.see == 1:  # Вверх
            self.pos_y -= 5
        elif self.see == 2:  # Вниз
            self.pos_y += 5
        elif self.see == 3:  # Вправо
            self.pos_x += 5
        elif self.see == 4:  # Влево
            self.pos_x -= 5

    def apple(self):
        self.pos_x, self.pos_y = self.apple_random_position()

    def apple_random_position(self):
        # Генерация случайной позиции для яблока
        x = random.randint(0, (WIDTH - self.size_x) // 5) * 5
        y = random.randint(0, (HEIGHT - self.size_y - 60) // 5) * 5  # Учитываем высоту меню
        return x, y

    def apple_draw(self, screen):
        screen.blit(self.image_apple, (self.apple_pos_x, self.apple_pos_y))

    def game_over(self, screen):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Ждем 2 секунды перед перезапуском
        self.reset()

    def reset(self):
        self.heart = 4
        self.pos_x = 60
        self.pos_y = 60
        self.see = 1  # Сброс направления

player = Player()

# Инициализация Pygame
pygame.init()

FPS = 15
# Images
menu = pygame.image.load('sprites/menu.png')
heart = pygame.image.load('sprites/heart.png')
pause = pygame.image.load('sprites/pause.png')
play = pygame.image.load('sprites/play.png')

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Установка иконки
icon = pygame.image.load('sprites/icon.png')
pygame.display.set_icon(icon)

# Главный игровой цикл
def main():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Обработка нажатий клавиш для управления игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.see = 1
        elif keys[pygame.K_DOWN]:
            player.see = 2
        elif keys[pygame.K_RIGHT]:
            player.see = 3
        elif keys[pygame.K_LEFT]:
            player.see = 4

        # Движение игрока
        player.move()


        # Проверка выхода за пределы поля
        if (player.pos_x < 0 or player.pos_x >= WIDTH or
            player.pos_y < 0 or player.pos_y >= HEIGHT - 60):  # Учитываем высоту меню
            player.game_over(screen)

        # Заполнение фона
        screen.fill('GREEN')
        screen.blit(menu, (0, 660))

        for i in range(player.heart):
            screen.blit(heart, (8 + i * 40, 680))  # Отрисовка сердечек с отступом

        screen.blit(pause, (600 , 680))

        # Рисуем игрока
        player.draw(screen)
        player.apple_draw(screen)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

