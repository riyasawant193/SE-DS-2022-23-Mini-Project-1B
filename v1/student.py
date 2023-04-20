import customtkinter
import tkinter
from tkinter import StringVar,messagebox,ttk,NO,CENTER,END
import mysql.connector
import webbrowser
import socket
from vidstream import *
import threading
targetip = '192.168.0.100'

customtkinter.set_appearance_mode("light")

studentPage = customtkinter.CTk()
studentPage.title("studentPage")
studentPage.attributes('-fullscreen',True)

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vep4pta8xv@",
    database="world"
)
cursor = mydb.cursor()

cursor.execute("SELECT username FROM recent_users")
result = cursor.fetchone()
# Store the username in a variable
studentName = result[0] if result else None

# VideoCall
local_ip_address = socket.gethostbyname(socket.gethostname())
print(local_ip_address)

server = StreamingServer(local_ip_address, 7777)
receiver = AudioReceiver(local_ip_address, 6666)

#VIDEOCALL

# Define a function to show a message box with a given title and message
def show_message_box(title, message):
    messagebox.showinfo(title, message)

# Define functions to start the audio stream and server/receiver
def start_listening():
    try:
        # Start the video streaming server and audio receiver on new threads
        t1 = threading.Thread(target=server.start_server)
        t2 = threading.Thread(target=receiver.start_server)
        t1.start()
        t2.start()
        show_message_box("Waiting", "Waiting for connection . . .")
    except:
        # Show an error message box if the server or receiver fails to start
        show_message_box("Streaming Error", "Failed to start streaming.")
#VIDEOCALL

def open_chat():
    # Create the main chat window
    root = customtkinter.CTkToplevel()
    root.wm_attributes("-topmost", True)  # Keep root window on top
    root.title("Chat App")

    # Create a label to display the username
    username_label = customtkinter.CTkLabel(root, text=f"Logged in as: {studentName}")
    username_label.pack()

    # Create a text widget to display the chat messages
    messages = customtkinter.CTkTextbox(root)
    messages.pack()

    # Create an entry widget for the user to type their messages
    message_entry = customtkinter.CTkEntry(root)
    message_entry.pack()

    # Create a function to send the message
    def send_message():
        # Get the message from the entry widget
        message = message_entry.get()
        message_entry.delete(0,END)  # Clear the entry widget

        # Send the username and message to the server
        data = f"{studentName}: {message}"
        client_socket.send(bytes(data, "utf-8"))

    # Create a button to send the message
    send_button = customtkinter.CTkButton(root, text="Send", command=send_message)
    send_button.pack()

    # Create a function to receive messages from the server
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                messages.insert(END, message + "\n")  # Append newline character
            except:
                # If an error occurs, assume the connection has been lost
                messages.insert(END, "Lost connection to server.\n")
                client_socket.close()
                break

    # Create a function to connect to the server
    def connect_to_server():
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 12345))

        # Create a thread to receive messages
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

    # Connect to the server
    connect_to_server()

    root.mainloop()

def open_link(url):
    webbrowser.open(url)

# Define a function to retrieve data from the database and populate the treeview
def update_treeview():
    # Clear any existing data from the treeview
    treeview.delete(*treeview.get_children())
    
    # Retrieve data from the database
    query = "SELECT * FROM attendance WHERE student_name = %s"
    cursor.execute(query,(studentName,))
    rows = cursor.fetchall()

    # Populate the treeview with the data
    for row in rows:
        treeview.insert('', 'end', values=row)


# D
ScrollableFrame = customtkinter.CTkScrollableFrame(
    master = studentPage
)
ScrollableFrame.pack(fill='both', expand=True)

mainPage = customtkinter.CTkFrame(
    master = ScrollableFrame,
    height=1400
)
mainPage.pack(fill='both', expand=True)

# Fetch the content of the notice table
cursor.execute("SELECT announcement FROM notice")
result = cursor.fetchone()

noticeLable = customtkinter.CTkLabel(
    master = mainPage,
    text   = result[0],
    font   = ("Segoe UI", 32),
    width  = 1300,
    anchor = "w"
)
noticeLable.place(x=20,y=10)

AttendanceLable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "View Your Attendance",
    font   = ("Segoe UI", 32),
    width  = 1300,
    anchor = "w"
)
AttendanceLable.place(x=20,y=80)

# Create a treeview widget
treeview = ttk.Treeview(mainPage, columns=('date', 'student_name', 'subject', 'attendance'))
treeview.heading('#0', text='ID')
treeview.heading('date', text='Date')
treeview.heading('student_name', text='Student Name')
treeview.heading('subject', text='Subject')
treeview.heading('attendance', text='Attendance')
treeview.column('#0', width=0, stretch=NO)
treeview.place(x=20,y=140)
update_treeview()

GradesLable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "View Your Grades",
    font   = ("Segoe UI", 32),
    width  = 1300,
    anchor = "w"
)
GradesLable.place(x=20,y=400)

# Retrieve data from the database
query = "SELECT * FROM grades WHERE student_name = %s"
cursor.execute(query, (studentName,))
rows = cursor.fetchall()

# Create the TreeView widget
gradetree = ttk.Treeview(mainPage)
gradetree['columns'] = ('subject', 'grade', 'date')

# Define the column headings and widths
gradetree.column('#0', width=0, stretch=NO)
gradetree.column('subject', anchor=CENTER, width=100)
gradetree.column('grade', anchor=CENTER, width=50)
gradetree.column('date', anchor=CENTER, width=100)

# Set the column headings
gradetree.heading('#0', text='ID')
gradetree.heading('subject', text='Subject')
gradetree.heading('grade', text='Grade')
gradetree.heading('date', text='Date')

# Add the data rows to the TreeView
for row in rows:
    gradetree.insert('', 'end', text=row[0], values=(row[2], row[3], row[4]))

# Pack the TreeView widget into the window
gradetree.place(x=20,y=460)

Links = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Links For Self Study",
    font   = ("Segoe UI", 32),
    width  = 1300,
    anchor = "w"
)
Links.place(x=400,y=400)

dbms = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "DATABASE MANAGEMENT",
    border_width = 1,
    command =lambda: open_link("https://www.tutorialspoint.com/dbms/index.htm")
)
dbms.place(x=400,y=480)

mp = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "MICROPREOCESSOR",
    border_width = 1,
    command =lambda: open_link("https://www.tutorialspoint.com/microprocessor/index.htm")
)
mp.place(x=590,y=480)

os = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "OPERATING SYSTEM",
    border_width = 1,
    command =lambda: open_link("https://www.tutorialspoint.com/operating_system/index.htm")
)
os.place(x=400,y=520)

math = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "MATHEMATICS 4",
    border_width = 1,
    command =lambda: open_link("https://lastmomenttuitions.com/course/engineering-maths-4/")
)
math.place(x=550,y=520)

math2 = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "MATHEMATICS 3",
    border_width = 1,
    command =lambda: open_link("https://mrcet.com/downloads/digital_notes/EEE/15122022/MATHEMATICS-III%20DIGITAL%20NOTES.pdf")
)
math2.place(x=680,y=520)

aoa = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "ANALYSIS OF ALGORITHMS",
    border_width = 1,
    command =lambda: open_link("https://www.tutorialspoint.com/design_and_analysis_of_algorithms/index.htm")
)
aoa.place(x=400,y=560)

Communication = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Communication Section",
    font   = ("Segoe UI", 32),
    width  = 1300,
    anchor = "w"
)
Communication.place(x=20,y=700)

chat = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "Chat",
    border_width = 1,
    command = open_chat
)
chat.place(x=20,y=760)

listen = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "JOIN / START LISTENING",
    border_width = 1,
    command = start_listening
)
listen.place(x=160,y=760)

studentPage.mainloop()
