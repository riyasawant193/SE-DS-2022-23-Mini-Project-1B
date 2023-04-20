from tkinter import *
from PIL import ImageTk, Image

#widget =GUI elements: button, textboxes,labels, images
#windows= serves as a comtainer to hold or contain these widgets

window = Tk() #instantiate an instance of a window
window.geometry("1000x650")
window.title("Prodigy's Pursuit- Explore Fields")

logo = PhotoImage(file='Grand Logo.png')
window.iconphoto(True,logo)
window.config(background="#E7C6FF")

window.geometry("1000x650")
img = ImageTk.PhotoImage(Image.open("expdesign.png"))
label = Label(window,image = img )
label.pack()
label.place(x=0,y=0)



#label = an area widget that holds text and/or an image within a window

label = Label(window,
              text="Explore Fields",
              font=('Grand Royal',32),
              fg='#7209B7',
              bg='#E7C6FF')
label.pack()
label.place(x=10,y=10)

label = Label(window,
              text="There are many different fields of engineering, each with its own specialties\n and applications. Here are some of the top engineering fields:",
              font=('Cambria',20),
              fg='#7209B7',
              bg='#E7C6FF')
label.pack()
label.place(x=10,y=80)

label = Label(window,
              text="Data Science engineer:\nThe art of designing and building\nadvanced data processing systems that can handle\nand extract insights from large and complex data sets.\nAverage Salary: 10 LPA",
              font=('Grand Royal',20),
              justify='left',
              fg='#7209B7',
              bg='#E7C6FF')
label.pack()
label.place(x=10,y=150)

label = Label(window,
              text="AI-ML engineer:\nA person in IT who focuses on researching, building\n and designingself-running artificial intelligence (AI)\nsystems to automate predictive models.\nAverage Salary: 7 LPA",
              font=('Grand Royal',20),
              justify='left',
              fg='#7209B7',
              bg='#E7C6FF')
label.pack()
label.place(x=10,y=320)

# button = you click it, then it does stuff

count = 0



window.mainloop() #place window on computer screen, lister for events

