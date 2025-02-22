import pygame
import sys
import random
import math

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE  # 32
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE  # 24
BACKGROUND_COLOR = (0, 100, 0)  # Dark green (used as fallback)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load images (assumes they are in the same directory)
background_img = pygame.image.load('background.png').convert()
snake_segment_img = pygame.image.load('snake_segment.png').convert_alpha()
food_img = pygame.image.load('food.png').convert_alpha()

# Load sound effects (assuming files exist; if not, sounds are skipped)
try:
    eat_sound = pygame.mixer.Sound("food_G1U6tbb.mp3")
    gameover_sound = pygame.mixer.Sound("gameoversnake.mp3")
except pygame.error:
    print("Warning: Sound files not found. Continuing without sound.")
    eat_sound = None
    gameover_sound = None

# Function to generate food position not overlapping with snake
def get_food_position(snake):
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            return (x, y)

# Function to save score to leaderboard
def save_score(score):
    try:
        with open("leaderboard.txt", "r") as f:
            scores = [int(line.strip()) for line in f]
    except FileNotFoundError:
        scores = []
    scores.append(score)
    scores.sort(reverse=True)
    top_scores = scores[:5]
    with open("leaderboard.txt", "w") as f:
        for s in top_scores:
            f.write(f"{s}\n")

# Draw background
def draw_background():
    for x in range(0, SCREEN_WIDTH, background_img.get_width()):
        for y in range(0, SCREEN_HEIGHT, background_img.get_height()):
            screen.blit(background_img, (x, y))

# Home Screen
def home_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "play"
                if event.key == pygame.K_l:
                    return "leaderboard"
        draw_background()
        title_text = font.render("Snake Game", True, (255, 255, 255))
        play_text = font.render("Press P to Play", True, (255, 255, 255))
        leader_text = font.render("Press L to View Leaderboard", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        screen.blit(play_text, (SCREEN_WIDTH//2 - play_text.get_width()//2, 200))
        screen.blit(leader_text, (SCREEN_WIDTH//2 - leader_text.get_width()//2, 250))
        pygame.display.flip()

# Main Gameplay
def play_game():
    snake_grid = [(10, 10)]  # Logical grid positions
    previous_snake_grid = [(10, 10)]  # Positions before last move
    direction = "right"
    food = get_food_position(snake_grid)
    score = 0
    move_timer = 0.0
    move_interval = 0.08  # Snake moves every 0.1 seconds
    particles = []  # List for particle effects
    floating_texts = []  # List for floating score text

    while True:
        delta_time = clock.tick(60) / 1000.0  # 60 FPS, delta_time in seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                elif event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"

        # Update move timer and perform logical move if needed
        move_timer += delta_time
        if move_timer >= move_interval:
            previous_snake_grid = snake_grid.copy()
            head = snake_grid[0]
            if direction == "up":
                new_head = (head[0], head[1] - 1)
            elif direction == "down":
                new_head = (head[0], head[1] + 1)
            elif direction == "left":
                new_head = (head[0] - 1, head[1])
            elif direction == "right":
                new_head = (head[0] + 1, head[1])

            # Check if snake ate food
            if new_head == food:
                if eat_sound:
                    eat_sound.play()
                score += 1
                snake_grid.insert(0, new_head)
                # Add particles
                food_pixel_pos = (food[0] * CELL_SIZE + CELL_SIZE / 2, food[1] * CELL_SIZE + CELL_SIZE / 2)
                for _ in range(10):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(50, 150)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    particles.append([food_pixel_pos[0], food_pixel_pos[1], vx, vy, 1.0])
                # Add floating text
                floating_texts.append([food_pixel_pos[0], food_pixel_pos[1], "+1", 1.0])
                food = get_food_position(snake_grid)
            else:
                snake_grid.insert(0, new_head)
                snake_grid.pop()
            move_timer -= move_interval

            # Check for collisions
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake_grid[1:]):
                if gameover_sound:
                    gameover_sound.play()
                return score

        # Update particles
        for p in particles:
            p[0] += p[2] * delta_time  # Update x position
            p[1] += p[3] * delta_time  # Update y position
            p[4] -= delta_time         # Decrease lifetime
        particles = [p for p in particles if p[4] > 0]

        # Update floating texts
        for ft in floating_texts:
            ft[1] -= 50 * delta_time  # Move up 50 pixels per second
            ft[3] -= delta_time       # Decrease lifetime
        floating_texts = [ft for ft in floating_texts if ft[3] > 0]

        # Draw everything
        draw_background()
        progress = min(move_timer / move_interval, 1.0)
        for i in range(len(snake_grid)):
            if i < len(previous_snake_grid):
                start_x = previous_snake_grid[i][0] * CELL_SIZE
                start_y = previous_snake_grid[i][1] * CELL_SIZE
            else:
                start_x = previous_snake_grid[-1][0] * CELL_SIZE
                start_y = previous_snake_grid[-1][1] * CELL_SIZE
            end_x = snake_grid[i][0] * CELL_SIZE
            end_y = snake_grid[i][1] * CELL_SIZE
            visual_x = start_x + progress * (end_x - start_x)
            visual_y = start_y + progress * (end_y - start_y)
            screen.blit(snake_segment_img, (int(visual_x), int(visual_y)))
        screen.blit(food_img, (food[0] * CELL_SIZE, food[1] * CELL_SIZE))
        for p in particles:
            if p[4] > 0:
                pygame.draw.circle(screen, (255, 255, 0), (int(p[0]), int(p[1])), 3)
        for ft in floating_texts:
            if ft[3] > 0:
                text_surface = font.render(ft[2], True, (255, 255, 0))
                screen.blit(text_surface, (ft[0] - text_surface.get_width() // 2, ft[1]))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

# Leaderboard Screen
def leaderboard():
    try:
        with open("leaderboard.txt", "r") as f:
            scores = [int(line.strip()) for line in f]
    except FileNotFoundError:
        scores = []
    scores.sort(reverse=True)
    top_scores = scores[:5]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    return "home"
        draw_background()
        title_text = font.render("Leaderboard", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        for i, score in enumerate(top_scores):
            score_text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 150 + i*50))
        back_text = font.render("Press H to Home", True, (255, 255, 255))
        screen.blit(back_text, (SCREEN_WIDTH//2 - back_text.get_width()//2, 150 + len(top_scores)*50 + 50))
        pygame.display.flip()

# Game Over Screen
def game_over_screen(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    return "home"
        draw_background()
        game_over_text = font.render("Game Over!", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        home_text = font.render("Press H to Home", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 100))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 150))
        screen.blit(home_text, (SCREEN_WIDTH//2 - home_text.get_width()//2, 200))
        pygame.display.flip()

# Main Game Loop
current_state = "home"
while True:
    if current_state == "home":
        current_state = home_screen()
    elif current_state == "play":
        score = play_game()
        save_score(score)
        current_state = "game_over"
    elif current_state == "leaderboard":
        current_state = leaderboard()
    elif current_state == "game_over":
        current_state = game_over_screen(score)