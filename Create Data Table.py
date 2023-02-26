import sqlite3


connection = sqlite3.connect("files/People's Data.db")

cursor = connection.cursor()


cursor.execute("""CREATE TABLE data (
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
                name_of_childerns text,
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

connection.commit()

connection.close()
