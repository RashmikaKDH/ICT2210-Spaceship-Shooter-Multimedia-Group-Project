import pygame
import random
import sys

pygame.init()

# --- Window Setup ---
w_width = 660
w_height = 600
window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Spaceship")

# --- Load Images ---
bg = pygame.image.load("media/bg.png")
bg = pygame.transform.scale(bg, (w_width, w_height))
start_bg = pygame.image.load("media/start_bg.png")
start_bg = pygame.transform.scale(start_bg, (w_width, w_height))
end_bg = pygame.image.load("media/end_bg.png")
end_bg = pygame.transform.scale(end_bg, (w_width, w_height))

spaceship_img = pygame.image.load("media/spaceship.png")
bullet = pygame.image.load("media/bullet.png")
enemy_img = [pygame.image.load(f'media/alien{i}.png') for i in range(1, 6)]
enemy_bullet = pygame.image.load("media/alien_bullet.png")

# --- Load Sounds ---
explosion = pygame.mixer.Sound("media/explosion.wav")
explosion2 = pygame.mixer.Sound("media/explosion2.wav")
laser = pygame.mixer.Sound("media/laser.wav")

# --- Fonts ---
font1 = pygame.font.SysFont("helvetica", 30, 1, 1)
font4 = pygame.font.Font("media/LuckiestGuy-Regular.ttf", 80)
font3 = pygame.font.SysFont("arial", 36)
font2 = pygame.font.Font("media/LuckiestGuy-Regular.ttf", 30)
font5 = pygame.font.Font("media/RubikWetPaint-Regular.ttf", 60)

# --- Clock ---
clock = pygame.time.Clock()

# --- Button Class ---
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, action=None, font=font2):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = font

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        result = None

        if self.rect.collidepoint(mouse):
            pygame.draw.rect(surface, self.hover_color, self.rect, border_radius=8)
            if click[0] == 1 and self.action is not None:
                pygame.time.delay(150)
                result = self.action()
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=8)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

        return result

# --- Game Classes ---
class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 75
        self.height = 75
        self.vel = 8
        self.health = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        if self.health > 0:
            window.blit(spaceship_img, (self.x, self.y))
            pygame.draw.rect(window, "red", (self.x, self.y + self.height, self.width, 10))
            pygame.draw.rect(window, "green",
                             (self.x, self.y + self.height, round(self.width * (self.health / 5)), 10))
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 11
        self.height = 11
        self.vel = 3
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.y -= self.vel
        window.blit(bullet, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Enemies:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.image = enemy_img[random.randint(0, 4)]
        self.direction = 1
        self.move_counter = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        self.x += self.direction
        self.move_counter += 1
        if abs(self.move_counter) > 100:
            self.direction *= -1
            self.move_counter *= self.direction
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class EnemyProjectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 13
        self.height = 13
        self.vel = 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.y += self.vel
        window.blit(enemy_bullet, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

# --- Screens ---
def start_screen():
    start_running = True

    def play_game():
        nonlocal start_running
        start_running = False

    def quit_game():
        pygame.quit()
        sys.exit()

    play_button = Button(w_width // 2 - 100, 300, 200, 60, "Play", (0, 100, 200), (0, 150, 255), action=play_game)
    quit_button = Button(w_width // 2 - 100, 400, 200, 60, "Quit", (200, 0, 0), (255, 0, 0), action=quit_game)

    while start_running:
        window.blit(start_bg, (0, 0))
        title_text = font4.render("SPACE FIGHTER", True, (255, 255, 255))
        window.blit(title_text, (w_width // 2 - title_text.get_width() // 2, 120))

        play_button.draw(window)
        quit_button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def end_screen(message, final_score=None):
    end_running = True
    result = None

    def play_again():
        nonlocal end_running, result
        result = "replay"
        end_running = False

    def quit_game():
        nonlocal end_running, result
        result = "quit"
        end_running = False

    play_button = Button(w_width // 2 - 100, 350, 200, 60, "Play Again", (0, 100, 200), (0, 150, 255),
                         action=play_again)
    quit_button = Button(w_width // 2 - 100, 430, 200, 60, "Quit", (200, 0, 0), (255, 0, 0),
                         action=quit_game)

    while end_running:
        window.blit(end_bg, (0, 0))
        text = font5.render(message, True, (255, 255, 255))
        window.blit(text, (w_width // 2 - text.get_width() // 2, 180))

        if final_score is not None:
            score_text = font3.render(f"Score: {final_score}", True, (255, 255, 255))
            window.blit(score_text, (w_width // 2 - score_text.get_width() // 2, 270))

        play_button.draw(window)
        quit_button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

    return result

# --- Main Game Loop ---
def main_game():
    score = 0
    bullets = []
    alien_bullets = []
    shoot_counter = 0
    alien_cooldown = 1000
    last_alien_shot = pygame.time.get_ticks()

    spaceship = Spaceship(w_width // 2 - 34, w_height - 100)

    enemies = [Enemies(100 + col * 100, 100 + row * 70) for row in range(4) for col in range(5)]

    running = True
    while running:
        clock.tick(60)
        window.blit(bg, (0, 0))

        # Display score
        score_text = font1.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))

        # Draw objects
        spaceship.draw(window)
        for enemy in enemies[:]:
            enemy.draw(window)
        for projectile in bullets[:]:
            projectile.draw(window)
        for ab in alien_bullets[:]:
            ab.draw(window)

        pygame.display.flip()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Enemy shooting
        time_now = pygame.time.get_ticks()
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullets) < 5 and enemies:
            attacking_alien = random.choice(enemies)
            alien_bullets.append(EnemyProjectile(attacking_alien.x + 25, attacking_alien.y + 50))
            last_alien_shot = time_now

        # Collision: enemy bullets
        for ab in alien_bullets[:]:
            if spaceship.rect.colliderect(ab.rect):
                spaceship.health -= 1
                if ab in alien_bullets:
                    alien_bullets.remove(ab)
                explosion.play()

        if spaceship.health <= 0:
            return end_screen("GAME OVER", final_score=score)

        # Collision: projectiles
        for enemy in enemies[:]:
            for proj in bullets[:]:
                if enemy.rect.colliderect(proj.rect):
                    if proj in bullets:
                        bullets.remove(proj)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    explosion2.play()
                    score += 1

        # Win condition
        if not enemies:
            return end_screen("YOU WIN!", final_score=score)

        # Cleanup bullets
        for ab in alien_bullets[:]:
            if ab.y > w_height:
                alien_bullets.remove(ab)
        for proj in bullets[:]:
            if proj.y < 0:
                bullets.remove(proj)

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship.x > 0:
            spaceship.x -= spaceship.vel
        if keys[pygame.K_RIGHT] and spaceship.x < w_width - spaceship.width:
            spaceship.x += spaceship.vel
        if keys[pygame.K_SPACE] and shoot_counter == 0:
            laser.play()
            if len(bullets) < 5:
                bullets.append(Projectile(spaceship.x + spaceship.width // 2, spaceship.y))
            shoot_counter = 1

        if shoot_counter > 0:
            shoot_counter += 1
        if shoot_counter > 10:
            shoot_counter = 0

# --- Main Loop ---
while True:
    start_screen()
    result = main_game()
    if result == "replay":
        continue
    else:
        break

pygame.quit()
