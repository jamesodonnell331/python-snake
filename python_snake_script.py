import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE  # 32
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE  # 24
BACKGROUND_COLOR = (0, 100, 0)  # Dark green
FOOD_COLOR = (0, 255, 0)  # Bright green
SNAKE_COLOR = (0, 0, 255)  # Blue

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

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
        screen.fill(BACKGROUND_COLOR)
        title_text = font.render("Snake Game", True, (255, 255, 255))
        play_text = font.render("Press P to Play", True, (255, 255, 255))
        leader_text = font.render("Press L to View Leaderboard", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        screen.blit(play_text, (SCREEN_WIDTH//2 - play_text.get_width()//2, 200))
        screen.blit(leader_text, (SCREEN_WIDTH//2 - leader_text.get_width()//2, 250))
        pygame.display.flip()

# Main Gameplay
def play_game():
    snake = [(10, 10)]  # Initial snake position
    direction = "right"
    food = get_food_position(snake)
    score = 0
    while True:
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
        # Move snake
        head = snake[0]
        if direction == "up":
            new_head = (head[0], head[1] - 1)
        elif direction == "down":
            new_head = (head[0], head[1] + 1)
        elif direction == "left":
            new_head = (head[0] - 1, head[1])
        elif direction == "right":
            new_head = (head[0] + 1, head[1])
        snake.insert(0, new_head)
        # Check if snake ate food
        if new_head == food:
            if eat_sound:
                eat_sound.play()
            score += 1
            food = get_food_position(snake)
        else:
            snake.pop()
        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in snake[1:]):  # Collision with self
            if gameover_sound:
                gameover_sound.play()
            return score
        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        for segment in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, FOOD_COLOR, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(10)  # Snake moves 10 times per second

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
        screen.fill(BACKGROUND_COLOR)
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
        screen.fill(BACKGROUND_COLOR)
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