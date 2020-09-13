from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import exists

#Conexion con la base de datos
engine = create_engine('sqlite:///:memory:')

#Clase base declarativa
Base = declarative_base()

#Definicion de la clase Autor
class Autor(Base):
	#Asociacion a una tabla de la BD
	__tablename__ = 'autor'

	#Mapeo de atributos y campos de la tabla
	id = Column(Integer, Sequence('autor_id_seq'), primary_key=True)
	nombre = Column(String)
	apellido = Column(String)

	#Relacion con tabla libro, cascade es atributo para borrado
	libros = relationship('Libro', order_by='Libro.id', back_populates='autor',
		cascade="all, delete, delete-orphan")

	def  __repr__(self):
		return "{} {}".format(self.nombre, self.apellido)

#Definicion de la clase libro
class Libro(Base):
	#Asociacion a una tabla de la BD
	__tablename__ = 'libro'

	#Mapeo de atributos y campos de la tabla
	id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
	isbn = Column(String)
	titulo = Column(String)
	descripcion = Column(String)
	#Definicion de clave foranea
	autor_id = Column(Integer, ForeignKey('autor.id'))

	#Relacion con el atributo autor
	autor = relationship("Autor", back_populates="libros")

	def __repr__(self):
		return "{}".format(self.titulo)

#Creacion de las tablas
Base.metadata.create_all(engine)

#Creacion de una sesion
Session = sessionmaker(bind=engine)
sesion = Session()

#Creacion de un autor
antoine = Autor(nombre = "Antoine", apellido = "de Saint")

#Imprime los libros asociados al autor
print(antoine.libros)

#Insercion de libros al autor
antoine.libros = [
Libro(isbn = "93747", titulo="El Principito", descripcion="El tiempo con tu rosa..."),
Libro(isbn = "27388", titulo="Carta a un rehen", descripcion="En la sonrisa nos reunimos...")]

#Impresion de atributos
print(antoine.libros[1])
print(antoine.libros[1].titulo)

#Agregar autor a la BD
sesion.add(antoine)
sesion.commit()

#Consulta a la BD
antoine = sesion.query(Autor).filter_by(nombre="Antoine").one()
print(antoine.libros)

###########Pruebas de consultas##############
#Autor y libro para un isbn determinado
print("\nQuery 1")
for autor, libro in sesion.query(Autor, Libro).filter(Autor.id == Libro.autor_id).filter(Libro.isbn == "93747").all():
	print(autor)
	print(libro)

#Autor del libro con un isbn determinado
print("\nQuery 2")
print(sesion.query(Autor).join(Libro).filter(Libro.isbn == "93747").all())

#Autores de los libros mediante condicion explicita
print("\nQuery 3")
print(sesion.query(Autor).join(Libro, Autor.id == Libro.autor_id).all())

#Autores de libros mediante realcion de izquierda a derecha
print("\nQuery 4")
print(sesion.query(Autor).join(Autor.libros).all())

#Autores de los libros para una relacion especifica
print("\nQuery 5")
print(sesion.query(Autor).join(Libro, Autor.libros).all())

#Autores de los libros mediante un string
print("\nQuery 6")
print(sesion.query(Autor).join('libros').all())

#Nombre del autor del libro mediante filtro exist
print("\nQuery 7")
stmt = exists().where(Libro.autor_id == Autor.id)
for name, in sesion.query(Autor.nombre).filter(stmt):
	print(name)

#Nombre del autor del libro con filtro any
print("\nQuery 8")
for name, in sesion.query(Autor.nombre).filter(Autor.libros.any()):
	print(name)

#Nombre del autor del libro con filtro like
print("\nQuery 9")
for name, in sesion.query(Autor.nombre).filter(Autor.libros.any(Autor.apellido.like('% Saint%'))):
	print(name)

#Libros donde el autor no se llama Antoine
print("\nQuery 10")
print(sesion.query(Libro).filter(~Libro.autor.has(Autor.nombre=='Antoine')).all())

###########Pruebas de borrado#############
sesion.delete(antoine)

print(sesion.query(Autor).filter_by(nombre='Antoine').count())

print(sesion.query(Libro).filter(Libro.isbn.in_(["93747", "27388"])).count())