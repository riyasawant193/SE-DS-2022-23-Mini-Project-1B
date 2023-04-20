import customtkinter
import tkinter
from tkinter import StringVar,messagebox,ttk,NO,CENTER,END
import mysql.connector

customtkinter.set_appearance_mode("light")

adminPage = customtkinter.CTk()
adminPage.title("adminPage")
adminPage.geometry('1366x768')
adminPage.attributes('-fullscreen',False)

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vep4pta8xv@",
    database="world"
)
cursor = mydb.cursor()

def add_announcement():
    announcement = notice.get("1.0", "end-1c")
    
    # Truncate the notice table
    cursor.execute("TRUNCATE TABLE notice")
    
    # Insert the new announcement
    cursor.execute("INSERT INTO notice (announcement) VALUES (%s)", (announcement,))
    mydb.commit()
    
    messagebox.showinfo("Success", "Announcement added successfully!")
    return

def update_student():
    # Get the ID of the selected row from the treeview
    selected_item = studentTree.selection()[0]
    selected_item_id = studentTree.item(selected_item)['values'][0]

    # Get the updated values from the entry fields
    name = userName.get()
    password = passWord.get()
    genderval = gender.get()
    phone = phonenumber.get()
    email = emailid.get()
    birth_year = birthYear.get()

    # Update the record in the database
    cursor.execute("UPDATE studentInfo SET name = %s, password = %s, gender = %s, phonenumber = %s, email = %s, birth_year = %s WHERE id = %s",
                   (name, password, genderval, phone, email, birth_year, selected_item_id))
    mydb.commit()
    messagebox.showinfo("Success", "Student updated successfully!")

    # Update the corresponding row in the treeview
    studentTree.item(selected_item, text="", values=(selected_item_id, name, password, genderval, phone, email, birth_year))

def update_staff():
    try:
        # Get the ID of the selected row from the treeview
        selected_item = staffTree.selection()[0]
        selected_item_id = staffTree.item(selected_item)['values'][0]

        # Get the updated values from the entry fields
        name = userName.get()
        password = passWord.get()
        genderval = gender.get()
        phone = phonenumber.get()
        email = emailid.get()
        birth_year = birthYear.get()

        # Update the record in the database
        cursor.execute("UPDATE staffInfo SET name = %s, password = %s, gender = %s, phonenumber = %s, email = %s, birth_year = %s WHERE id = %s",
                       (name, password, genderval, phone, email, birth_year, selected_item_id))
        mydb.commit()

        # Update the corresponding row in the treeview
        staffTree.item(selected_item, text="", values=(selected_item_id, name, password, genderval, phone, email, birth_year))
        messagebox.showinfo("Success", "Staff updated successfully!")
        
    except IndexError:
        # Catch an IndexError if no row is selected in the treeview
        messagebox.showerror("Error", "Please select a staff member to update.")
        
    except Exception as e:
        # Catch any other exceptions and show an error message
        messagebox.showerror("Error", f"An error occurred while updating the staff member: {str(e)}")

def add_student():
    name = userName.get()
    password = passWord.get()
    genderval = gender.get()
    phone = phonenumber.get()
    email = emailid.get()
    birth_year = birthYear.get()

    # Insert values into the table
    cursor.execute("INSERT INTO studentInfo (name, password, gender, phonenumber, email, birth_year) VALUES (%s, %s, %s, %s, %s, %s)",
                   (name, password, genderval, phone, email, birth_year))
    mydb.commit()
    messagebox.showinfo("Success", "Student added successfully!")

    # Update the treeview with the new data
    studentTree.insert("", "end", values=(cursor.lastrowid, name, password, genderval, phone, email, birth_year))

def add_staff():
    name = userName.get()
    password = passWord.get()
    genderval = gender.get()
    phone = phonenumber.get()
    email = emailid.get()
    birth_year = birthYear.get()

    # Insert values into the table
    cursor.execute("INSERT INTO staffInfo (name, password, gender, phonenumber, email, birth_year) VALUES (%s, %s, %s, %s, %s, %s)",
                   (name, password, genderval, phone, email, birth_year))
    mydb.commit()
    messagebox.showinfo("Success", "Staff added successfully!")

    # Update the treeview with the new data
    staffTree.insert("", "end", values=(cursor.lastrowid, name, password, genderval, phone, email, birth_year))

def delete_selected_student():
    selected_item = studentTree.selection()[0]
    values = studentTree.item(selected_item, 'values')
    cursor.execute(f"DELETE FROM studentInfo WHERE id={values[0]}")
    mydb.commit()
    studentTree.delete(selected_item)
    messagebox.showinfo("Delete Student", f"Student with ID {values[0]} has been deleted")

def delete_selected_staff():
    selected_item = staffTree.selection()[0]
    values = staffTree.item(selected_item, 'values')
    cursor.execute(f"DELETE FROM staffInfo WHERE id={values[0]}")
    mydb.commit()
    staffTree.delete(selected_item)
    messagebox.showinfo("Delete Staff", f"Staff with ID {values[0]} has been deleted")

ScrollableFrame = customtkinter.CTkScrollableFrame(
    master = adminPage
)
ScrollableFrame.pack(fill='both', expand=True)

mainPage = customtkinter.CTkFrame(
    master = ScrollableFrame,
    height=1400
)
mainPage.pack(fill='both', expand=True)

adminLable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "ADMIN LOGIN",
    font   = ("Segoe UI",14)
)
adminLable.place(x=20,y=10)

studentTable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Students",
    font   = ("Segoe UI",18)
)
studentTable.place(x=20,y=50)

# Create studentTreeview widget
studentTree = ttk.Treeview(mainPage, columns=("id", "name", "password", "gender", "phone", "email", "birth_year"), show="headings")
studentTree.heading("id", text="ID")
studentTree.heading("name", text="Name")
studentTree.heading("password", text="Password")
studentTree.heading("gender", text="Gender")
studentTree.heading("phone", text="Phone")
studentTree.heading("email", text="Email")
studentTree.heading("birth_year", text="Birth Year")

# Retrieve data from studentInfo table and insert into studentTreeview
cursor.execute("SELECT * FROM studentInfo")
rows = cursor.fetchall()
for row in rows:
    studentTree.insert("", "end", values=row)

# Configure columns to fit the content
studentTree.column("id", width=50, minwidth=50, anchor="center")
studentTree.column("name", width=100, minwidth=100, anchor="center")
studentTree.column("password", width=100, minwidth=100, anchor="center")
studentTree.column("gender", width=75, minwidth=75, anchor="center")
studentTree.column("phone", width=125, minwidth=125, anchor="center")
studentTree.column("email", width=150, minwidth=150, anchor="center")
studentTree.column("birth_year", width=100, minwidth=100, anchor="center")

studentTree.place(x=20,y=80,width=600)

removeButtonStudent = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "Remove Student",
    fg_color = "#D3494E",
    hover_color = "#852E32",
    command = delete_selected_student
)
removeButtonStudent.place(x=20,y=320)

updateStudentButton = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "Update Student",
    border_width = 1,
    command = update_student
)
updateStudentButton.place(x=150,y=320)

staffTable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Staff",
    font   = ("Segoe UI",18)
)
staffTable.place(x=700,y=50)

# Create staffTreeview widget
staffTree = ttk.Treeview(mainPage, columns=("id", "name", "password", "gender", "phone", "email", "birth_year"), show="headings")
staffTree.heading("id", text="ID")
staffTree.heading("name", text="Name")
staffTree.heading("password", text="Password")
staffTree.heading("gender", text="Gender")
staffTree.heading("phone", text="Phone")
staffTree.heading("email", text="Email")
staffTree.heading("birth_year", text="Birth Year")

# Retrieve data from studentInfo table and insert into staffTreeview
cursor.execute("SELECT * FROM staffInfo")
rows = cursor.fetchall()
for row in rows:
    staffTree.insert("", "end", values=row)

# Configure columns to fit the content
staffTree.column("id", width=50, minwidth=50, anchor="center")
staffTree.column("name", width=100, minwidth=100, anchor="center")
staffTree.column("password", width=100, minwidth=100, anchor="center")
staffTree.column("gender", width=75, minwidth=75, anchor="center")
staffTree.column("phone", width=125, minwidth=125, anchor="center")
staffTree.column("email", width=150, minwidth=150, anchor="center")
staffTree.column("birth_year", width=100, minwidth=100, anchor="center")

staffTree.place(x=700,y=80,width=600)

removeButtonStaff = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "Remove Staff",
    fg_color = "#D3494E",
    hover_color = "#852E32",
    command = delete_selected_staff
)
removeButtonStaff.place(x=700,y=320)

updateStaffButton = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "Update Staff",
    border_width = 1,
    command = update_staff
)
updateStaffButton.place(x=830,y=320)

inputSection = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Add details to add or update student/Staff",
    font   = ("Segoe UI",18)
)
inputSection.place(x=25,y=370)

userName = customtkinter.CTkEntry(
    master = mainPage,
    width  = 260,
    height = 60, 
    placeholder_text = "USERNAME",
    border_width = 2,
    corner_radius = 10
)
userName.place(x=20,y=400)

passWord = customtkinter.CTkEntry(
    master = mainPage,
    width  = 260,
    height = 60, 
    placeholder_text = "PASSWORD",
    border_width = 2,
    corner_radius = 10
)
passWord.place(x=300,y=400)

gender = customtkinter.CTkComboBox(
    master = mainPage,
    values=["male", "female", "others"],
)
gender.place(x=20,y=470)

phonenumber = customtkinter.CTkEntry(
    master = mainPage,
    width  = 200,
    height = 32, 
    placeholder_text = "Phone number",
    border_width = 2,
    corner_radius = 10
)
phonenumber.place(x=170,y=470)

emailid = customtkinter.CTkEntry(
    master = mainPage,
    width  = 180,
    height = 32, 
    placeholder_text = "email id",
    border_width = 2,
    corner_radius = 10
)
emailid.place(x=380,y=470)

birthYear = customtkinter.CTkEntry(
    master = mainPage,
    width  = 80,
    height = 32, 
    placeholder_text = "Birth Year",
    border_width = 2,
    corner_radius = 10
)
birthYear.place(x=20,y=510)

addStaffButton = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 30,
    text   = "Add Staff",
    border_width = 1,
    command = add_staff
)
addStaffButton.place(x=120,y=510)

addStudentButton = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "Add Student",
    border_width = 1,
    command = add_student
)
addStudentButton.place(x=250,y=510)

noticeLable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Announment Section",
    font   = ("Segoe UI",26)
)
noticeLable.place(x=25,y=570)

notice = customtkinter.CTkTextbox(
    master = mainPage,
    border_width = 1,
    width = 900,
    height = 300,
    wrap = "word",
    font = ("Segoe UI",30)
)
notice.place(x=25,y=630)

sendAnnouncement = customtkinter.CTkButton(
    master = mainPage,
    width  = 120,
    height = 32,
    text   = "send",
    border_width = 1,
    command = add_announcement
)
sendAnnouncement.place(x=790,y=880)

attendanceLable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Attendance of Students",
    font   = ("Segoe UI",26)
)
attendanceLable.place(x=25,y=950)

# Create attTree treeview
attTree = ttk.Treeview(master=mainPage)

# Define columns
attTree['columns'] = ('Date', 'Student Name', 'Subject', 'Attendance')

# Format columns
attTree.column('#0', width=0, stretch=NO)
attTree.column('Date', anchor=CENTER, width=100)
attTree.column('Student Name', anchor=CENTER, width=150)
attTree.column('Subject', anchor=CENTER, width=100)
attTree.column('Attendance', anchor=CENTER, width=40)

# Create headings
attTree.heading('#0', text='', anchor=CENTER)
attTree.heading('Date', text='Date', anchor=CENTER)
attTree.heading('Student Name', text='Student Name', anchor=CENTER)
attTree.heading('Subject', text='Subject', anchor=CENTER)
attTree.heading('Attendance', text='Attendance', anchor=CENTER)

# Retrieve data from attendance table
cursor.execute("SELECT * FROM attendance")
rows = cursor.fetchall()

# Insert data into treeview
for row in rows:
    attTree.insert(parent='', index='end', text='', values=row)

# Place treeview
attTree.place(x=25, y=1000, width=600)

GradesLable = customtkinter.CTkLabel(
    master = mainPage,
    text   = "Grades of Students",
    font   = ("Segoe UI",26)
)
GradesLable.place(x=700,y=950)

# Create a treeview to display the grades data
gradesTree = ttk.Treeview(mainPage, columns=("student_name", "subject", "grade", "date"), selectmode="extended")

# Set the column headings and widths
gradesTree.heading("#0", text="ID")
gradesTree.column("#0", width=0, stretch=NO)
gradesTree.heading("student_name", text="Student Name")
gradesTree.column("student_name", width=150, anchor='w')
gradesTree.heading("subject", text="Subject")
gradesTree.column("subject", width=200, anchor='w')
gradesTree.heading("grade", text="Grade")
gradesTree.column("grade", width=100, anchor=CENTER)
gradesTree.heading("date", text="Date")
gradesTree.column("date", width=150, anchor=CENTER)

# Populate the treeview with data from the grades table
cursor.execute("SELECT id, student_name, subject, grade, date FROM grades")
rows = cursor.fetchall()
for row in rows:
    gradesTree.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4]))

gradesTree.place(x=700,y=1000,width=600)

adminPage.mainloop()
