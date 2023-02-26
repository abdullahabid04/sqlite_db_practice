import sqlite3


connection = sqlite3.connect("files/Accounts.db")

cursor = connection.cursor()

cursor.execute("""CREATE TABLE logged_users (
                line text
                )
            """)

connection.commit()

connection.close()
