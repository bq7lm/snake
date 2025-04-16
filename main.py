import pygame
import sys
import random 

# Константы
WIDTH, HEIGHT = 640, 720  # 640 + 80 из-за меню

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

class Player:
    def __init__(self):
        self.heart = 4
        self.size_x = 32
        self.size_y = 32
        self.pos_x = 300
        self.pos_y = 300
        self.body = []  # Список для хранения частей тела
        self.apple_pos_x, self.apple_pos_y = self.apple_random_position()
        self.see = 1  # 1 - up, 2 - down, 3 - right, 4 - left
        self.image_apple = pygame.image.load('sprites/apple.png')

        self.image_head_up = pygame.image.load('sprites/head_up.png')
        self.image_head_down = pygame.image.load('sprites/head_down.png')
        self.image_head_left = pygame.image.load('sprites/head_left.png')
        self.image_head_right = pygame.image.load('sprites/head_right.png')

        self.eat_sound = pygame.mixer.Sound('sounds/eat.mp3') # 
        self.image_body = pygame.image.load('sprites/body.png')
        self.last_down = 1  # 1 - up, 2 - down, 3 - right, 4 - left
        self.score = 0
        self.record = 0

    def draw(self, screen):
        # Рисуем голову игрока
        if self.see == 1:
            screen.blit(self.image_head_up, (self.pos_x, self.pos_y))
        elif self.see == 2:
            screen.blit(self.image_head_down, (self.pos_x, self.pos_y))
        elif self.see == 3:
            screen.blit(self.image_head_right, (self.pos_x, self.pos_y))
        elif self.see == 4:
            screen.blit(self.image_head_left, (self.pos_x, self.pos_y))

    def move(self):
        # Сохраняем текущую позицию головы в начало тела
        if self.score > 0:
            self.body.insert(0, (self.pos_x, self.pos_y))
            if len(self.body) > self.score:
                self.body.pop()

        if self.see == 1:
            self.pos_y -= 5
        elif self.see == 2:
            self.pos_y += 5
        elif self.see == 3:
            self.pos_x += 5
        elif self.see == 4:
            self.pos_x -= 5

    def draw_body(self):
        for part in self.body:
            screen.blit(self.image_body, part)

    def apple_random_position(self):
        x = random.randint(0, (WIDTH - self.size_x) // 5) * 5
        y = random.randint(0, (HEIGHT - self.size_y - 60) // 5) * 5
        return x, y

    def check_collision(self):
        if (self.pos_x < self.apple_pos_x + self.size_x and
            self.pos_x + self.size_x > self.apple_pos_x and
            self.pos_y < self.apple_pos_y + self.size_y and
            self.pos_y + self.size_y > self.apple_pos_y):
            self.eat_sound.play()
            return True
        return False

    def update_apple(self):
        self.apple_pos_x, self.apple_pos_y = self.apple_random_position()
        self.score += 1
        if self.score >= self.record:
            self.record = self.score

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
        self.see = 1
        self.score = 0
        self.body = []
        self.apple_pos_x, self.apple_pos_y = self.apple_random_position()

player = Player()



FPS = 15
menu = pygame.image.load('sprites/menu.png')
heart = pygame.image.load('sprites/heart.png')
pause = pygame.image.load('sprites/pause.png')
play = pygame.image.load('sprites/play.png')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

icon = pygame.image.load('sprites/icon.png')
pygame.display.set_icon(icon)

def main():
    clock = pygame.time.Clock()
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_UP] and player.see != 2:
                player.see = 1
            elif keys[pygame.K_DOWN] and player.see != 1:
                player.see = 2
            elif keys[pygame.K_RIGHT] and player.see != 4:
                player.see = 3
            elif keys[pygame.K_LEFT] and player.see != 3:
                player.see = 4

            player.move()

            if (player.pos_x < 0 or player.pos_x >= WIDTH - player.size_x or
                player.pos_y < 0 or player.pos_y >= HEIGHT - 60 - player.size_y):
                game_over = True

            if player.check_collision():
                player.update_apple()

        else:
            player.game_over(screen)
            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                player.reset()
                game_over = False

        if not game_over:
            screen.fill('GREEN')
            screen.blit(menu, (0, 660))

            for i in range(player.heart):
                screen.blit(heart, (8 + i * 40, 680))

            screen.blit(pause, (600, 680))

            font_score = pygame.font.Font(None, 32)
            score_text = font_score.render(f"Score {player.score} | Record: {player.record}", True, (255, 255, 255))
            screen.blit(score_text, (240, 680))

            player.draw_body()
            player.draw(screen)
            player.apple_draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
