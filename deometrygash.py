import pygame
import time
import random
import turtle

# Initialize pygame mixer for music (safe load)
try:
    pygame.mixer.init()
    pygame.mixer.music.load("c:/Users/ketin/Downloads/313d9220-7843-45b3-a85c-5beef813a30b.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Music failed to load:", e)

# Screen setup
win = turtle.Screen()
time.sleep(0.1)
win.title("Deometry Gash")
win.bgcolor("cyan")
win.setup(width=800, height=400)
win.tracer(0)

# Background squares
background_squares = []
for _ in range(30):
    square = turtle.Turtle()
    square.shape("square")
    square.color("dark cyan")
    square.shapesize(stretch_wid=1, stretch_len=1)
    square.penup()
    x = random.randint(-400, 400)
    y = random.randint(-50, 180)
    square.goto(x, y)
    background_squares.append(square)

# Ground squares
ground_squares = []
for x in range(-400, 400, 40):
    square = turtle.Turtle()
    square.shape("square")
    square.color("dark cyan")
    square.shapesize(stretch_wid=1, stretch_len=2)
    square.penup()
    square.goto(x + 20, -110)
    ground_squares.append(square)

# Progress display
progress = 0
last_progress_time = time.time()
progress_display = turtle.Turtle()
progress_display.hideturtle()
progress_display.penup()
progress_display.color("black")
progress_display.goto(-380, 160)
progress_display.write(f"Progress: {progress}%", font=("Calibri", 16, "normal"))

# High score display
high_score = 0
high_score_display = turtle.Turtle()
high_score_display.hideturtle()
high_score_display.penup()
high_score_display.color("black")
high_score_display.goto(-380, 130)
high_score_display.write(f"High Score: {high_score}%", font=("Calibri", 16, "normal"))

# Attempts display
attempts = 1
attempts_display = turtle.Turtle()
attempts_display.hideturtle()
attempts_display.penup()
attempts_display.color("black")
attempts_display.goto(-380, 100)
attempts_display.write(f"Attempt: {attempts}", font=("Calibri", 16, "normal"))

# Player setup
player = turtle.Turtle()
player.shape("square")
player.color("black")
player.penup()
player.goto(-250, -100)
player.dy = 0
player.gravity = -0.45
player.jump_strength = 9
is_jumping = False

# Obstacle class
class Obstacle(turtle.Turtle):
    def __init__(self, x):
        super().__init__()
        self.shape("triangle")
        self.setheading(90)
        self.color("black")
        self.penup()
        self.shapesize(stretch_wid=2.2, stretch_len=2.2)
        self.goto(x, -98)
        self.passed = False

    def move(self):
        self.setx(self.xcor() - 5)
        if self.xcor() < -400:
            self.setx(random.randint(400, 800))
            self.passed = False

# Block class
class Block(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("square")
        self.color("black")
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.goto(x, y)
        self.visible = False
        self.hideturtle()

    def move(self):
        self.setx(self.xcor() - 5)
        if self.xcor() < -400:
            self.hideturtle()
            self.visible = False
        else:
            self.showturtle()

# Stack of blocks
blocks = []
stack_x = 900
block_height = 20
num_blocks = 2
for i in range(num_blocks):
    block = Block(stack_x, -100 + i * block_height)
    blocks.append(block)
    block.goto(block.xcor(), -500)

# Obstacles
obstacles = [Obstacle(x) for x in range(400, 1000, 300)]
passed_obstacles = 0

# Jump function
def jump():
    global is_jumping
    if not is_jumping:
        player.dy = player.jump_strength
        is_jumping = True

# Restart cooldown management
last_restart_time = 0  # global cooldown timer

def try_restart_game(x=None, y=None):
    global last_restart_time
    current = time.time()
    if current - last_restart_time >= 0.5:  # 0.5 second cooldown
        restart_game()
        last_restart_time = current

win.onscreenclick(try_restart_game, 1)

# Restart game function
def restart_game(x=None, y=None):  # Accepts optional args for onclick
    global progress, passed_obstacles, is_jumping, game_over, attempts
    # Reset game variables
    progress = 0
    passed_obstacles = 0
    is_jumping = False
    game_over = False
    attempts += 1

    # Reset player
    player.goto(-250, -100)
    player.dy = 0
    player.showturtle()

    # Reset obstacles
    for i, obstacle in enumerate(obstacles):
        obstacle.goto(400 + i*300, -98)
        obstacle.passed = False
        obstacle.showturtle()

    # Reset blocks
    for block in blocks:
        block.hideturtle()
        block.visible = False
        block.goto(block.xcor(), -500)

    # Clear and rewrite progress, attempts displays
    progress_display.clear()
    progress_display.write(f"Progress: {progress}%", font=("Calibri", 16, "normal"))
    attempts_display.clear()
    attempts_display.write(f"Attempt: {attempts}", font=("Calibri", 16, "normal"))

    # Hide any game over or win messages
    for t in win.turtles():
        if getattr(t, "is_game_message", False):
            t.clear()
            t.hideturtle()

    # Restart music
    try:
        pygame.mixer.music.play(-1)
    except:
        pass

# Controls
win.listen()
win.onkeypress(jump, "space")
win.onkeypress(jump, "Up")
win.onkeypress(jump, "w")
win.onclick(lambda x, y: jump())

# Game over flag
game_over = False

# Removed show_game_over function completely

# Main game loop
while True:
    win.update()
    time.sleep(0.005)

    if game_over:
        continue

    for obstacle in obstacles:
        obstacle.move()
        if obstacle.xcor() < player.xcor() and not obstacle.passed:
            passed_obstacles += 1
            obstacle.passed = True
        if player.distance(obstacle) < 25:
            print("Game Over! Hit a spike.")
            if progress > high_score:
                high_score = progress
                high_score_display.clear()
                high_score_display.write(f"High Score: {high_score}%", font=("Calibri", 16, "normal"))
            
            game_over = True
            pygame.mixer.music.stop()
            for obstacle in obstacles:
                obstacle.hideturtle()
            for block in blocks:
                block.hideturtle()
            player.hideturtle()

            time.sleep(0.5)
            restart_game()
            break

    if passed_obstacles >= 3:
        if not blocks[0].visible:
            base_y = -100
            for i, block in enumerate(blocks):
                block.goto(stack_x, base_y + i * block_height)
                block.visible = True
                block.showturtle()
        for block in blocks:
            block.move()

    player.dy += player.gravity
    y = player.ycor() + player.dy

    landed_on_block = False
    for block in blocks:
        if not block.visible:
            continue

        px, py = player.xcor(), player.ycor()
        bx, by = block.xcor(), block.ycor()
        block_width = 40
        block_height = 20

        dx = abs(px - bx)
        dy = py - by

        if dx < block_width / 2 and 0 <= dy <= 20 and player.dy <= 0:
            y = by + 20
            player.dy = 0
            is_jumping = False
            landed_on_block = True
            break
        elif dy < 20 and dy > -20 and dx >= block_width / 2 and dx < (block_width / 2 + 10):
            print("Game Over! Hit block side.")
            if progress > high_score:
                high_score = progress
                high_score_display.clear()
                high_score_display.write(f"High Score: {high_score}%", font=("Calibri", 16, "normal"))
            
            game_over = True
            pygame.mixer.music.stop()
            for obstacle in obstacles:
                obstacle.hideturtle()
            for block in blocks:
                block.hideturtle()
            player.hideturtle()

            time.sleep(0.5)
            restart_game()
            break
        elif dy < 0 and dx < block_width / 2 and abs(dy) < block_height:
            print("Game Over! Hit block from below.")
            if progress > high_score:
                high_score = progress
                high_score_display.clear()
                high_score_display.write(f"High Score: {high_score}%", font=("Calibri", 16, "normal"))
            
            game_over = True
            pygame.mixer.music.stop()
            for obstacle in obstacles:
                obstacle.hideturtle()
            for block in blocks:
                block.hideturtle()
            player.hideturtle()

            time.sleep(0.5)
            restart_game()
            break

    if y <= -100 and not landed_on_block:
        y = -100
        player.dy = 0
        is_jumping = False

    player.sety(y)

    current_time = time.time()
    if current_time - last_progress_time >= 10 and progress < 100:
        progress += 1
        last_progress_time = current_time
        progress_display.clear()
        progress_display.write(f"Progress: {progress}%", font=("Calibri", 16, "normal"))

        # Update high score live
        if progress > high_score:
            high_score = progress
            high_score_display.clear()
            high_score_display.write(f"High Score: {high_score}%", font=("Calibri", 16, "normal"))

        if progress == 100:
            # Show win message
            pygame.mixer.music.stop()
            win_text = turtle.Turtle()
            win_text.hideturtle()
            win_text.penup()
            win_text.color("green")
            win_text.goto(0, 0)
            win_text.write("LEVEL COMPLETE", align="center", font=("Calibri", 30, "bold"))
            win_text.is_game_message = True

            game_over = True

    # Update attempts display live
    attempts_display.clear()
    attempts_display.write(f"Attempt: {attempts}", font=("Calibri", 16, "normal"))
