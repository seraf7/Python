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
class Author(Base):
	#Asociacion a una tabla de la BD
	__tablename__ = 'author'

	#Mapeo de atributos y campos de la tabla
	id = Column(Integer, Sequence('autor_id_seq'), primary_key=True)
	firstname = Column(String)
	lastname = Column(String)

	#Relacion con tabla libro
	books = relationship('Book', order_by='Book.id', back_populates='author')

	def  __repr__(self):
		return "{} {}".format(self.firstname, self.lastname)

#Definicion de la clase libro
class Book(Base):
	#Asociacion a una tabla de la BD
	__tablename__ = 'book'

	#Mapeo de atributos y campos de la tabla
	id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
	isbn = Column(String)
	title = Column(String)
	#Definicion de clave foranea
	author_id = Column(Integer, ForeignKey('author.id'))

	#Relacion con el atributo autor
	author = relationship("Author", back_populates="books")

	def __repr__(self):
		return "{}".format(self.titulo)

#Creacion de las tablas
Base.metadata.create_all(engine)

#Creacion de una sesion
Session = sessionmaker(bind=engine)
sesion = Session()

autores = [
	Author(firstname='firstname1', lastname='lastname1'),
	Author(firstname='firstname2', lastname='lastname2'),
	Author(firstname='firstname3', lastname='lastname3')]

autores[1].books = [
	Book(isbn='isbn1', title='title1'),
	Book(isbn='isbn3', title='title3')]

autores[2].books = [Book(isbn='isbn2', title='title2')]

sesion.add_all(autores)

print(sesion.query(Author.firstname).filter(Author.books.any()).count())

for libro in sesion.query(Book):
	print("{} {}".format(libro.id, libro.title))