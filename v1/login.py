import customtkinter
import tkinter
from tkinter import StringVar,messagebox
import mysql.connector

customtkinter.set_appearance_mode("light")

def login():
    username = userName.get()
    password = passWord.get()

    # Check if fields are empty
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    if checkVar.get() != "on":
        messagebox.showerror("Error", "Please accept the terms and conditions")
        return

    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vep4pta8xv@",
        database="world"
    )
    cursor = mydb.cursor()

    # Check if user is an admin
    cursor.execute("SELECT * FROM adminInfo WHERE username = %s AND password = %s", (username, password))
    admin = cursor.fetchone()
    if admin:
        messagebox.showinfo("Success", "Login successful as admin")
        import admin
        return

    # Check if user is a staff member
    cursor.execute("SELECT * FROM staffInfo WHERE name = %s AND password = %s", (username, password))
    staff = cursor.fetchone()
    if staff:
        messagebox.showinfo("Success", "Login successful as staff member")
        import staff
        return

    # Check if user is a student
    cursor.execute("SELECT * FROM studentInfo WHERE name = %s AND password = %s", (username, password))
    student = cursor.fetchone()
    if student:
        print(username)
        # Truncate the table to remove any existing records
        cursor.execute("TRUNCATE TABLE recent_users")
        # Insert a new record with the provided username
        cursor.execute("INSERT INTO recent_users (username) VALUES (%s)", (username,))
        mydb.commit()
        messagebox.showinfo("Success", "Login successful as student")
        import student
        return

    # If user is not found in any table, display error message
    messagebox.showerror("Error", "Invalid username or password")

def on_exit():
    loginPage.destroy()

loginPage = customtkinter.CTk()
loginPage.title("LoginPage")
loginPage.attributes('-fullscreen',True)

loginFrame = customtkinter.CTkFrame(
    master = loginPage,
    height = 350,
    width  = 300,
)
loginFrame.place(relx=0.5, rely=0.5, anchor='center')

loginLable = customtkinter.CTkLabel(
    master = loginFrame,
    text   = "𝒲𝑒𝓁𝒸𝑜𝓂𝑒",
    font   = ("Segoe UI",28)
)
loginLable.place(x=20,y=30)

userName = customtkinter.CTkEntry(
    master = loginFrame,
    width  = 260,
    height = 60, 
    placeholder_text = "USERNAME",
    border_width = 2,
    corner_radius = 10
)
userName.place(x=20,y=100)

passWord = customtkinter.CTkEntry(
    master = loginFrame,
    width  = 260,
    height = 60, 
    placeholder_text = "PASSWORD",
    border_width = 2,
    corner_radius = 10
)
passWord.place(x=20,y=170)

loginButton = customtkinter.CTkButton(
    master = loginFrame,
    width  = 120,
    height = 32,
    text   = "Login",
    command= login
)
loginButton.place(x=25,y=280)

exitButton = customtkinter.CTkButton(
    master = loginFrame,
    width  = 120,
    height = 32,
    text   = "Exit",
    fg_color = "#D3494E",
    hover_color = "#852E32",
    command = on_exit
)
exitButton.place(x=150,y=280)

checkVar = tkinter.StringVar(value="off")
termCondition = customtkinter.CTkCheckBox(
    master = loginFrame,
    variable = checkVar,
    onvalue  = "on",
    offvalue = "off",
    text     = "Terms and Conditions"
)
termCondition.place(x=25,y=245)

loginPage.mainloop()