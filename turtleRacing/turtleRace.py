import turtle
import random
import math

win_lenght = 500
win_height = 500
turtles = 8

class Racer(object):
    def __init__(self, color, pos):
        self.pos = pos
        self.color = color
        self.turtle = turtle.Turtle()
        self.turtle.shape("turtle")
        self.turtle.penup()
        self.turtle.setpos(pos)
        self.turtle.setheading(90)
        self.turtle.color(color)

    def move(self):
        r = random.randrange(1, 20)
        self.pos = (self.pos[0], self.pos[1] + r)
        self.turtle.pendown()
        self.turtle.forward(r)

    def reset(self):
        self.turtle.penup()
        self.turtle.setpos(self.pos)

def setUpFile(name, colors):
    file = open(name, 'w')
    for color in colors:
        file.write(color + '0\n')
    file.close()

def startGame():
    tList = []
    turtle.clearscreen()
    turtle.hideturtle()
    turtle.bgcolor("cyan")
    colors = ['red','blue','green','grey','black','purple','orange','pink','yellow']
    start = -(win_lenght/2) + 20
    for t in range(turtles):
        newPos = start + t*(win_lenght) // turtles
        tList.append(Racer(colors[t],(newPos, -230)))
        tList[t].turtle.showturtle()

    run = True
    while run:
        for t in tList:
            t.move()

        maxColor = []
        maxDis = 0
        for t in tList:
            if t.pos[1] > 230 and t.pos[1] > maxDis:
                maxDis = t.pos[1]
                maxColor = []
                maxColor.append(t.color)
            elif t.pos[1] > 230 and t.pos[1] == maxDis:
                maxDis = t.pos[1]
                maxColor.append(t.color)

        if len(maxColor) > 0:
            run = False
            print('The winner is...')
            for win in maxColor:
                print(win)

        oldScore = []
        file = open('scores.txt', 'r')
        for line in file:
            l = line.split()
            color = 1[0]
            score = 1[1]
            oldScore.append([color, score])

        file.close()

        file = open('scores.txt', 'w')

        for entry in oldScore:
            for winner in maxColor:
                if entry[0] == winner:
                    entry[1] = int(entry[1]) + 1

            file.write(str(entry[0]) + ' ' + str(entry[1]) + '\n')

        file.close()

start = input('Would you like to start a new game?')
startGame()

while True:
    print('==============================')
    start = input('Would you like to keep going?')
    print(start)
    if start == 'n' or 'N'or'No'or'nO'or'no'or'NO':
        break
    startGame()