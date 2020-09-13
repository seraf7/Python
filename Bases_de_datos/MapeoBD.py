from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased

#Clase base declarativa
Base = declarative_base()

#Definicion de clase Autor, hereda de clase base
class Autor(Base):
	#Asociacion a una tabla
	__tablename__ = 'autor'

	#Mapeo de columnas y atributos
	id = Column(Integer, Sequence('autor_id_seq'), primary_key=True)
	nombre = Column(String)
	apellido = Column(String)

	def __repr__(self):
		return "{} {}".format(self.nombre, self.apellido)

#Conexion con la base de datos
engine = create_engine('sqlite:///:memory:')

#Crea todas las tablas que no han sido creadas
Base.metadata.create_all(engine)

#Clase sesion para poder crear sesiones a la base dada
Session = sessionmaker(bind = engine)
sesion = Session()

#Creacion de un autor
autor = Autor(nombre = "Federico", apellido = "Garcia")

#Agregar objeto a la BD
sesion.add(autor)

#Realizar consulta a la BD
nuestro = sesion.query(Autor).filter_by(nombre = 'Federico').first()

#Comprueba que nuestra instancia y objeto de la consulta son el mismo
print(autor is nuestro)

#Agregar lista de objetos a la base
sesion.add_all([
	Autor(nombre = 'Gabriel', apellido = 'Garcia'),
	Autor(nombre = 'Miguel', apellido = 'De Cervantes')])

#Devuelve registros en la sesion que no han sido guardados
sesion.new

#Devuelve cambios en sesion no guardados en la BD
sesion.dirty

#Guardar cambios en la BD
sesion.commit()

#Revertir cambios en la BD
sesion.rollback()

###########Ejemplos de consultas#################

#Autores ordenados por id
print("\nQuery 1")
for instancia in sesion.query(Autor).order_by(Autor.id):
	print(instancia.nombre, instancia.apellido)

#Nombre y apellido de cada autor
print("\nQuery 2")
for nombre, apellido in sesion.query(Autor.nombre, Autor.apellido):
	print(nombre, apellido)

#Autor y primer nombre
print("\nQuery 3")
for row in sesion.query(Autor, Autor.nombre).all():
	print(row.Autor, row.nombre)

#Autores y asignacion de etiqueta
print("\nQuery 4")
for row in sesion.query(Autor.nombre.label('nom')).all():
	print(row.nom)

#Autor y primer nombre, mediante un alias
print("\nQuery 5")
autor_alias = aliased(Autor, name='autor_alias')
for row in sesion.query(autor_alias, autor_alias.nombre).all():
	print(row.autor_alias)

#Todos los autores, pero conservando 2 y 3
print("\nQuery 6")
for un_autor in sesion.query(Autor).order_by(Autor.id)[1:3]:
	print(un_autor)

#Autores con nombre Federico
print("\nQuery 7")
for nombre, in sesion.query(Autor.nombre).filter_by(nombre='Federico'):
	print(nombre)

#Filtro mediante apellido
print("\nQuery 8")
for nombre, in sesion.query(Autor.nombre).filter(Autor.apellido=='Garcia'):
	print(nombre)

#Filtro mediante nombre y apellido
print("\nQuery 9")
for autor in sesion.query(Autor).filter(Autor.nombre=='Federico').filter(Autor.apellido=='Garcia'):
	print(autor)

#Cantidad de autores con nombre Federico
print("\nQuery 10")
print(sesion.query(Autor).filter(Autor.nombre=='Federico').count())