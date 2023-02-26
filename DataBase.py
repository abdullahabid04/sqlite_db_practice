from tkinter import *
from PIL import Image, ImageTk
import sqlite3


main_win = Tk()

icon = ImageTk.PhotoImage(Image.open("images/lab_logo.png"))

main_win.title("DataBase Handling")
main_win.wm_iconphoto(main_win, icon)
main_win.geometry("1200x800")
main_win.config(bg="Light Blue")

name_label_main = Label(main_win, text="D A T A B A S E   O F   C I T I Z E N S   O F   P A K I S T A N", font=("Arial", 15, "bold"), fg="Dark Blue", bg="Light Blue", padx=10, pady=10)
name_label_main.place(x=300, y=50)

connection = sqlite3.connect("files/People's Data.db")

cursor = connection.cursor()


'''
cursor1.execute("""CREATE TABLE addresses (
                first_name text,
                last_name text,
                father_name text,
                mother_name text,
                gender text,
                date_of_birth integer,
                place_of_birth text,
                age integer,
                height integer,
                weight integer,
                waist integer,
                BMI integer,
                blood_group text,
                marial_status text,
                husband_OR_wife_name text,
                no_of_childern integer,
                qualification text,
                degree text,
                job text,
                country text, 
                province text,
                state text,
                city text,
                address text,
                zipcode integer
                )
            """)
'''


def submit():
    connection = sqlite3.connect("files/People's Data.db")

    cursor = connection.cursor()

    cursor.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :father_name, :mother_name, :gender, :date_of_birth, :place_of_birth, :age, :height, :weight, :waist, :BMI, :blood_group, :marial_status, :husband_OR_wife_name, :no_of_childern, :qualification, :degree, :job, :country, :province, :state, :city, :address, :zipcode)",
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

    connection.commit()

    connection.close()

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
    connection = sqlite3.connect("files/People's Data.db")

    cursor = connection.cursor()

    cursor.execute("SELECT *, oid FROM addresses")
    records = cursor.fetchall()

    print_records = ""

    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) + " " \
                         + str(record[4]) + " " + str(record[5]) + " " + str(record[6]) + " " + str(record[7]) + " " \
                         + str(record[8]) + " " + str(record[9]) + " " + str(record[10]) + " " + str(record[11]) + " " \
                         + str(record[12]) + " " + str(record[13]) + " " + str(record[14]) + " " + str(record[15]) + " "\
                         + str(record[16]) + " " + str(record[17]) + " " + str(record[18]) + " " + str(record[19]) + " " \
                         + str(record[20]) + " " + str(record[21]) + " " + str(record[22]) + " " + str(record[23]) + " " \
                         + str(record[24]) + " " + str(record[25]) + " " + "\n"

    records_win = Tk()
    records_win.title("Records")
    records_win.geometry("1200x200")

    record_label = Label(records_win, text=print_records)
    record_label.grid(row=0, column=0)

    connection.commit()

    connection.close()


def delete():
    connection = sqlite3.connect("files/People's Data.db")

    cursor = connection.cursor()

    cursor.execute("DELETE from addresses WHERE oid = " + select_id.get())

    select_id.delete(0, END)

    connection.commit()

    connection.close()


def edit():
    global editor_win

    editor_win = Tk()
    editor_win.title("Update records")
    editor_win.geometry("1200x800")
    editor_win.config(bg="Light Blue")

    name_label_editor = Label(editor_win, text="U P D A T E   D A T A B A S E   O F   C I T I Z E N S   O F   P A K I S T A N", font=("Arial", 15, "bold"), fg="Dark Blue", bg="Light Blue", padx=10, pady=10)
    name_label_editor.place(x=250, y=50)

    connection = sqlite3.connect("files/People's Data.db")

    cursor = connection.cursor()

    record_id = select_id.get()

    cursor.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    records = cursor.fetchall()

    global f_name_editor
    global l_name_editor
    global father_name_editor
    global mother_name_editor
    global gender_editor
    global date_of_birth_editor
    global place_of_birth_editor
    global age_editor
    global height_editor
    global weight_editor
    global waist_editor
    global BMI_editor
    global blood_group_editor
    global marial_status_editor
    global husband_OR_wife_name_editor
    global no_of_childern_editor
    global qualification_editor
    global degree_editor
    global job_editor
    global country_editor
    global province_editor
    global state_editor
    global city_editor
    global address_editor
    global zipcode_editor

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
    qualification_editor = Entry(editor_win, width=20)
    qualification_editor.place(x=200, y=400)
    degree_editor = Entry(editor_win, width=20)
    degree_editor.place(x=450, y=400)
    job_editor = Entry(editor_win, width=20)
    job_editor.place(x=700, y=400)
    country_editor = Entry(editor_win, width=20)
    country_editor.place(x=950, y=400)
    province_editor = Entry(editor_win, width=20)
    province_editor.place(x=200, y=450)
    state_editor = Entry(editor_win, width=20)
    state_editor.place(x=450, y=450)
    city_editor = Entry(editor_win, width=20)
    city_editor.place(x=700, y=450)
    address_editor = Entry(editor_win, width=20)
    address_editor.place(x=950, y=450)
    zipcode_editor = Entry(editor_win, width=20)
    zipcode_editor.place(x=200, y=500)

    f_name_label_editor = Label(editor_win, text="First name", bg="Light Blue")
    f_name_label_editor.place(x=100, y=200)
    l_name_label_editor = Label(editor_win, text="Last name", bg="Light Blue")
    l_name_label_editor.place(x=350, y=200)
    father_name_label_editor = Label(editor_win, text="Father name", bg="Light Blue")
    father_name_label_editor.place(x=600, y=200)
    mother_name_label_editor = Label(editor_win, text="Mother name", bg="Light Blue")
    mother_name_label_editor.place(x=850, y=200)
    gender_label_editor = Label(editor_win, text="Gender", bg="Light Blue")
    gender_label_editor.place(x=100, y=250)
    date_of_birth_label_editor = Label(editor_win, text="Date of Birth", bg="Light Blue")
    date_of_birth_label_editor.place(x=350, y=250)
    place_of_birth_label_editor = Label(editor_win, text="Place of Birth", bg="Light Blue")
    place_of_birth_label_editor.place(x=600, y=250)
    age_label_editor = Label(editor_win, text="Age", bg="Light Blue")
    age_label_editor.place(x=850, y=250)
    height_label_editor = Label(editor_win, text="Height", bg="Light Blue")
    height_label_editor.place(x=100, y=300)
    weight_label_editor = Label(editor_win, text="weight", bg="Light Blue")
    weight_label_editor.place(x=350, y=300)
    waist_label_editor = Label(editor_win, text="Waist", bg="Light Blue")
    waist_label_editor.place(x=600, y=300)
    BMI_label_editor = Label(editor_win, text="BMI", bg="Light Blue")
    BMI_label_editor.place(x=850, y=300)
    blood_group_label_editor = Label(editor_win, text="Blood Group", bg="Light Blue")
    blood_group_label_editor.place(x=100, y=350)
    marial_status_label_editor = Label(editor_win, text="Marial Status", bg="Light Blue")
    marial_status_label_editor.place(x=350, y=350)
    husband_OR_wife_name_label_editor = Label(editor_win, text="Husband / Wife", bg="Light Blue")
    husband_OR_wife_name_label_editor.place(x=600, y=350)
    no_of_childern_label_editor = Label(editor_win, text="No of Childern", bg="Light Blue")
    no_of_childern_label_editor.place(x=850, y=350)
    qualification_label_editor = Label(editor_win, text="Qualification", bg="Light Blue")
    qualification_label_editor.place(x=100, y=400)
    degree_label_editor = Label(editor_win, text="Degree", bg="Light Blue")
    degree_label_editor.place(x=350, y=400)
    job_label_editor = Label(editor_win, text="Job", bg="Light Blue")
    job_label_editor.place(x=600, y=400)
    country_label_editor = Label(editor_win, text="Country", bg="Light Blue")
    country_label_editor.place(x=850, y=400)
    province_label_editor = Label(editor_win, text="Province", bg="Light Blue")
    province_label_editor.place(x=100, y=450)
    state_label_editor = Label(editor_win, text="State", bg="Light Blue")
    state_label_editor.place(x=350, y=450)
    city_label_editor = Label(editor_win, text="City", bg="Light Blue")
    city_label_editor.place(x=600, y=450)
    address_label_editor = Label(editor_win, text="Address", bg="Light Blue")
    address_label_editor.place(x=850, y=450)
    zipcode_label_editor = Label(editor_win, text="Zipcode", bg="Light Blue")
    zipcode_label_editor.place(x=100, y=500)

    save_btn = Button(editor_win, text="Update Records in DataBase", padx=10, pady=5, command=update)
    save_btn.place(x=550, y=700)

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
        qualification_editor.insert(0, record[16])
        degree_editor.insert(0, record[17])
        job_editor.insert(0, record[18])
        country_editor.insert(0, record[19])
        province_editor.insert(0, record[20])
        state_editor.insert(0, record[21])
        city_editor.insert(0, record[22])
        address_editor.insert(0, record[23])
        zipcode_editor.insert(0, record[24])


def update():
    connection = sqlite3.connect("files/People's Data.db")

    cursor = connection.cursor()

    record_id = select_id.get()

    cursor.execute("""UPDATE addresses SET 
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

    connection.commit()

    connection.close()

    editor_win.destroy()


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
qualification = Entry(main_win, width=20)
qualification.place(x=200, y=400)
degree = Entry(main_win, width=20)
degree.place(x=450, y=400)
job = Entry(main_win, width=20)
job.place(x=700, y=400)
country = Entry(main_win, width=20)
country.place(x=950, y=400)
province = Entry(main_win, width=20)
province.place(x=200, y=450)
state = Entry(main_win, width=20)
state.place(x=450, y=450)
city = Entry(main_win, width=20)
city.place(x=700, y=450)
address = Entry(main_win, width=20)
address.place(x=950, y=450)
zipcode = Entry(main_win, width=20)
zipcode.place(x=200, y=500)

select_id = Entry(main_win, width=20)
select_id.place(x=600, y=650)

f_name_label = Label(main_win, text="First name", bg="Light Blue")
f_name_label.place(x=100, y=200)
l_name_label = Label(main_win, text="Last name", bg="Light Blue")
l_name_label.place(x=350, y=200)
father_name_label = Label(main_win, text="Father name", bg="Light Blue")
father_name_label.place(x=600, y=200)
mother_name_label = Label(main_win, text="Mother name", bg="Light Blue")
mother_name_label.place(x=850, y=200)
gender_label = Label(main_win, text="Gender", bg="Light Blue")
gender_label.place(x=100, y=250)
date_of_birth_label = Label(main_win, text="Date of Birth", bg="Light Blue")
date_of_birth_label.place(x=350, y=250)
place_of_birth_label = Label(main_win, text="Place of Birth", bg="Light Blue")
place_of_birth_label.place(x=600, y=250)
age_label = Label(main_win, text="Age", bg="Light Blue")
age_label.place(x=850, y=250)
height_label = Label(main_win, text="Height", bg="Light Blue")
height_label.place(x=100, y=300)
weight_label = Label(main_win, text="weight", bg="Light Blue")
weight_label.place(x=350, y=300)
waist_label = Label(main_win, text="Waist", bg="Light Blue")
waist_label.place(x=600, y=300)
BMI_label = Label(main_win, text="BMI", bg="Light Blue")
BMI_label.place(x=850, y=300)
blood_group_label = Label(main_win, text="Blood Group", bg="Light Blue")
blood_group_label.place(x=100, y=350)
marial_status_label = Label(main_win, text="Marial Status", bg="Light Blue")
marial_status_label.place(x=350, y=350)
husband_OR_wife_name_label = Label(main_win, text="Husband / Wife", bg="Light Blue")
husband_OR_wife_name_label.place(x=600, y=350)
no_of_childern_label = Label(main_win, text="No of Childern", bg="Light Blue")
no_of_childern_label.place(x=850, y=350)
qualification_label = Label(main_win, text="Qualification", bg="Light Blue")
qualification_label.place(x=100, y=400)
degree_label = Label(main_win, text="Degree", bg="Light Blue")
degree_label.place(x=350, y=400)
job_label = Label(main_win, text="Job", bg="Light Blue")
job_label.place(x=600, y=400)
country_label = Label(main_win, text="Country", bg="Light Blue")
country_label.place(x=850, y=400)
province_label = Label(main_win, text="Province", bg="Light Blue")
province_label.place(x=100, y=450)
state_label = Label(main_win, text="State", bg="Light Blue")
state_label.place(x=350, y=450)
city_label = Label(main_win, text="City", bg="Light Blue")
city_label.place(x=600, y=450)
address_label = Label(main_win, text="Address", bg="Light Blue")
address_label.place(x=850, y=450)
zipcode_label = Label(main_win, text="Zipcode", bg="Light Blue")
zipcode_label.place(x=100, y=500)

select_id_label = Label(main_win, text="Select id", bg="Light Blue")
select_id_label.place(x=500, y=650)

submit_btn = Button(main_win, text="Add record to database", padx=25, pady=5, height=1, width=40, command=submit)
submit_btn.place(x=450, y=600)
query_btn = Button(main_win, text="Show Records", padx=10, pady=3, command=query)
query_btn.place(x=575, y=700)
delete_btn = Button(main_win, text="Delete Records", padx=10, pady=3, command=delete)
delete_btn.place(x=350, y=700)
edit_btn = Button(main_win, text="Edit Records", padx=10, pady=3, command=edit)
edit_btn.place(x=800, y=700)

connection.commit()

connection.close()

main_win.mainloop()
