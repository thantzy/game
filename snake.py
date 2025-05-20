import turtle
import time
import random

# Setup window
win = turtle.Screen()
win.title("🐍 Snake Snack - K1")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0)

# Global state
game_running = False
game_over = False
score = 0
high_score = 0
segments = []

# Kepala ular
head = turtle.Turtle()
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 100)
head.direction = "stop"

# Makanan 1: Apel
food1 = turtle.Turtle()
food1.shape("circle")
food1.color("red")
food1.penup()

# Makanan 2: Pisang
food2 = turtle.Turtle()
food2.shape("square")
food2.color("yellow")
food2.penup()

# Teks skor
pen = turtle.Turtle()
pen.speed(0)
pen.penup()
pen.hideturtle()

# Tombol
start_btn = turtle.Turtle()
restart_btn = turtle.Turtle()
for btn in [start_btn, restart_btn]:
    btn.hideturtle()
    btn.penup()
    btn.speed(0)

# ---------- FUNGSI ----------

def draw_button(t, text, pos, width=200, height=50, fill_color="lightblue"):
    x, y = pos
    t.clear()
    t.goto(x - width/2, y - height/2)
    t.color("white", fill_color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()

    # Outline
    t.goto(x - width/2, y - height/2)
    t.pendown()
    t.pensize(2)
    t.color("white")
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.penup()

    # Text
    t.goto(x, y - 10)
    t.color("black")
    t.write(text, align="center", font=("Courier", 16, "bold"))

def safe_food_position():
    while True:
        x = random.randint(-270, 270)
        y = random.randint(-270, 270)
        if y > -100:
            return x, y

def update_score():
    pen.clear()

    pen.goto(-180, 270)
    pen.color("white")
    pen.begin_fill()
    for _ in range(2):
        pen.forward(360)   # lebar kotak diperpanjang dari 300 ke 360
        pen.right(90)
        pen.forward(30)
        pen.right(90)
    pen.end_fill()

    pen.goto(2, 248)
    pen.color("white")
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 18, "bold"))

    pen.goto(0, 250)
    pen.color("black")
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 18, "bold"))


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"


def start_game():
    global game_running, game_over, score, segments
    if not game_running:
        start_btn.clear()
        restart_btn.clear()
        game_running = True
        game_over = False
        head.goto(0, 100)
        head.direction = "stop"
        food1.goto(safe_food_position())
        food2.goto(safe_food_position())

        for s in segments:
            s.goto(1000, 1000)
        segments.clear()
        score = 0
        update_score()
        game_loop()

def reset_game():
    global game_running, game_over, high_score
    game_running = False
    game_over = True
    food1.goto(1000, 1000)
    food2.goto(1000, 1000)
    draw_button(restart_btn, "Restart", (0, -130), fill_color="orange")

def on_click(x, y):
    if -100 < x < 100 and -145 < y < -95 and not game_running and not game_over:
        start_game()
    elif -100 < x < 100 and -155 < y < -105 and game_over:
        restart_btn.clear()
        start_game()

def game_loop():
    global score, high_score, game_running
    delay = 0.1
    while game_running:
        win.update()

        # Tabrak dinding
        if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
            reset_game()
            break

        # Makan food1 (apel)
        if head.distance(food1) < 20:
            food1.goto(safe_food_position())
            segment = turtle.Turtle()
            segment.shape("square")
            segment.color("lightgreen")
            segment.penup()
            segments.append(segment)
            score += 10
            if score > high_score:
                high_score = score
            update_score()

        # Makan food2 (pisang)
        if head.distance(food2) < 20:
            food2.goto(safe_food_position())
            segment = turtle.Turtle()
            segment.shape("square")
            segment.color("lightgreen")
            segment.penup()
            segments.append(segment)
            score += 15
            if score > high_score:
                high_score = score
            update_score()

        # Gerakkan tubuh
        for i in range(len(segments)-1, 0, -1):
            segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
        if segments:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # Cek tabrakan dengan badan
        for s in segments:
            if s.distance(head) < 20:
                reset_game()
                return

        time.sleep(delay)

# Control
win.listen()
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")
win.onscreenclick(on_click)


# Show start button
draw_button(start_btn, "Start Game", (0, -120), fill_color="green")

turtle.done()
