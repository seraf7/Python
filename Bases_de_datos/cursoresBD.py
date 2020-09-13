import sqlite3

#Conexion con la base de datos, usa una base de datos en memoria
#Se pierde cuando se termina el programa
conn = sqlite3.connect(':memory:')

#Creacion de un cursor
cursor = conn.cursor()

#Creacion de una tabla
cursor.execute("""CREATE TABLE divisas (
	id INTEGER PRIMARY KEY, nombre TEXT, simbolo TEXT);""")

#Insertar registros en la tabla
cursor.execute("INSERT INTO divisas VALUES(1, 'Peso(MXN)', '$');")
cursor.execute("INSERT INTO divisas VALUES(2, 'Dolar USD', 'U$S');")

#Guardar los cambios en la base de datos
conn.commit()

#Ejecucion de una consulta
query = "SELECT * FROM divisas;"

#Busco resultado de la consulta, un registro a la vez
divisas = cursor.execute(query).fetchone()
print(divisas)

print(cursor.fetchone())
print(cursor.fetchone())

#Busco resultado de la consulta, todos los registros a la vez
divisas = cursor.execute(query).fetchall()
print(divisas)

#Cierra base de datos
conn.close()