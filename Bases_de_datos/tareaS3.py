import sqlite3

#Crea conexion con BD
conn = sqlite3.connect(':memory:')

#Creacion de un cursor
cursor = conn.cursor()

#Creacion de una tabla
cursor.execute("""CREATE TABLE table_1
	(id INTEGER PRIMARY KEY, name TEXT);""")

#Insercion de un registro
cursor.execute("INSERT INTO table_1 VALUES(1, 'prueba');")

conn.commit()

#Definicion de un query
query = "SELECT * FROM table_1"

#Busqueda de registros de la consulta
currencies = cursor.execute(query).fetchall()
print(currencies)

#Cierra conexion con la base de datos
conn.close()