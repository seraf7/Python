from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Table, Text

#Conexion con la base de datos
engine = create_engine('sqlite:///:memory:')

#Clase base declarativa
Base = declarative_base()

#Tabla de asociacion Libro-Categoria
libro_categoria = Table('libro_categoria', Base.metadata,
	Column('libro_id', ForeignKey('libro.id'), primary_key=True),
	Column('categoria_id', ForeignKey('categoria.id'), primary_key=True))

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

#Definicion de la calse Categoria
class Categoria(Base):
	__tablename__ = 'categoria'
	id = Column(Integer, Sequence('categoria_id_seq'), primary_key=True)
	nombre = Column(String)

	#Relacion con el atributo libro
	libros = relationship('Libro', secondary=libro_categoria, back_populates='categorias')

	def __repr__(self):
		return "{}".format(self.nombre)

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

	categorias = relationship('Categoria', secondary=libro_categoria, back_populates='libros')

	def __repr__(self):
		return "{}".format(self.titulo)


#Creacion de las tablas
Base.metadata.create_all(engine)

#Creacion de una sesion
Session = sessionmaker(bind=engine)
sesion = Session()

#Creacion de un autor
antoine = Autor(nombre = "Antoine", apellido = "de Saint")
sesion.add(antoine)

antoine = sesion.query(Autor).filter_by(nombre='Antoine').one()

#Creacion de un libro
libro = Libro(isbn='27373', titulo='El Principito', descripcion='Libro para no niños...')

#Adicion de categorias al libro
libro.categorias.append(Categoria(nombre='Fantasia'))
libro.categorias.append(Categoria(nombre='Aventura'))

#Asociacion del libro y autor
libro.autor = antoine

#Libros con la categoria Fantasia
print(sesion.query(Libro).filter(Libro.categorias.any(nombre='Fantasia')).all())

#Libros con autor Antoine y categoria Fantasia
print(sesion.query(Libro).filter(Libro.autor==antoine).filter(Libro.categorias.any(nombre='Fantasia')).all())