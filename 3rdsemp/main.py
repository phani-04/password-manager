import face_recognition as fr
import cv2
import numpy as np
import os
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import turtle
import time
import speech_recognition as sr

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def show_data():
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
            # Create a new window to display the data
            data_window = Toplevel(window)
            data_window.title("Stored Data")
            data_window.config(padx=20, pady=20)
            
            # Create a text widget to display the data
            data_text = Text(data_window, height=10, width=40)
            data_text.pack()
            
            # Insert the data into the text widget
            data_text.insert(INSERT, "Stored Data:\n\n")
            for website, info in data.items():
                data_text.insert(INSERT, f"Website: {website}\n")
                data_text.insert(INSERT, f"Email: {info['email']}\n")
                data_text.insert(INSERT, f"Password: {info['password']}\n\n")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")

def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")
# Path to the directory containing known face images
path = "./train/"

known_names = []
known_name_encodings = []

images = os.listdir(path)
for _ in images:
    image = fr.load_image_file(path + _)
    image_path = path + _
    encoding = fr.face_encodings(image)[0]

    known_name_encodings.append(encoding)
    known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())

# Open the camera for capturing video
camera = cv2.VideoCapture(0)  
recognized_person = "Phani"  

while True:
    ret, frame = camera.read()
    if not ret:
        break

    face_locations = fr.face_locations(frame)
    face_encodings = fr.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        name = ""

        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)

        if matches[best_match]:
            name = known_names[best_match]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if name == recognized_person:
            cv2.putText(frame, "Recognized Phani! Stopping...", (10, 30), font, 1.0, (0, 255, 0), 2)
            cv2.imshow("Live Face Recognition", frame)
            camera.release()
            cv2.destroyAllWindows()

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

            time.sleep(3)
            screen.bye()

            # # Initialize the recognizer
            # recognizer = sr.Recognizer()

            # # Define a function to listen for speech
            # def listen_for_command():
            #     with sr.Microphone() as source:
            #         print("Listening for command...")
            #         try:
            #             audio = recognizer.listen(source, timeout=None)  # Listen indefinitely
            #             command = recognizer.recognize_google(audio)
            #             print("You said:", command)
            #             return command
            #         except sr.UnknownValueError:
            #             print("Sorry, I could not understand what you said.")
            #             return None

            # # Run an infinite loop listening for the command "its me"
            # while True:
            #     command = listen_for_command()
            #     if command and "allow" in command.lower():
            #         print("Terminating the loop.")
            #         break





            window = Tk()
            window.title("Password Manager")
            window.config(padx=50, pady=50)

            canvas = Canvas(height=200, width=200)
            logo_img = PhotoImage(file="logo.png")
            canvas.create_image(100, 100, image=logo_img)
            canvas.grid(row=0, column=1)

            #Labels
            website_label = Label(text="Website:")
            website_label.grid(row=1, column=0)
            email_label = Label(text="Email/Username:")
            email_label.grid(row=2, column=0)
            password_label = Label(text="Password:")
            password_label.grid(row=3, column=0)

            #Entries
            website_entry = Entry(width=21)
            website_entry.grid(row=1, column=1)
            website_entry.focus()
            email_entry = Entry(width=35)
            email_entry.grid(row=2, column=1, columnspan=2)
            email_entry.insert(0, "phanindhra@gmail.com")
            password_entry = Entry(width=21)
            password_entry.grid(row=3, column=1)

            # Buttons
            search_button = Button(text="Search", width=13, command=find_password)
            search_button.grid(row=1, column=2)
            generate_password_button = Button(text="Generate Password", command=generate_password)
            generate_password_button.grid(row=3, column=2)
            add_button = Button(text="Add", width=36, command=save)
            add_button.grid(row=4, column=1, columnspan=2)
            data_button = Button(text="Data", width=36, command=show_data)
            data_button.grid(row=5, column=1, columnspan=2, pady=(10, 0))

            window.mainloop()
            
            exit(0)

    cv2.imshow("Live Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break

camera.release()
cv2.destroyAllWindows()
