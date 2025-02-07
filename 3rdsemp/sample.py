import turtle
import time
screen = turtle.Screen()
screen.title("Access Granted")
screen.bgcolor("white")

text_turtle = turtle.Turtle()
text_turtle.speed(1)  

font = ("Arial", 16, "bold")

text_turtle.penup()
text_turtle.goto(0, 50)
text_turtle.pendown()
text_turtle.color("black")
text_turtle.write("Face Recognized", align="center", font=font)

text_turtle.penup()
text_turtle.goto(-40, 0)
text_turtle.pendown()
text_turtle.color("green")
text_turtle.width(10)
text_turtle.setheading(315)
text_turtle.forward(40)
text_turtle.setheading(45)
text_turtle.forward(60)

text_turtle.penup()
text_turtle.goto(0, -60)
text_turtle.pendown()
text_turtle.color("blue")
text_turtle.write("Access Granted", align="center", font=font)

text_turtle.hideturtle()

time.sleep(10)
screen.bye()
