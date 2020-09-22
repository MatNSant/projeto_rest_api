import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"   
cursor.execute(create_table)

user = (1, "Matheus", "oasuet10")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, "João", "1234",),
    (3, "Vini", "4321",),
]

cursor.executemany(insert_query, users)

query = "SELECT * FROM users"  # '*' = todas as colunas, muda por "id" se quiser id  
for row in cursor.execute(select_querry):
    print(row)


connection.commit()
connection.close()
