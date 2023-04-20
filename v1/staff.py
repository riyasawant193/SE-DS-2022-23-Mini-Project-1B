import customtkinter
import tkinter
from tkinter import StringVar,messagebox,ttk,NO,CENTER,END
import mysql.connector
import datetime
from vidstream import *
import socket
import threading
targetIp = '192.168.0.100'

# VIDEOCALL
# Get the local IP address of the machine
local_ip_address = socket.gethostbyname(socket.gethostname())
print(local_ip_address)

# Create server and receiver objects for video and audio streaming
server = StreamingServer(local_ip_address, 9999)
receiver = AudioReceiver(local_ip_address, 8888)

def start_listening():
    t1 = threading.Thread(target=server.start_server)
    t2 = threading.Thread(target=receiver.start_server)
    t1.start()
    t2.start()

# Define a function to show a message box with a given title and message
def show_message_box(title, message):
    messagebox.showinfo(title, message)

# Define functions to start the video and screen sharing streams
def start_camera_stream():
    try:
        # Create a camera client object and start the camera stream on a new thread
        camera_client = CameraClient(targetIp, 7777)
        t3 = threading.Thread(target=camera_client.start_stream)
        t3.start()

        # Show a success message box
        show_message_box("Camera Stream", "Started camera stream successfully!")
    except:
        # Show an error message box if the camera stream fails to start
        show_message_box("Camera Stream Error", "Failed to start camera stream.")

def start_screen_sharing():
    try:
        # Create a screen share client object and start the screen sharing stream on a new thread
        screen_client = ScreenShareClient(targetIp, 7777)
        t4 = threading.Thread(target=screen_client.start_stream)
        t4.start()

        # Show a success message box
        show_message_box("Screen Sharing", "Started screen sharing successfully!")
    except:
        # Show an error message box if the screen sharing stream fails to start
        show_message_box("Screen Sharing Error", "Failed to start screen sharing.")

def start_audio_sharing():
    try:
        # Create an audio sender object and start the audio stream on a new thread
        audio_sender = AudioSender(targetIp, 6666)
        t4 = threading.Thread(target=audio_sender.start_stream)
        t4.start()
    except:
        # Show an error message box if the audio stream fails to start
        show_message_box("Audio Stream Error", "Failed to start audio stream.")
# VIDEO CALL

customtkinter.set_appearance_mode("light")

staffPage = customtkinter.CTk()
staffPage.title("staffPage")
staffPage.attributes('-fullscreen',True)

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vep4pta8xv@",
    database="world"
)
cursor = mydb.cursor()

# Get today's date
today = datetime.date.today().isoformat()

def open_chat():
    # Create the main chat window
    root = customtkinter.CTkToplevel()
    root.wm_attributes("-topmost", True)  # Keep root window on top
    root.title("Chat App")

    # Create a label to display the username
    username_label = customtkinter.CTkLabel(root, text=f"Logged in as: {username}")
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
        data = f"{username}: {message}"
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

def sort_grades():
    # Get selected sorting option from ComboBox
    sort_option = sort.get()
    print("Sorting option selected:", sort_option)

    # Remove existing items from Treeview widget
    gradestree.delete(*gradestree.get_children())

    # Retrieve data from database and insert into Treeview widget based on sorting option
    if sort_option == "ID":
        cursor.execute("SELECT * FROM grades ORDER BY id ASC")
    elif sort_option == "Student Name":
        cursor.execute("SELECT * FROM grades ORDER BY student_name ASC")
    elif sort_option == "Subject":
        cursor.execute("SELECT * FROM grades ORDER BY subject ASC")
    elif sort_option == "Grade":
        cursor.execute("SELECT * FROM grades ORDER BY grade ASC")
    elif sort_option == "Date":
        cursor.execute("SELECT * FROM grades ORDER BY date ASC")
    else:
        cursor.execute("SELECT * FROM grades")
    
    # Debugging statement to check number of rows returned
    rows = cursor.fetchall()
    print("Number of rows returned:", len(rows))

    for row in rows:
        gradestree.insert("", "end", values=row)


def update_grades():
    # Get selected item in Treeview widget
    selection = gradestree.selection()
    if len(selection) == 1:
        # Get data for selected item
        item = gradestree.item(selection[0])
        values = item["values"]

        # Get existing subjects for selected item
        subjects = values[2].split(",") if values[2] else []

        # Get updated grade from ComboBox
        updated_grade = grades.get()

        # Update grade column for selected item
        grade_text = updated_grade
        gradestree.item(selection[0], values=(values[0], values[1], values[2], grade_text, datetime.date.today()))

        # Update database
        cursor.execute("UPDATE grades SET grade = %s, date = %s WHERE id = %s", (grade_text, datetime.date.today(), values[0]))
        mydb.commit()

def add_grades():
    # Get student name and grade from ComboBoxes
    student_name = students.get()
    grade = grades.get()

    # Add new row to Treeview widget
    gradestree.insert(parent="", index="end", values=(None, student_name, subjectName.get(), grade, today))

    # Insert new row into MySQL table
    cursor.execute("INSERT INTO grades (student_name, subject, grade, date) VALUES (%s, %s, %s, %s)", (student_name, subjectName.get(), grade, today))
    mydb.commit()

def mark_absent():
    # Get selected item in Treeview widget
    selection = treeview.selection()
    if len(selection) == 1:
        # Get data for selected item
        item = treeview.item(selection[0])
        values = item["values"]

        # Get existing subjects for selected item
        subjects = values[2].split(",") if values[2] else []

        # Add new subject to list of subjects
        new_subject = subjectAttendance.get()
        if new_subject not in subjects:
            subjects.append(f"Abs({new_subject})")

        # Update subject and attendance columns for selected item
        subject_text = ",".join(subjects)
        treeview.item(selection[0], values=(values[0], values[1], subject_text, "Absent"))

        # Update database
        cursor.execute("UPDATE attendance SET subject = %s, attendance = %s WHERE date = %s AND student_name = %s", (subject_text, "Absent", values[0], values[1]))
        db.commit()

def mark_present():
    # Get selected item in Treeview widget
    selection = treeview.selection()
    if len(selection) == 1:
        # Get data for selected item
        item = treeview.item(selection[0])
        values = item["values"]

        # Get existing subjects for selected item
        subjects = values[2].split(",") if values[2] else []

        # Add new subject to list of subjects
        new_subject = subjectAttendance.get()
        if new_subject not in subjects:
            subjects.append(new_subject)

        # Update subject and attendance columns for selected item
        subject_text = ",".join(subjects)
        treeview.item(selection[0], values=(values[0], values[1], subject_text, "Present"))

        # Update database
        cursor.execute("UPDATE attendance SET subject = %s, attendance = %s WHERE date = %s AND student_name = %s", (subject_text, "Present", values[0], values[1]))
        mydb.commit()

def add_students_to_attendance():

    # Get the student names from the studentInfo table
    cursor.execute("SELECT name FROM studentInfo")
    data = cursor.fetchall()

    # Insert the students into the attendance table with today's date
    for row in data:
        # Check if a row already exists for this student and today's date
        cursor.execute("SELECT * FROM attendance WHERE student_name = %s AND date = %s", (row[0], today))
        existing_data = cursor.fetchone()

        # If a row doesn't exist, insert the student with today's date and default attendance value 'N'
        if not existing_data:
            cursor.execute("INSERT INTO attendance (date, student_name, subject, attendance) VALUES (%s, %s, %s, %s)", (today, row[0], '', 'N'))

    # Commit the changes to the database
    mydb.commit()

ScrollableFrame = customtkinter.CTkScrollableFrame(
    master = staffPage
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
    text   = "Attendance Manager",
    font   = ("Segoe UI", 32),
    width  = 1300,
    anchor = "w"
)
AttendanceLable.place(x=20,y=80)

subjectAttendance = customtkinter.CTkEntry(
    master = mainPage,
    width  = 260,
    height = 60, 
    placeholder_text = "SUBJECT",
    border_width = 2,
    corner_radius = 10
)
subjectAttendance.place(x=850,y=140)

presentStudent = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "PRESENT",
    border_width = 1,
    command = mark_present
)
presentStudent.place(x=850,y=250)

absentStudent = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "ABSENT",
    fg_color = "#D3494E",
    hover_color = "#852E32",
    command = mark_absent
)
absentStudent.place(x=850,y=210)

add_students_to_attendance()
# Create Treeview widget
treeview = ttk.Treeview(mainPage, columns=("date", "name", "subject", "attendance"), show="headings")
treeview.heading("date", text="Date")
treeview.heading("name", text="Student Name")
treeview.heading("subject", text="Subject")
treeview.heading("attendance", text="Attendance")

# Get attendance data from MySQL table for today's date
cursor.execute("SELECT * FROM attendance WHERE date=%s", (today,))
data = cursor.fetchall()

# Insert data into Treeview widget
for row in data:
    treeview.insert("", END, values=row)

treeview.place(x=20,y=150)

GradesLable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Grades",
    font   = ("Segoe UI", 32),
    width  = 1300,
    anchor = "w"
)
GradesLable.place(x=20,y=430)

# Create Treeview widget
gradestree = ttk.Treeview(mainPage, columns=("id", "name", "subject", "grade", "date"), show="headings")
gradestree.place(x=20,y=480)

# Add headings
gradestree.heading("id", text="ID")
gradestree.heading("name", text="Student Name")
gradestree.heading("subject", text="Subject")
gradestree.heading("grade", text="Grade")
gradestree.heading("date", text="Date")

# Retrieve data from database and insert into Treeview widget
cursor.execute("SELECT * FROM grades")
for row in cursor.fetchall():
    gradestree.insert("", "end", values=row)

subjectName = customtkinter.CTkEntry(
    master = mainPage,
    width  = 260,
    height = 60, 
    placeholder_text = "EXAM SUBJECT",
    border_width = 2,
    corner_radius = 10
)
subjectName.place(x=1050,y=480)

# Retrieve student names from MySQL
cursor.execute("SELECT name FROM studentInfo")
student_names = [row[0] for row in cursor.fetchall()]

# Create CTkComboBox and populate with student names
students = customtkinter.CTkComboBox(
    master=mainPage,
    values=student_names
)
students.place(x=1050, y=550)

grades = customtkinter.CTkComboBox(
    master = mainPage,
    values=["A", "B", "C", "D", "F"],
    width = 110,
)
grades.place(x=1200,y=550)

addGradesButton = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 30,
    text   = "Add Grades",
    border_width = 1,
    command = add_grades
)
addGradesButton.place(x=1050,y=590)

updateGradesButton = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 30,
    text   = "Update Grades",
    border_width = 1,
    command = update_grades
)
updateGradesButton.place(x=1180,y=590)

commsLable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Communication",
    font   = ("Segoe UI", 32),
    width  = 1300,
    anchor = "w"
)
commsLable.place(x=20,y=750)

chatButton = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 30,
    text   = "Chat",
    border_width = 1,
    command = open_chat
)
chatButton.place(x=20,y=830)

audiosharebutton = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 30,
    text   = "Share Audio",
    border_width = 1,
    command = start_audio_sharing
)
audiosharebutton.place(x=150,y=830)

screenShare = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 30,
    text   = "Screen Share",
    border_width = 1,
    command = start_screen_sharing
)
screenShare.place(x=280,y=830)

videoCall = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 30,
    text   = "Video call",
    border_width = 1,
    command = start_camera_stream
)
videoCall.place(x=410,y=830)
username = "staff"

staffPage.mainloop()