import turtle
import os
import math
import random
import platform


if platform.system()=="Windows":
    try:
        import windsound
    except:
        print("Modulo winsound non trovato o non riproducibile")

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Retro Game: Space Invaders")
wn.bgpic("space_invaders_background.gif")#sfondo
wn.tracer(0)

wn.register_shape("invader.gif")#immagine dei nemici
wn.register_shape("player.gif")#immagine del giocatore

border_pen=turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#Impostare lo score
score=0
#visualizzare lo score
score_pen=turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,280)
scorestring="Score: {}".format(score)
score_pen.write(scorestring,False,align="left",font=("Arial",14,"normal"))
score_pen.hideturtle()

#creazione della turtle del giocatore
player= turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0 )
player.setposition(0,-250)
player.setheading(90)
player.speed=0

#Creazione dei nemici
number_of_enemies=30
enemies=[]

for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

enemy_start_x=-225
enemy_start_y=250
enemy_number=0

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x= enemy_start_x+(50*enemy_number)
    y= enemy_start_y
    enemy.setposition(x,y)
    enemy_number+=1
    if enemy_number==10:
        enemy_start_y-=50
        enemy_number=0

enemyspeed=0.13


#creazione dei proiettili del giocatore
bullet=turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed=5

#Definizione dello stato dei proiettili
# ready -  ponto al fuoco
# fire - proiettile sparato
bulletstate="ready"


def move_left():
    player.speed=-0.5

def move_right():
    player.speed=0.5


def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    global bulletstate
    if bulletstate=="ready":
        play_sound("laser.mav")
        bulletstate="fire"
        #movimento del proiettile da sopra il giocatore
        x=player.xcor()
        y=player.ycor()+10
        bullet.setposition(x,y)
        bullet.showturtle()

def isCollision(t1,t2):
    distance=math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance<15:
        return True
    else:
        return False

def play_sound(sound_file,time=0):
    #Windows
    if platform.system=="Windows":
        windsound.PlaySound(sound_file,winsound.SND_ASYNC)
    #Linux
    elif platform.system()=="Linux":
        os.system("aplay -q{}&".format(sound_file))
    #Mac
    elif platform.system()=="macOS":
        os.system("afplay {}&".format(sound_file))
    if time>0:
        turtle.ontimer(lambda: play_sound(sound_file,time), t=int(time*1000))

wn.listen()
wn.onkey(move_left,"Left")
wn.onkey(move_right,"Right")
wn.onkey(fire_bullet,"space")

#Musica in background
play_sound("bgm.mp3",119)

while True:
    wn.update()
    move_player()
    for enemy in enemies:

        #Movimento dei nemici
        x=enemy.xcor()
        x+=enemyspeed
        enemy.setx(x)

        #Movimento dei nemici indietro e giù
        if enemy.xcor()>280:
            for e in enemies:
                y=e.ycor()
                y-=40
                e.sety(y)
            enemyspeed*=-1
        if enemy.xcor()<-280:
            for e in enemies:
                y=e.ycor()
                y-=40
                e.sety(y)
            enemyspeed *= -1

        # controllo della collisione tra il proiettile e il nemico
        if isCollision(bullet, enemy):
            play_sound("explosion.wav")

            # Resetta il proiettile
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)

            # Resetta il nemico

            enemy.setposition(0, 10000)

            #Aggiornamento dello score
            score+=10
            scorestring="Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

        # Controllo collisione tra giocatore e nemico
        if isCollision(player, enemy):
            play_sound("explosion.wav")
            palyer.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break

    #Muovere il proiettile
    if bulletstate=="fire":
        y=bullet.ycor()
        y+=bulletspeed
        bullet.sety(y)

    #controllo se il proiettile è andato fino in alto
    if bullet.ycor()>275:
        bullet.hideturtle()
        bulletstate="ready"





























