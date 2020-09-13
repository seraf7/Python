# -*- coding: utf-8 -*-

import sqlite3

#Path de la base de datos
db_path = 'prueba2'

#Clase de excepcion para divisa inexistente
class DivisaInexistente(Exception):
	pass

#Manejador de divisas en la DB
class DivisasManager:
	def __init__(self, database = None):
		#Si no hay una base de datos, se crea una conexion a memoria
		if not database:
			database = ':memory:'
		#Crea conexion con la BD
		self.conn = sqlite3.connect(database)
		#Crea un cursor para la BD
		self.cursor = self.conn.cursor()

	#Metodo para insertar objeto a la BD
	def insertar(self, divisa):
		query = 'INSERT INTO divisa VALUES ("{}", "{}", "{}")'.format(divisa.codigo, divisa.nombre, divisa.simbolo)
		#Ejecuta el comando de insercion
		self.cursor.execute(query)
		#Guarda los cambios en la BD
		self.conn.commit()

	#Metodo para obtener una divisa por su codigo
	def get(self, codigo):
		query = 'SELECT * FROM divisa WHERE codigo = "{}";'.format(codigo)
		self.cursor.execute(query)
		data = self.cursor.fetchone()
		#Valida que se devolvió un registro
		if not data:
			raise DivisaInexistente("No existe la moneda de codigo {}".format(codigo))
		return Divisa(data[0], data[1], data[2])

	#Metodo para filtrar datos
	def filtro(self, **kwargs):
		#Asignacion de los parametros ingresados
		codigo = kwargs.get('codigo')
		nombre = kwargs.get('nombre')
		simbolo = kwargs.get('simbolo')

		condicion = " WHERE "
		add_and = False
		add_condition = False

		#Valida que se ingreso un codigo
		if codigo:
			condicion += 'codigo = "{}" '.format(codigo)
			add_condition = True
			add_and = True

		#Valida que se ingreso un nombre
		if nombre:
			#Valida si hay una condicion previa
			if add_and:
				condicion += "AND "
			condicion += 'nombre = "{}" '.format(nombre)
			add_condition = True
			add_and = True

		#Valida que se ingreso un simbolo
		if simbolo:
			#Valida si hay una condicion previa
			if add_and:
				condicion += "AND "
			condicion += 'simbolo = "{}"'.format(simbolo)
			add_condition = True

		query = "SELECT * FROM divisa"
		#Valida si se creo algun filtro
		if add_condition:
			query += condicion

		self.cursor.execute(query)
		resultado = self.cursor.fetchall()

		divisas = []
		#Ingresa resultados de la consulta en una lista
		for data in resultado:
			#Crea objeto del registro
			divisa = Divisa(data[0], data[1], data[2])
			divisas.append(divisa)

		return divisas

	#Metodo para actualizar un objeto de la BD
	def actualizar(self, old, new):
		update = False
		add_comma = False

		query = 'UPDATE divisa SET'

		#Valida cambio en el nombre
		if old.nombre != new.nombre:
			query += ' nombre = "{}"'.format(new.nombre)
			update = True
			add_comma = True
		#Valida cambio de simbolo
		if old.simbolo != new.simbolo:
			#Valida si hay un cambio previo
			if add_comma:
				query += ', '
			query += 'simbolo = "{}"'.format(new.simbolo)
			update = True

		if update:
			#Para actualizar solo objeto especifico
			query += ' WHERE codigo = "{}"'.format(new.codigo)
			self.cursor.execute(query)
			self.conn.commit()

	#Metodo para guardar un objeto
	def guardar(self, divisa):
		#Busca objeto mediante codigo
		try:
			old = self.get(divisa.codigo)
		#Excepcion cuando no es encontrado el objeto
		except DivisaInexistente:
			self.insertar(divisa)
		#Caso general
		else:
			self.actualizar(old, divisa)

	#Metodo para borrar un registro
	def borrar(self, divisa):
		query = 'DELETE FROM divisa WHERE codigo = "{}"'.format(divisa.codigo)
		self.cursor.execute(query)
		self.conn.commit()

	#Metodo para liberar recursos
	def cerrar(self):
		self.conn.close()

#Definicion de la clase Divisa
class Divisa:
	#Variable de clase con el path de la DB
	db = DivisasManager(db_path)

	def __init__(self, codigo, nombre, simbolo):
		self.codigo = codigo
		self.nombre = nombre
		self.simbolo = simbolo

	def __repr__(self):
		return '{}'.format(self.nombre)


#Instancia de divisas
#Es necesario insertar comillas dos veces para que se interpreten
#los valores como texto en la BD
"""peso = Divisa("MXN", "Peso (MXN)", "$")
dolar = Divisa("USD", "Dolar", "U$D")
euro = Divisa("EUR", "Euro", "€")

#Insercion de divisas mediante variable de clase
Divisa.db.insertar(peso)
Divisa.db.insertar(dolar)
Divisa.db.insertar(euro)

#Buscar moneda mediante su codigo
print(Divisa.db.get("MXN"))

#Buscar moneda no existente mediante su codigo
print(Divisa.db.get("MXP"))

#Buscar moneda con filtros
print(Divisa.db.filtro(codigo = "EUR"))
print(Divisa.db.filtro(nombre = "Dolar"))
print(Divisa.db.filtro(simbolo = "€"))

#Buscar moneda sin filtros
print(Divisa.db.filtro())

################Pruebas de actualizar y guardar##################
peso = Divisa.db.get("MXN")
Divisa.db.guardar(peso)

peso = Divisa.db.get("MXN")
print(peso.codigo)
print(peso.nombre)
print(peso.simbolo)

#Cambio en el nombre
peso.nombre = 'Peso (MEX)'
Divisa.db.guardar(peso)

#Para verificar informacion
peso = Divisa.db.get("MXN")
print(peso.codigo)
print(peso.nombre)
print(peso.simbolo)

#Instancia de nueva moneda
centimo = Divisa("CEN", "Centimo", "¢")
#Guardar moneda no existente
Divisa.db.guardar(centimo)

centimo = Divisa.db.get("CEN")
print(centimo.codigo)
print(centimo.nombre)
print(centimo.simbolo)
"""

######Prueba de borrado#######
centimo = Divisa.db.get("CEN")
Divisa.db.borrar(centimo)
centimo = Divisa.db.get("CEN")

#Finalizar conexion
Divisa.db.cerrar()