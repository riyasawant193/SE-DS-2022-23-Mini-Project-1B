from tkinter import *
from PIL import ImageTk, Image
import subprocess

# widget =GUI elements: button, textboxes,labels, images
# windows= serves as a container to hold or contain these widgets

window = Tk()  # instantiate an instance of a window
window.geometry("1000x650")
window.title("Prodigy's Pursuit- Course Outlets")

logo = PhotoImage(file='Grand Logo.png')
window.iconphoto(True, logo)
window.config(background="#E7C6FF")

window.geometry("1000x650")
img = ImageTk.PhotoImage(Image.open("Course Outlets.png"))
label = Label(window, image=img)
label.pack()
label.place(x=0, y=0)

# label = an area widget that holds text and/or an image within a window

label = Label(window,
              text="Course Outlets",
              font=('Grand Royal', 32),
              fg='#7209B7',
              bg='#EFD5ED')
label.pack()
label.place(x=10, y=20)

label = Label(window,
              text="Here are Top 5 courses you can use to grow academically",
              font=('Cambria', 20),
              fg='#7209B7',
              bg='#EFD5ED')
label.pack()
label.place(x=10, y=100)

label = Label(window,
              text="(1) MIT OpenCourseWare",
              font=('Cambria', 16),
              fg='#7209B7',
              bg='#EFD5ED')
label.pack()
label.place(x=10, y=150)

label = Label(window,
              text="(2) Coursera ",
              font=('Cambria', 16),
              fg='#7209B7',
              bg='#EFD5ED')
label.pack()
label.place(x=10, y=220)

label = Label(window,
              text="(3) edX ",
              font=('Cambria', 16),
              fg='#7209B7',
              bg='#EFD5ED')
label.pack()
label.place(x=10, y=290)

label = Label(window,
              text="4) Udacity ",
              font=('Cambria', 16),
              fg='#7209B7',
              bg='#EFD5ED')
label.pack()
label.place(x=10, y=360)

label = Label(window,
              text="(5) Udemy ",
              font=('Cambria', 16),
              fg='#7209B7',
              bg='#EFD5ED')
label.pack()
label.place(x=10, y=430)

# button = you click it, then it does stuff

count = 0


def click():
    print("You clicked the button")


def on_button_click():
    # Close the current file
    window.destroy()
    # Open the new file
    subprocess.Popen(["python", "Dashboard.py"])


button = Button(window,
                text=" ← ",
                command=on_button_click,
                font=("Montserrat", 15),
                fg="#E7C6FF",
                bg="#F72585",
                activeforeground="#E7C6FF",
                activebackground="#7209B7",
                state=ACTIVE)
button.pack()
button.place(x=950, y=10)

window.mainloop()  # place window on computer screen, lister for events
