from tkinter import *
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
import json
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


connection1 = sqlite3.connect("files/Accounts.db")
connection2 = sqlite3.connect("files/People's Data.db")

cursor1 = connection1.cursor()
cursor2 = connection2.cursor()


def add_win(win1, win2, txt):
    noteBook1.add(win1, text=txt)
    noteBook1.hide(win2)


def win_add(win1, win2, txt):
    noteBook2.add(win1, text=txt)
    noteBook2.hide(win2)


def print_text(win, txt, color, x, y):
    Label(win, text=txt, font=("Arial", 10, "bold"), bg="light Blue", fg=color).place(x=x, y=y)


def get_user_id():
    connection1 = sqlite3.connect("files/Accounts.db")
    cursor1 = connection1.cursor()

    cursor1.execute("SELECT *, oid FROM accounts")
    records = cursor1.fetchall()

    user_id = 0

    for record in records:
        if login_email.get() == record[1] and login_password.get() == str(record[2]):
            user_id = record[3]

    connection1.commit()
    connection1.close()

    return user_id


def account_login():
    connection1 = sqlite3.connect("files/Accounts.db")
    cursor1 = connection1.cursor()

    cursor1.execute("SELECT *, oid FROM accounts")
    records = cursor1.fetchall()

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
        print_text(user_account_screen, "Hi! We are happy to see you " + str(name), "Green", 75, 0)

        text = name + " " + str(user_id) + " logged in on " + str(time.strftime("%A")) + " " + str(
            time.strftime("%B")) + " " + str(time.strftime("%x")) + " at " + str(time.strftime("%I : %M : %S %p"))

        cursor1.execute("INSERT INTO logged_users VALUES (:line)",
                        {
                            'line': text
                        }
                        )

        connection2 = sqlite3.connect("files/People's Data.db")
        cursor2 = connection2.cursor()

        cursor2.execute("SELECT * FROM data WHERE oid = " + str(user_id))
        rec = cursor2.fetchone()

        display_records(rec)

        connection2.commit()
        connection2.close()

    else:
        print_text(login_screen, "Your email or password may be wrong", "Red", 75, 450)

    connection1.commit()
    connection1.close()


def log_out():
    add_win(login_screen, user_account_screen, "L O G I N")

    connection1 = sqlite3.connect("files/Accounts.db")
    cursor1 = connection1.cursor()

    cursor1.execute("SELECT *, oid FROM accounts")
    records = cursor1.fetchall()

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

        cursor1.execute("INSERT INTO logged_users VALUES (:line)",
                        {
                            'line': text
                        }
                        )

    connection1.commit()
    connection1.close()


def account_create():
    connection1 = sqlite3.connect("files/Accounts.db")
    cursor1 = connection1.cursor()

    cursor1.execute("INSERT INTO accounts VALUES (:user_name, :email_id, :pass)",
                    {
                        'user_name': user_name.get(),
                        'email_id': email.get(),
                        'pass': password.get()
                    }
                    )

    connection1.commit()
    connection1.close()

    user_name.delete(0, END)
    email.delete(0, END)
    password.delete(0, END)


def create_pdf():
    connection1 = sqlite3.connect("files/Accounts.db")
    cursor1 = connection1.cursor()

    cursor1.execute("SELECT * FROM logged_users")
    logged_users = cursor1.fetchall()

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

    connection1.commit()
    connection1.close()


def show_records():
    connection1 = sqlite3.connect("files/Accounts.db")
    cursor1 = connection1.cursor()

    cursor1.execute("SELECT *, oid FROM accounts")
    records = cursor1.fetchall()

    print_records = ""

    h, w = 40, 400
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

    connection1.commit()
    connection1.close()


def convert():
    connection1 = sqlite3.connect("files/Accounts.db")
    cursor1 = connection1.cursor()

    cursor1.execute("SELECT *, oid FROM accounts")
    records1 = cursor1.fetchall()

    for record in records1:
        dict1 = {"name": record[0], "email": record[1], "pass": record[2], "oid": record[3]}

        with open("files/user" + str(record[3]) + ".json", "w") as f:
            json.dump(dict1, f, indent=4)
        f.close()

    connection1.commit()
    connection1.close()

    connection2 = sqlite3.connect("files/People's Data.db")
    cursor2 = connection2.cursor()

    cursor2.execute("SELECT *, oid FROM data")
    records2 = cursor2.fetchall()

    for record in records2:
        dict2 = {"first_name": record[0], "last_name": record[1], "father_name": record[2], "mother_name": record[3],
                 "gender": record[4], "date_of_birth": record[5], "place_of_birth": record[6], "age": record[7],
                 "height": record[8], "weight": record[9], "waist": record[10], "BMI": record[11],
                 "blood_group": record[12], "marial_status": record[13], "husband_OR_wife_name": record[14],
                 "no_of_childerns": record[15], "name_of_childerns": [n.strip() for n in str(record[16]).split(",")],
                 "qualification": record[17], "degree": record[18], "job": record[19], "country": record[20],
                 "province": record[21], "state": record[22], "city": record[23], "address": record[24],
                 "zipcode": record[25]
                 }

        with open("files/" + str(record[0]) + " " + str(record[1]) + " " + str(record[26]) + ".json", "w") as f:
            json.dump(dict2, f, indent=4)
        f.close()

    connection2.commit()
    connection2.close()


def delete_records():
    connection1 = sqlite3.connect("files/Accounts.db")
    connection2 = sqlite3.connect("files/People's Data.db")

    cursor1 = connection1.cursor()
    cursor2 = connection2.cursor()

    cursor1.execute("DELETE from accounts WHERE oid = " + select_id.get())
    cursor2.execute("DELETE from data WHERE oid = " + select_id.get())

    connection1.commit()
    connection2.commit()

    connection1.close()
    connection2.close()

    select_id.delete(0, END)


def edit_records():
    connection1 = sqlite3.connect("files/Accounts.db")
    cursor1 = connection1.cursor()

    record_id = select_id_editor.get()

    cursor1.execute("SELECT * FROM accounts WHERE oid = " + record_id)
    records = cursor1.fetchall()

    for record in records:
        user_name_editor.insert(0, record[0])
        email_editor.insert(0, record[1])
        password_editor.insert(0, record[2])


def update_records():
    connection1 = sqlite3.connect("files/Accounts.db")
    cursor1 = connection1.cursor()

    record_id = select_id_editor.get()

    cursor1.execute("""UPDATE accounts SET 
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

    connection1.commit()
    connection1.close()


def display_records(records=None):
    if records is None:
        records = []
    Label(user_account_screen, text="first name           : " + str(records[0]), bg="light blue", fg="blue").place(
        x=100, y=20)
    Label(user_account_screen, text="last name            : " + str(records[1]), bg="light blue", fg="blue").place(
        x=100, y=40)
    Label(user_account_screen, text="father name          : " + str(records[2]), bg="light blue", fg="blue").place(
        x=100, y=60)
    Label(user_account_screen, text="mother name          : " + str(records[3]), bg="light blue", fg="blue").place(
        x=100, y=80)
    Label(user_account_screen, text="gender name          : " + str(records[4]), bg="light blue", fg="blue").place(
        x=100, y=100)
    Label(user_account_screen, text="date of birth        : " + str(records[5]), bg="light blue", fg="blue").place(
        x=100, y=120)
    Label(user_account_screen, text="place of birth       : " + str(records[6]), bg="light blue", fg="blue").place(
        x=100, y=140)
    Label(user_account_screen, text="age                  : " + str(records[7]), bg="light blue", fg="blue").place(
        x=100, y=160)
    Label(user_account_screen, text="height               : " + str(records[8]), bg="light blue", fg="blue").place(
        x=100, y=180)
    Label(user_account_screen, text="weight               : " + str(records[9]), bg="light blue", fg="blue").place(
        x=100, y=200)
    Label(user_account_screen, text="waist                : " + str(records[10]), bg="light blue", fg="blue").place(
        x=100, y=220)
    Label(user_account_screen, text="BMI                  : " + str(records[11]), bg="light blue", fg="blue").place(
        x=100, y=240)
    Label(user_account_screen, text="blood group          : " + str(records[12]), bg="light blue", fg="blue").place(
        x=100, y=260)
    Label(user_account_screen, text="marial status        : " + str(records[13]), bg="light blue", fg="blue").place(
        x=100, y=280)
    Label(user_account_screen, text="husband or wife name : " + str(records[14]), bg="light blue", fg="blue").place(
        x=100, y=300)
    Label(user_account_screen, text="no of childerns      : " + str(records[14]), bg="light blue", fg="blue").place(
        x=100, y=320)
    Label(user_account_screen, text="name of childerns    : " + str(records[15]), bg="light blue", fg="blue").place(
        x=100, y=340)
    Label(user_account_screen, text="qualification        : " + str(records[16]), bg="light blue", fg="blue").place(
        x=100, y=360)
    Label(user_account_screen, text="degree               : " + str(records[17]), bg="light blue", fg="blue").place(
        x=100, y=380)
    Label(user_account_screen, text="job                  : " + str(records[18]), bg="light blue", fg="blue").place(
        x=100, y=400)
    Label(user_account_screen, text="country              : " + str(records[19]), bg="light blue", fg="blue").place(
        x=100, y=420)
    Label(user_account_screen, text="province             : " + str(records[20]), bg="light blue", fg="blue").place(
        x=100, y=440)
    Label(user_account_screen, text="state                : " + str(records[21]), bg="light blue", fg="blue").place(
        x=100, y=460)
    Label(user_account_screen, text="city                 : " + str(records[22]), bg="light blue", fg="blue").place(
        x=100, y=480)
    Label(user_account_screen, text="address              : " + str(records[23]), bg="light blue", fg="blue").place(
        x=100, y=500)
    Label(user_account_screen, text="zipcode              : " + str(records[25]), bg="light blue", fg="blue").place(
        x=100, y=520)


def submit():
    connection2 = sqlite3.connect("files/People's Data.db")
    cursor2 = connection2.cursor()

    cursor2.execute("""INSERT INTO data VALUES 
                    (
                        :f_name, 
                        :l_name, 
                        :father_name, 
                        :mother_name, 
                        :gender, 
                        :date_of_birth, 
                        :place_of_birth, 
                        :age, 
                        :height, 
                        :weight, 
                        :waist, 
                        :BMI, 
                        :blood_group, 
                        :marial_status, 
                        :husband_OR_wife_name, 
                        :no_of_childern,
                        :name_of_childerns, 
                        :qualification, 
                        :degree, 
                        :job, 
                        :country, 
                        :province, 
                        :state, 
                        :city, 
                        :address, 
                        :zipcode
                    )""",

                    {
                        'f_name': f_name.get(),
                        'l_name': l_name.get(),
                        'father_name': father_name.get(),
                        'mother_name': mother_name.get(),
                        'gender': gender.get(),
                        'date_of_birth': date_of_birth.get(),
                        'place_of_birth': place_of_birth.get(),
                        'age': age.get(),
                        'height': height.get(),
                        'weight': weight.get(),
                        'waist': waist.get(),
                        'BMI': BMI.get(),
                        'blood_group': blood_group.get(),
                        'marial_status': marial_status.get(),
                        'husband_OR_wife_name': husband_OR_wife_name.get(),
                        'no_of_childern': no_of_childern.get(),
                        'name_of_childerns': name_of_childerns.get(),
                        'qualification': qualification.get(),
                        'degree': degree.get(),
                        'job': job.get(),
                        'country': country.get(),
                        'province': province.get(),
                        'state': state.get(),
                        'city': city.get(),
                        'address': address.get(),
                        'zipcode': zipcode.get()
                    }
                    )

    connection2.commit()
    connection2.close()

    f_name.delete(0, END)
    l_name.delete(0, END)
    father_name.delete(0, END)
    mother_name.delete(0, END)
    gender.delete(0, END)
    date_of_birth.delete(0, END)
    place_of_birth.delete(0, END)
    age.delete(0, END)
    height.delete(0, END)
    weight.delete(0, END)
    waist.delete(0, END)
    BMI.delete(0, END)
    blood_group.delete(0, END)
    marial_status.delete(0, END)
    husband_OR_wife_name.delete(0, END)
    no_of_childern.delete(0, END)
    name_of_childerns.delete(0, END)
    qualification.delete(0, END)
    degree.delete(0, END)
    job.delete(0, END)
    country.delete(0, END)
    province.delete(0, END)
    state.delete(0, END)
    city.delete(0, END)
    address.delete(0, END)
    zipcode.delete(0, END)


def query():
    connection2 = sqlite3.connect("files/People's Data.db")
    cursor2 = connection2.cursor()

    cursor2.execute("SELECT *, oid FROM data")
    records = cursor2.fetchall()

    print_records = ""

    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) + " " \
                         + str(record[4]) + " " + str(record[5]) + " " + str(record[6]) + " " + str(record[7]) + " " \
                         + str(record[8]) + " " + str(record[9]) + " " + str(record[10]) + " " + str(record[11]) + " " \
                         + str(record[12]) + " " + str(record[13]) + " " + str(record[14]) + " " + str(record[15]) + " " \
                         + str(record[16]) + " " + str(record[17]) + " " + str(record[18]) + " " + str(record[19]) + " " \
                         + str(record[20]) + " " + str(record[21]) + " " + str(record[22]) + " " + str(record[23]) + " " \
                         + str(record[24]) + " " + str(record[25]) + " " + str(record[26]) + " " + "\n"

    records_win = Tk()
    records_win.title("Records")
    records_win.geometry("1200x200")

    record_label = Label(records_win, text=print_records)
    record_label.grid(row=0, column=0)

    connection2.commit()
    connection2.close()


def edit():
    win_add(editor_win, main_win, "E D I T O R   W I N")

    name_label_editor = Label(editor_win,
                              text="U P D A T E   D A T A B A S E   O F   C I T I Z E N S   O F   P A K I S T A N",
                              font=("Arial", 15, "bold"), fg="Dark Blue", bg="Light Blue", padx=10, pady=10)
    name_label_editor.place(x=250, y=50)

    connection2 = sqlite3.connect("files/People's Data.db")
    cursor2 = connection2.cursor()

    record_id = str(get_user_id())

    cursor2.execute("SELECT * FROM data WHERE oid = " + record_id)
    records = cursor2.fetchall()

    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        father_name_editor.insert(0, record[2])
        mother_name_editor.insert(0, record[3])
        gender_editor.insert(0, record[4])
        date_of_birth_editor.insert(0, record[5])
        place_of_birth_editor.insert(0, record[6])
        age_editor.insert(0, record[7])
        height_editor.insert(0, record[8])
        weight_editor.insert(0, record[9])
        waist_editor.insert(0, record[10])
        BMI_editor.insert(0, record[11])
        blood_group_editor.insert(0, record[12])
        marial_status_editor.insert(0, record[13])
        husband_OR_wife_name_editor.insert(0, record[14])
        no_of_childern_editor.insert(0, record[15])
        name_of_childerns_editor.insert(0, record[16])
        qualification_editor.insert(0, record[17])
        degree_editor.insert(0, record[18])
        job_editor.insert(0, record[19])
        country_editor.insert(0, record[20])
        province_editor.insert(0, record[21])
        state_editor.insert(0, record[22])
        city_editor.insert(0, record[23])
        address_editor.insert(0, record[24])
        zipcode_editor.insert(0, record[25])


def update():
    connection2 = sqlite3.connect("files/People's Data.db")
    cursor2 = connection2.cursor()

    record_id = select_id.get()

    cursor2.execute("""UPDATE data SET 
                    first_name = :first,
                    last_name = :last,
                    father_name = :father_name,
                    mother_name = :mother_name,
                    gender = :gender,
                    date_of_birth = :date_of_birth,
                    place_of_birth = :place_of_birth,                
                    age = :age,
                    height = :height,
                    weight = :weight,
                    waist = :waist,
                    BMI = :BMI,
                    blood_group = :blood_group,
                    marial_status = :marial_status,
                    husband_OR_wife_name = :husband_OR_wife_name,
                    no_of_childern = :no_of_childern,
                    name_of_childerns = :name_of_childerns,
                    qualification = :qualification,
                    degree = :degree,
                    job = :job,
                    country = :country,
                    province = :province,
                    state = :state,
                    city = :city,
                    address = :address,
                    zipcode = :zipcode

                    WHERE oid = :oid""",
                    {
                        'first': f_name_editor.get(),
                        'last': l_name_editor.get(),
                        'father_name': father_name_editor.get(),
                        'mother_name': mother_name_editor.get(),
                        'gender': gender_editor.get(),
                        'date_of_birth': date_of_birth_editor.get(),
                        'place_of_birth': place_of_birth_editor.get(),
                        'age': age_editor.get(),
                        'height': height_editor.get(),
                        'weight': weight_editor.get(),
                        'waist': waist_editor.get(),
                        'BMI': BMI_editor.get(),
                        'blood_group': blood_group_editor.get(),
                        'marial_status': marial_status_editor.get(),
                        'husband_OR_wife_name': husband_OR_wife_name_editor.get(),
                        'no_of_childern': no_of_childern_editor.get(),
                        'name_of_childerns': name_of_childerns_editor.get(),
                        'qualification': qualification_editor.get(),
                        'degree': degree_editor.get(),
                        'job': job_editor.get(),
                        'country': country_editor.get(),
                        'province': province_editor.get(),
                        'state': state_editor.get(),
                        'city': city_editor.get(),
                        'address': address_editor.get(),
                        'zipcode': zipcode_editor.get(),

                        'oid': record_id
                    }
                    )

    connection2.commit()
    connection2.close()

    win_add(main_win, editor_win, "M A I N   W I N")


win1 = Tk()
win2 = Tk()

icon = ImageTk.PhotoImage(Image.open("images/lab_logo.png"))

win1.title("THE ISLAMIA UNIVERSITY OF BAHAWALPUR")
win1.wm_iconphoto(win1, icon)
win1.geometry("450x600")
win1.resizable(width=False, height=False)
win1.config(bg="Light Blue")

win2.title("THE ISLAMIA UNIVERSITY OF BAHAWALPUR")
win2.geometry("1200x800")
win2.resizable(width=False, height=False)
win2.config(bg="Light Blue")

noteBook1 = ttk.Notebook(win1)
noteBook2 = ttk.Notebook(win2)

login_screen = Frame(noteBook1, bg="light blue", relief=SOLID, borderwidth=3)
create_account_screen = Frame(noteBook1, bg="light blue", relief=SOLID, borderwidth=3)
admin = Frame(noteBook1, bg="light blue", relief=SOLID, borderwidth=3)
editor_screen = Frame(noteBook1, bg="Light blue", relief=SOLID, borderwidth=3)
user_account_screen = Frame(noteBook1, bg="Light blue", relief=SOLID, borderwidth=3)

main_win = Frame(noteBook2, bg="light blue", relief=SOLID, borderwidth=3)
editor_win = Frame(noteBook2, bg="Light blue", relief=SOLID, borderwidth=3)

noteBook1.add(login_screen, text="L O G I N")
noteBook1.pack(expand=True, fill="both", ipadx=5, ipady=5, padx=5, pady=5)

noteBook2.add(main_win)
noteBook2.pack(expand=True, fill="both", ipadx=5, ipady=5, padx=5, pady=5)

Label(login_screen, text="A C C O U N T   L O G I N", font=("Arial", 17, "bold"), bg="light Blue", fg="Blue").place(
    x=65, y=50)
Label(login_screen, text="E-mail", bg="Light Blue").place(x=100, y=150)
Label(login_screen, text="Password", bg="Light Blue").place(x=100, y=200)

Label(create_account_screen, text="C R E A T E   N E W   A C C O U N T", font=("Arial", 14, "bold"), bg="light Blue",
      fg="Blue").place(x=50, y=50)
Label(create_account_screen, text="user name", bg="Light Blue").place(x=100, y=100)
Label(create_account_screen, text="E-mail", bg="Light Blue").place(x=100, y=150)
Label(create_account_screen, text="Password", bg="Light Blue").place(x=100, y=200)

Label(admin, text="Select id", bg="Light Blue").place(x=100, y=100)

Label(editor_screen, text="user name", bg="Light Blue").place(x=50, y=200)
Label(editor_screen, text="email id", bg="Light Blue").place(x=50, y=300)
Label(editor_screen, text="password", bg="Light Blue").place(x=50, y=400)

Label(editor_screen, text="Select id", bg="Light Blue").place(x=100, y=100)
Label(editor_screen, text="UPDATE RECORDS", font=("Arial", 15, "bold"), bg="Light Blue").place(x=100, y=50)

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

Button(create_account_screen, text="CREATE", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=10, command=account_create).place(x=140, y=325)
Button(create_account_screen, text="<<<", font=("Arial", 10, "bold"), padx=1, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=5, command=lambda: add_win(login_screen, create_account_screen, "LOGIN")).place(x=5, y=5)

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

Button(editor_screen, text="Update Records", padx=1, pady=3, command=update_records).place(x=150, y=500)
Button(editor_screen, text="Insert Data", padx=1, pady=3, command=edit_records).place(x=175, y=150)

Button(editor_screen, text="<<<", font=("Arial", 9, "bold"), padx=3, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=20, command=lambda: add_win(admin, editor_screen, "LOGIN")).place(x=0, y=0)

Button(user_account_screen, text="LOG OUT", font=("Arial", 7, "bold"), padx=1, pady=1, bg="light blue",
       fg="black", activebackground="light blue", activeforeground="black", bd=1, relief=GROOVE, state=ACTIVE,
       height=1, width=10, command=log_out).place(x=0, y=0)

login_email = Entry(login_screen, width=25)
login_email.place(x=200, y=150)
login_password = Entry(login_screen, width=25)
login_password.place(x=200, y=200)

user_name = Entry(create_account_screen, width=20)
user_name.place(x=200, y=100)
email = Entry(create_account_screen, width=20)
email.place(x=200, y=150)
password = Entry(create_account_screen, width=20)
password.place(x=200, y=200)

user_name_editor = Entry(editor_screen, width=20)
user_name_editor.place(x=150, y=200)
email_editor = Entry(editor_screen, width=20)
email_editor.place(x=150, y=300)
password_editor = Entry(editor_screen, width=20)
password_editor.place(x=150, y=400)

select_id = Entry(admin, width=20)
select_id.place(x=200, y=100)

select_id_editor = Entry(editor_screen, width=20)
select_id_editor.place(x=200, y=100)

f_name = Entry(main_win, width=20)
f_name.place(x=200, y=200)
l_name = Entry(main_win, width=20)
l_name.place(x=450, y=200)
father_name = Entry(main_win, width=20)
father_name.place(x=700, y=200)
mother_name = Entry(main_win, width=20)
mother_name.place(x=950, y=200)
gender = Entry(main_win, width=20)
gender.place(x=200, y=250)
date_of_birth = Entry(main_win, width=20)
date_of_birth.place(x=450, y=250)
place_of_birth = Entry(main_win, width=20)
place_of_birth.place(x=700, y=250)
age = Entry(main_win, width=20)
age.place(x=950, y=250)
height = Entry(main_win, width=20)
height.place(x=200, y=300)
weight = Entry(main_win, width=20)
weight.place(x=450, y=300)
waist = Entry(main_win, width=20)
waist.place(x=700, y=300)
BMI = Entry(main_win, width=20)
BMI.place(x=950, y=300)
blood_group = Entry(main_win, width=20)
blood_group.place(x=200, y=350)
marial_status = Entry(main_win, width=20)
marial_status.place(x=450, y=350)
husband_OR_wife_name = Entry(main_win, width=20)
husband_OR_wife_name.place(x=700, y=350)
no_of_childern = Entry(main_win, width=20)
no_of_childern.place(x=950, y=350)
name_of_childerns = Entry(main_win, width=20)
name_of_childerns.place(x=200, y=400)
qualification = Entry(main_win, width=20)
qualification.place(x=450, y=400)
degree = Entry(main_win, width=20)
degree.place(x=700, y=400)
job = Entry(main_win, width=20)
job.place(x=950, y=400)
country = Entry(main_win, width=20)
country.place(x=200, y=450)
province = Entry(main_win, width=20)
province.place(x=450, y=450)
state = Entry(main_win, width=20)
state.place(x=700, y=450)
city = Entry(main_win, width=20)
city.place(x=950, y=450)
address = Entry(main_win, width=20)
address.place(x=200, y=500)
zipcode = Entry(main_win, width=20)
zipcode.place(x=450, y=500)

f_name_editor = Entry(editor_win, width=20)
f_name_editor.place(x=200, y=200)
l_name_editor = Entry(editor_win, width=20)
l_name_editor.place(x=450, y=200)
father_name_editor = Entry(editor_win, width=20)
father_name_editor.place(x=700, y=200)
mother_name_editor = Entry(editor_win, width=20)
mother_name_editor.place(x=950, y=200)
gender_editor = Entry(editor_win, width=20)
gender_editor.place(x=200, y=250)
date_of_birth_editor = Entry(editor_win, width=20)
date_of_birth_editor.place(x=450, y=250)
place_of_birth_editor = Entry(editor_win, width=20)
place_of_birth_editor.place(x=700, y=250)
age_editor = Entry(editor_win, width=20)
age_editor.place(x=950, y=250)
height_editor = Entry(editor_win, width=20)
height_editor.place(x=200, y=300)
weight_editor = Entry(editor_win, width=20)
weight_editor.place(x=450, y=300)
waist_editor = Entry(editor_win, width=20)
waist_editor.place(x=700, y=300)
BMI_editor = Entry(editor_win, width=20)
BMI_editor.place(x=950, y=300)
blood_group_editor = Entry(editor_win, width=20)
blood_group_editor.place(x=200, y=350)
marial_status_editor = Entry(editor_win, width=20)
marial_status_editor.place(x=450, y=350)
husband_OR_wife_name_editor = Entry(editor_win, width=20)
husband_OR_wife_name_editor.place(x=700, y=350)
no_of_childern_editor = Entry(editor_win, width=20)
no_of_childern_editor.place(x=950, y=350)
name_of_childerns_editor = Entry(editor_win, width=20)
name_of_childerns_editor.place(x=200, y=400)
qualification_editor = Entry(editor_win, width=20)
qualification_editor.place(x=450, y=400)
degree_editor = Entry(editor_win, width=20)
degree_editor.place(x=700, y=400)
job_editor = Entry(editor_win, width=20)
job_editor.place(x=950, y=400)
country_editor = Entry(editor_win, width=20)
country_editor.place(x=200, y=450)
province_editor = Entry(editor_win, width=20)
province_editor.place(x=450, y=450)
state_editor = Entry(editor_win, width=20)
state_editor.place(x=700, y=450)
city_editor = Entry(editor_win, width=20)
city_editor.place(x=950, y=450)
address_editor = Entry(editor_win, width=20)
address_editor.place(x=200, y=500)
zipcode_editor = Entry(editor_win, width=20)
zipcode_editor.place(x=450, y=500)

Label(main_win, text="First name", bg="Light Blue").place(x=100, y=200)
Label(main_win, text="Last name", bg="Light Blue").place(x=350, y=200)
Label(main_win, text="Father name", bg="Light Blue").place(x=600, y=200)
Label(main_win, text="Mother name", bg="Light Blue").place(x=850, y=200)
Label(main_win, text="Gender", bg="Light Blue").place(x=100, y=250)
Label(main_win, text="Date of Birth", bg="Light Blue").place(x=350, y=250)
Label(main_win, text="Place of Birth", bg="Light Blue").place(x=600, y=250)
Label(main_win, text="Age", bg="Light Blue").place(x=850, y=250)
Label(main_win, text="Height", bg="Light Blue").place(x=100, y=300)
Label(main_win, text="weight", bg="Light Blue").place(x=350, y=300)
Label(main_win, text="Waist", bg="Light Blue").place(x=600, y=300)
Label(main_win, text="BMI", bg="Light Blue").place(x=850, y=300)
Label(main_win, text="Blood Group", bg="Light Blue").place(x=100, y=350)
Label(main_win, text="Marial Status", bg="Light Blue").place(x=350, y=350)
Label(main_win, text="Husband / Wife", bg="Light Blue").place(x=600, y=350)
Label(main_win, text="No of Childern", bg="Light Blue").place(x=850, y=350)
Label(main_win, text="Name of Childern", bg="Light Blue").place(x=100, y=400)
Label(main_win, text="Qualification", bg="Light Blue").place(x=350, y=400)
Label(main_win, text="Degree", bg="Light Blue").place(x=600, y=400)
Label(main_win, text="Job", bg="Light Blue").place(x=850, y=400)
Label(main_win, text="Country", bg="Light Blue").place(x=100, y=450)
Label(main_win, text="Province", bg="Light Blue").place(x=350, y=450)
Label(main_win, text="State", bg="Light Blue").place(x=600, y=450)
Label(main_win, text="City", bg="Light Blue").place(x=850, y=450)
Label(main_win, text="Address", bg="Light Blue").place(x=100, y=500)
Label(main_win, text="Zipcode", bg="Light Blue").place(x=350, y=500)

Label(editor_win, text="First name", bg="Light Blue").place(x=100, y=200)
Label(editor_win, text="Last name", bg="Light Blue").place(x=350, y=200)
Label(editor_win, text="Father name", bg="Light Blue").place(x=600, y=200)
Label(editor_win, text="Mother name", bg="Light Blue").place(x=850, y=200)
Label(editor_win, text="Gender", bg="Light Blue").place(x=100, y=250)
Label(editor_win, text="Date of Birth", bg="Light Blue").place(x=350, y=250)
Label(editor_win, text="Place of Birth", bg="Light Blue").place(x=600, y=250)
Label(editor_win, text="Age", bg="Light Blue").place(x=850, y=250)
Label(editor_win, text="Height", bg="Light Blue").place(x=100, y=300)
Label(editor_win, text="weight", bg="Light Blue").place(x=350, y=300)
Label(editor_win, text="Waist", bg="Light Blue").place(x=600, y=300)
Label(editor_win, text="BMI", bg="Light Blue").place(x=850, y=300)
Label(editor_win, text="Blood Group", bg="Light Blue").place(x=100, y=350)
Label(editor_win, text="Marial Status", bg="Light Blue").place(x=350, y=350)
Label(editor_win, text="Husband / Wife", bg="Light Blue").place(x=600, y=350)
Label(editor_win, text="No of Childern", bg="Light Blue").place(x=850, y=350)
Label(editor_win, text="Name of Childern", bg="Light Blue").place(x=100, y=400)
Label(editor_win, text="Qualification", bg="Light Blue").place(x=350, y=400)
Label(editor_win, text="Degree", bg="Light Blue").place(x=600, y=400)
Label(editor_win, text="Job", bg="Light Blue").place(x=850, y=400)
Label(editor_win, text="Country", bg="Light Blue").place(x=100, y=450)
Label(editor_win, text="Province", bg="Light Blue").place(x=350, y=450)
Label(editor_win, text="State", bg="Light Blue").place(x=600, y=450)
Label(editor_win, text="City", bg="Light Blue").place(x=850, y=450)
Label(editor_win, text="Address", bg="Light Blue").place(x=100, y=500)
Label(editor_win, text="Zipcode", bg="Light Blue").place(x=350, y=500)

Button(main_win, text="Update Records in DataBase", padx=10, pady=5, state=ACTIVE, command=submit).place(x=500, y=700)
Button(main_win, text="E D I T", padx=10, pady=5, state=ACTIVE, command=edit).place(x=500, y=650)
Button(main_win, text="S H O W", padx=10, pady=5, state=ACTIVE, command=query).place(x=700, y=650)
Button(editor_win, text="Update Records in DataBase", padx=10, pady=5, state=ACTIVE, command=update).place(x=500, y=700)

connection1.commit()
connection2.commit()

connection1.close()
connection2.close()

win1.mainloop()
