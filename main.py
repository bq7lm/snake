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
        self.apple_pos_x, self.apple_pos_y = self.apple_random_position()
        self.see = 1  # 1 - up, 2 - down, 3 - right, 4 - left
        self.image_apple = pygame.image.load('sprites/apple.png')
        self.image_head = pygame.image.load('sprites/head.png')
        self.image_body = pygame.image.load('sprites/body.png')
        self.last_down = 1  # 1 - up, 2 - down, 3 - right, 4 - left
        self.score = 0
        self.record = 0

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

    def apple_random_position(self):
        # Генерация случайной позиции для яблока
        x = random.randint(0, (WIDTH - self.size_x) // 5) * 5
        y = random.randint(0, (HEIGHT - self.size_y - 60) // 5) * 5  # Учитываем высоту меню
        return x, y

    def check_collision(self):
        # Проверка столкновения с яблоком
        if (self.pos_x < self.apple_pos_x + self.size_x and
            self.pos_x + self.size_x > self.apple_pos_x and
            self.pos_y < self.apple_pos_y + self.size_y and
            self.pos_y + self.size_y > self.apple_pos_y):
            return True
        return False

    def update_apple(self):
        # Обновление позиции яблока
        self.apple_pos_x, self.apple_pos_y = self.apple_random_position()
        self.score += 1  # Увеличиваем счет при поедании яблока
        if self.score >= self.record:
        	self.record = self.score # Проверка рекорда

    def apple_draw(self, screen):
        screen.blit(self.image_apple, (self.apple_pos_x, self.apple_pos_y))

    def game_over(self, screen):
        font = pygame.font.Font(None, 64)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        font_continue = pygame.font.Font(None, 32)
        text_continue = font_continue.render(f"Best record: {self.record} | You: {self.score} | Press Enter to Restart", True, (255, 255, 255))
        screen.blit(text_continue, (80, 400))

        pygame.display.flip()

    def reset(self):
        self.heart = 4
        self.pos_x = 60
        self.pos_y = 60
        self.see = 1  # Сброс направления
        self.score = 0
        self.apple_pos_x, self.apple_pos_y = self.apple_random_position()  # Сброс позиции яблока

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
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Обработка нажатий клавиш для управления игроком
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_UP] and player.see != 2:  # Запрет на движение в противоположном направлении
                player.see = 1
            elif keys[pygame.K_DOWN] and player.see != 1:
                player.see = 2
            elif keys[pygame.K_RIGHT] and player.see != 4:
                player.see = 3
            elif keys[pygame.K_LEFT] and player.see != 3:
                player.see = 4

            # Движение игрока
            player.move()

            # Проверка выхода за пределы поля
            if (player.pos_x < 0 or player.pos_x >= WIDTH - player.size_x or
                player.pos_y < 0 or player.pos_y >= HEIGHT - 60 - player.size_y):  # Учитываем высоту меню
                game_over = True

            # Проверка столкновения с яблоком
            if player.check_collision():
                player.update_apple()  # Обновляем позицию яблока и увеличиваем счет

        else:
            # Если игра завершена, показываем экран "Game Over"
            player.game_over(screen)

            # Проверка нажатия клавиши Enter для перезапуска игры
            if keys[pygame.K_RETURN]:  # Enter
                player.reset()
                game_over = False
            elif keys[pygame.K_SPACE]:  # SPACE
                player.reset()
                game_over = False

        # Заполнение фона
        if not game_over:
            screen.fill('GREEN')  # Заполняем фон зеленым, если игра не завершена
            screen.blit(menu, (0, 660))

            for i in range(player.heart):
                screen.blit(heart, (8 + i * 40, 680))  # Отрисовка сердечек с отступом

            screen.blit(pause, (600, 680))

            font_score = pygame.font.Font(None, 32)
            score_text = font_score.render(f"Score {player.score} | Record: {player.record}", True, (255, 255, 255))  # Белый цвет текста
            screen.blit(score_text, (240, 680))  # Центрируем текст по горизонтали

            # Рисуем игрока и яблоко, если игра не завершена
            player.draw(screen)
            player.apple_draw(screen)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
