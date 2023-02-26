import sqlite3


connection = sqlite3.connect("files/Accounts.db")

cursor = connection.cursor()

cursor.execute("""CREATE TABLE accounts (
                user_name text,
                email_id text,
                pass text
                )
            """)

connection.commit()

connection.close()
