import sqlite3
import hashlib

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

#Revierte los cambios realizados en la base de datos
conn.rollback()

#Ejecucion de una consulta
query = "SELECT * FROM divisas;"

#Busco resultado de la consulta
divisas = cursor.execute(query).fetchall()

print(divisas)

#Cierra conexion con la base de datos
conn.close()

#Crear una funcion
def md5sum(t):
	#Realiza un hash del parametro dado
	return hashlib.md5(t).hexdigest()

conn = sqlite3.connect(":memory:")
#Crea conexion con la funcion md5
conn.create_function("md5", 1, md5sum)
cursor = conn.cursor()
#El signo ? se cambia por foo
cursor.execute("SELECT md5(?)", (b"foo",))
print(cursor.fetchone()[0])

#Se cierra la conexion
conn.close()

#Para funcion de agregacion
class MySum:
	def __init__(self):
		self.count = 0

	def step(self, value):
		self.count += value

	def finalize(self):
		return self.count

conn = sqlite3.connect(":memory:")
#Crea la funcion de agregacion
conn.create_aggregate("mysum", 1, MySum)
cursor = conn.cursor()
cursor.execute("CREATE TABLE test(i)")
cursor.execute("INSERT INTO test(i) VALUES (1)")
cursor.execute("INSERT INTO test(i) VALUES (2)")
#Llama a la funcion mysum para ser ejecutada
cursor.execute("SELECT mysum(i) FROM test")
print(cursor.fetchone()[0])

#Cierra conexion con la basse de datos
conn.close()