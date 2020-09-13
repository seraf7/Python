from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker

#Clase base declarativa
Base = declarative_base()

class Author(Base):
	#Asociacion a una tabla
	__tablename__ = 'author'

	#Mapeo de columnas y atributos
	id = Column(Integer, Sequence('autor_id_seq'), primary_key=True)
	firstname = Column(String)
	lastname = Column(String)

	def __repr__(self):
		return "{} {}".format(self.firstname, self.lastname)

#Conexion con la base de datos
engine = create_engine('sqlite:///:memory:')

#Crea todas las tablas que no han sido creadas
Base.metadata.create_all(engine)

#Clase sesion para poder crear sesiones a la base dada
Session = sessionmaker(bind = engine)
sesion = Session()

sesion.add_all([
	Author(firstname = 'firstname1', lastname = 'lastname1'),
	Author(firstname = 'firstname2', lastname = 'lastname2'),
	Author(firstname = 'firstname3', lastname = 'lastname3')])

print(sesion.query(Author).filter(Author.firstname.like('firstname%')).count())