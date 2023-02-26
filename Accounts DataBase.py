from tkinter import *
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
import json
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

connection = sqlite3.connect("files/Accounts.db")

cursor = connection.cursor()


def add_win(win1, win2, txt):
    noteBook.add(win1, text=txt)
    noteBook.hide(win2)


def print_text(win, txt, color, x, y):
    Label(win, text=txt, font=("Arial", 10, "bold"), bg="light Blue", fg=color).place(x=x, y=y)


def account_login():
    connection = sqlite3.connect("files/Accounts.db")

    cursor = connection.cursor()

    cursor.execute("SELECT *, oid FROM accounts")
    records = cursor.fetchall()

    access = False
    name = ""
    user_id = 0

    for record in records:
        if login_email.get() == record[1] and login_password.get() == str(record[2]):
            access = True
            name = record[0]
            user_id = record[3]

    if access:
        add_win(user_account_screen, login_screen, "USER ACCOUNT")
        print_text(user_account_screen, "Hi! We are happy to see you " + str(name), "Green", 75, 300)

        text = name + " " + str(user_id) + " logged in on " + str(time.strftime("%A")) + " " + str(
            time.strftime("%B")) + " " + str(time.strftime("%x")) + " at " + str(time.strftime("%I : %M : %S %p"))

        cursor.execute("INSERT INTO logged_users VALUES (:line)",
                       {
                           'line': text
                       }
                       )
    else:
        print_text(login_screen, "Your email or password may be wrong", "Red", 75, 450)

    connection.commit()

    connection.close()


def log_out():
    add_win(login_screen, user_account_screen, "L O G I N")

    connection = sqlite3.connect("files/Accounts.db")

    cursor = connection.cursor()

    cursor.execute("SELECT *, oid FROM accounts")
    records = cursor.fetchall()

    access = False
    name = ""
    user_id = 0

    for record in records:
        if login_email.get() == record[1] and login_password.get() == str(record[2]):
            access = True
            name = record[0]
            user_id = record[3]

    if access:
        text = name + " " + str(user_id) + " logged out on " + str(time.strftime("%A")) + " " + str(
            time.strftime("%B")) + " " + str(time.strftime("%x")) + " at " + str(time.strftime("%I : %M : %S %p"))

        cursor.execute("INSERT INTO logged_users VALUES (:line)",
                       {
                           'line': text
                       }
                       )

    connection.commit()

    connection.close()

    login_email.delete(0, END)
    login_password.delete(0, END)


def account_create():
    connection = sqlite3.connect("files/Accounts.db")

    cursor = connection.cursor()

    cursor.execute("INSERT INTO accounts VALUES (:user_name, :email_id, :pass)",
                   {
                       'user_name': user_name.get(),
                       'email_id': email.get(),
                       'pass': password.get()
                   }
                   )

    connection.commit()

    connection.close()

    user_name.delete(0, END)
    email.delete(0, END)
    password.delete(0, END)


def create_pdf():
    connection = sqlite3.connect("files/Accounts.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM logged_users")
    logged_users = cursor.fetchall()

    c = canvas.Canvas("files/account_report.pdf", pagesize=A4)
    c.setFont("Helvetica", 15)

    c.drawString(100, 750, "THE ISLAMIA UNIVERSITY OF BAHAWALPUR")

    x, y = 50, 700

    for log_user in logged_users:
        line = str(log_user)
        c.drawString(x, y, line)
        y -= 25
        if y < 50:
            c.showPage()
            y = 700

    c.save()

    connection.commit()

    connection.close()


def show_records():
    connection = sqlite3.connect("files/Accounts.db")

    cursor = connection.cursor()

    cursor.execute("SELECT *, oid FROM accounts")
    records = cursor.fetchall()

    print_records = ""

    h, w = 20, 400
    inc = 20

    records_win = Tk()
    records_win.title("Records")

    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) + '\n'
        h += inc

    records_win.geometry(str(w) + "x" + str(h))

    Label(records_win, text="R E C O R D S   O F   I U B", font=("Arial", 15, "bold")).pack()
    record_label = Label(records_win, text=print_records)
    record_label.pack()

    connection.commit()

    connection.close()


def convert():
    connection = sqlite3.connect("files/Accounts.db")

    cursor = connection.cursor()

    cursor.execute("SELECT *, oid FROM accounts")
    records = cursor.fetchall()

    dicts = []

    for record in records:
        dict = {"name": record[0], "email": record[1], "pass": record[2], "oid": record[3]}
        dicts.append(dict)

    with open("files/users.json", "w") as f:
        json.dump(dicts, f, indent=4)
    f.close()

    connection.commit()

    connection.close()


def delete_records():
    connection = sqlite3.connect("files/Accounts.db")

    cursor = connection.cursor()

    cursor.execute("DELETE from accounts WHERE oid = " + select_id.get())

    select_id.delete(0, END)

    connection.commit()

    connection.close()


def edit_records():
    connection = sqlite3.connect("files/Accounts.db")

    cursor = connection.cursor()

    record_id = select_id_editor.get()

    cursor.execute("SELECT * FROM accounts WHERE oid = " + record_id)
    records = cursor.fetchall()

    for record in records:
        user_name_editor.insert(0, record[0])
        email_editor.insert(0, record[1])
        password_editor.insert(0, record[2])


def update_records():
    connection = sqlite3.connect("files/Accounts.db")

    cursor = connection.cursor()

    record_id = select_id_editor.get()

    cursor.execute("""UPDATE accounts SET 
                    user_name = :user_name,
                    email_id = :email_id,
                    pass = :pass

                    WHERE oid = :oid""",
                   {
                       'user_name': user_name_editor.get(),
                       'email_id': email_editor.get(),
                       'pass': password_editor.get(),

                       'oid': record_id
                   }
                   )

    connection.commit()

    connection.close()


main_win = Tk()

icon = ImageTk.PhotoImage(Image.open("images/lab_logo.png"))

main_win.title("THE ISLAMIA UNIVERSITY OF BAHAWALPUR")
main_win.wm_iconphoto(main_win, icon)
main_win.geometry("450x600")
main_win.resizable(width=False, height=False)
main_win.config(bg="Light Blue")

noteBook = ttk.Notebook(main_win)

login_screen = Frame(noteBook, bg="light blue", relief=SOLID, borderwidth=3)
create_account_screen = Frame(noteBook, bg="light blue", relief=SOLID, borderwidth=3)
admin = Frame(noteBook, bg="light blue", relief=SOLID, borderwidth=3)
editor_screen = Frame(noteBook, bg="Light blue", relief=SOLID, borderwidth=3)
user_account_screen = Frame(noteBook, bg="Light blue", relief=SOLID, borderwidth=3)

noteBook.add(login_screen, text="L O G I N")

noteBook.pack(expand=True, fill="both", ipadx=5, ipady=5, padx=5, pady=5)

login_email = Entry(login_screen, width=25)
login_email.place(x=200, y=150)
login_password = Entry(login_screen, width=25)
login_password.place(x=200, y=200)

Label(login_screen, text="A C C O U N T   L O G I N", font=("Arial", 17, "bold"), bg="light Blue", fg="Blue").place(
    x=65, y=50)
Label(login_screen, text="E-mail", bg="Light Blue").place(x=100, y=150)
Label(login_screen, text="Password", bg="Light Blue").place(x=100, y=200)

Button(login_screen, text="L O G I N", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=10, command=account_login).place(x=180, y=300)
Button(login_screen, text="CREATE NEW ACCOUNT", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=lambda: add_win(create_account_screen, login_screen, "CREATE ACCOUNT")
       ).place(x=140, y=350)
Button(login_screen, text="ADMINISTRATOR", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=lambda: add_win(admin, login_screen, "ADMIN")).place(x=0, y=0)

user_name = Entry(create_account_screen, width=20)
user_name.place(x=200, y=100)
email = Entry(create_account_screen, width=20)
email.place(x=200, y=150)
password = Entry(create_account_screen, width=20)
password.place(x=200, y=200)

Label(create_account_screen, text="C R E A T E   N E W   A C C O U N T", font=("Arial", 14, "bold"), bg="light Blue",
      fg="Blue").place(x=50, y=50)
Label(create_account_screen, text="user name", bg="Light Blue").place(x=100, y=100)
Label(create_account_screen, text="E-mail", bg="Light Blue").place(x=100, y=150)
Label(create_account_screen, text="Password", bg="Light Blue").place(x=100, y=200)

Button(create_account_screen, text="CREATE", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=10, command=account_create).place(x=140, y=325)
Button(create_account_screen, text="<<<", font=("Arial", 10, "bold"), padx=1, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=5, command=lambda: add_win(login_screen, create_account_screen, "LOGIN")).place(x=5, y=5)

Label(admin, text="Select id", bg="Light Blue").place(x=100, y=100)

select_id = Entry(admin, width=20)
select_id.place(x=200, y=100)

Button(admin, text="DELETE RECORDS", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=delete_records).place(x=225, y=450)
Button(admin, text="SHOW RECORDS", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=show_records).place(x=25, y=450)
Button(admin, text="Convert To JSON", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=convert).place(x=225, y=500)
Button(admin, text="EDIT RECORDS", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=lambda: add_win(editor_screen, admin, "EDITOR")).place(x=25, y=500)
Button(admin, text="<<<", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=lambda: add_win(login_screen, admin, "LOGIN")).place(x=0, y=0)
Button(admin, text="CREATE PDF", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=create_pdf).place(x=125, y=400)

user_name_editor = Entry(editor_screen, width=20)
user_name_editor.place(x=150, y=200)
email_editor = Entry(editor_screen, width=20)
email_editor.place(x=150, y=300)
password_editor = Entry(editor_screen, width=20)
password_editor.place(x=150, y=400)

user_name_label_editor = Label(editor_screen, text="user name", bg="Light Blue")
user_name_label_editor.place(x=50, y=200)
email_label_editor = Label(editor_screen, text="email id", bg="Light Blue")
email_label_editor.place(x=50, y=300)
password_label_editor = Label(editor_screen, text="password", bg="Light Blue")
password_label_editor.place(x=50, y=400)

save_btn = Button(editor_screen, text="Update Records", padx=1, pady=3, command=update_records)
save_btn.place(x=150, y=500)

insert_btn = Button(editor_screen, text="Insert Data", padx=1, pady=3, command=edit_records)
insert_btn.place(x=175, y=150)

Label(editor_screen, text="Select id", bg="Light Blue").place(x=100, y=100)
Label(editor_screen, text="UPDATE RECORDS", font=("Arial", 15, "bold"), bg="Light Blue").place(x=100, y=50)

select_id_editor = Entry(editor_screen, width=20)
select_id_editor.place(x=200, y=100)

Button(editor_screen, text="<<<", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=lambda: add_win(admin, editor_screen, "LOGIN")).place(x=0, y=0)

Button(user_account_screen, text="LOG OUT", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=log_out).place(x=0, y=0)

connection.commit()

connection.close()

main_win.mainloop()
