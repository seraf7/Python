from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Time
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Table, Text

from datetime import datetime

#Clase base declarativa
Base = declarative_base()

#Definicion de la clase Alumno
class Alumno(Base):
	#Asociacion a una tabla de la BD
	__tablename__ = 'alumno'

	#Mapeo de atributos y campos de la tabla
	idAl = Column(Integer, Sequence('alumno_id_seq'), primary_key=True)
	nombreAl = Column(String)
	apellidoAl = Column(String)
	#Clave foranea del curso inscrito
	curso_id = Column(Integer, ForeignKey('curso.idCur'))

	#Relacion con la tabla curso
	curso = relationship('Curso', back_populates='alumnos')

	def __repr__(self):
		return "{} {} {}".format(self.idAl, self.nombreAl, self.apellidoAl)

#Definicion de la clase Curso
class Curso(Base):
	#Asociacion a una tabla de la BD
	__tablename__ = 'curso'

	#Mapeo de atributos y campos de la tabla
	idCur = Column(Integer, Sequence('curso_id_seq'), primary_key=True)
	nombreCur = Column(String)

	#Relacion con la tabla alumno
	alumnos = relationship('Alumno', order_by='Alumno.idAl', back_populates='curso')

	#Relacion con la tabla profesor
	profesores = relationship('Profesor', secondary='horario', back_populates='cursos')

	def __repr__(self):
		return "{} {}".format(self.idCur, self.nombreCur)

#Definicion de la clase Horario
class Horario(Base):
	#Asociacion a una tabla de la BD
	__tablename__ = 'horario'

	curso_id = Column(Integer, ForeignKey('curso.idCur'), primary_key=True)
	profesor_id = Column(Integer, ForeignKey('profesor.idProf'), primary_key=True)
	dia = Column(String)
	inicio = Column(Time)
	fin = Column(Time)

	def __repr__(self):
		return "{} {} {} {} {}".format(self.curso_id, self.profesor_id,self.dia, self.inicio, self.fin)

#Definicion de la clase Profesor
class Profesor(Base):
	#Asociacion a una tabla de la BD
	__tablename__ = 'profesor'

	#Mapeo de atributos y campos de la tabla
	idProf = Column(Integer, Sequence('profesor_id_seq'), primary_key=True)
	nombreProf = Column(String)
	apellidoProf = Column(String)

	#Relacion con la tabla curso
	cursos = relationship('Curso', secondary='horario', back_populates='profesores')

	def __repr__(self):
		return "{} {} {}".format(self.idProf, self.nombreProf, self.apellidoProf)

#Conexion con la base de datos
engine = create_engine('sqlite:///:memory:')

#Creacion de las tablas
Base.metadata.create_all(engine)

#Creacion de una sesion
Session = sessionmaker(bind=engine)
sesion = Session()

#############Insercion de datos##################

#Creacion de alumnos de alumnos
alumnos = [
	Alumno(nombreAl='Lizbeth', apellidoAl='Alpizar'),
	Alumno(nombreAl='Serafin', apellidoAl='Castillo'),
	Alumno(nombreAl='Mario', apellidoAl='Suarez'),
	Alumno(nombreAl='Sarahi', apellidoAl='Lopez'),
	Alumno(nombreAl='Perla', apellidoAl='Gutierrez'),
	Alumno(nombreAl='Aldair', apellidoAl='Dorantes')]

sesion.add_all(alumnos)

#Creacion de cursos
cursos = [
	Curso(nombreCur='Matematicas'),
	Curso(nombreCur='Ciencias'),
	Curso(nombreCur='Español')]

sesion.add_all(cursos)

#Inscripcion de alumnos en cursos
cursos[0].alumnos.append(alumnos[0])
cursos[0].alumnos.append(alumnos[5])

cursos[1].alumnos.append(alumnos[2])
cursos[1].alumnos.append(alumnos[1])

cursos[2].alumnos.append(alumnos[4])
cursos[2].alumnos.append(alumnos[3])

#Creacion de profesores
profes = [
	Profesor(nombreProf='Ruben', apellidoProf='Anaya'),
	Profesor(nombreProf='Edagar', apellidoProf='Tista'),
	Profesor(nombreProf='Pedro', apellidoProf='Alcantara')]

#Asociacion de profesores y cursos
cursos[0].profesores.append(profes[1])
cursos[0].profesores.append(profes[0])

cursos[1].profesores.append(profes[2])

cursos[2].profesores.append(profes[0])
cursos[2].profesores.append(profes[1])
cursos[2].profesores.append(profes[2])

sesion.add_all(cursos)

#Actualizar horarios asociados a un curso y un profesor
def actualizarHorario(curso, profesor, dia, inicio, fin):
	global sesion
	h = sesion.query(Horario).filter(Horario.profesor_id==profesor).filter(Horario.curso_id==curso).first()
	if h:
		h.dia = dia
		#Realiza la conversion de una cadena a objeto time
		h.inicio = datetime.strptime(inicio, '%H:%M').time()
		h.fin = datetime.strptime(fin, '%H:%M').time()
		sesion.commit()
	else:
		print("Registro no encontrado")

actualizarHorario(3, 2, 'Martes', '07:00', '08:30')
actualizarHorario(1, 1, 'Lunes', '07:00', '09:00')
actualizarHorario(1, 2, 'Martes', '09:00', '11:00')
actualizarHorario(2, 3, 'Jueves', '09:40', '11:15')
actualizarHorario(3, 1, 'Viernes', '14:40', '16:15')
actualizarHorario(3, 3, 'Sabado', '09:40', '11:15')

print("\nTabla de horario")
for horario in sesion.query(Horario):
	print("{} {} {} {} {}".format(horario.curso_id, horario.profesor_id, horario.dia, horario.inicio, horario.fin))

#Despliegue de alumnos inscritos
print("\nMatricula de alumnos")
for alumno in sesion.query(Alumno):
	print(alumno)

#Despliegue de alumnos por curso
def alumnosInscritos(idCur):
	c = sesion.query(Curso).filter(Curso.idCur==idCur).first()
	if c:
		print("\nAlumnos inscritos en {}".format(c.nombreCur))
		for alumno in sesion.query(Alumno).join(Curso).filter(Curso.idCur==idCur).all():
			print(alumno)
	else:
		print("\nCurso no encontrado")

alumnosInscritos(1)
alumnosInscritos(2)
alumnosInscritos(3)

#Despliegue de horario del profesor
def horarioProfesor(idProf):
	global sesion
	prof = sesion.query(Profesor).filter(Profesor.idProf==idProf).first()
	if prof:
		print("\nProfesor: {} {}".format(prof.nombreProf, prof.apellidoProf))
		for curso, horario in sesion.query(Curso, Horario).filter(Curso.idCur==Horario.curso_id).filter(Horario.profesor_id==idProf).all():
			print("{} {} {} {}".format(curso.nombreCur, horario.dia, horario.inicio, horario.fin))
	else:
		print("\nProfesor no encontrado")

horarioProfesor(1)
horarioProfesor(2)
horarioProfesor(3)

#Despliegue de horario del curso
def horarioCurso(idCur):
	global sesion
	curso = sesion.query(Curso).filter(Curso.idCur==idCur).first()
	if curso:
		print("\nCurso {}: {}".format(curso.idCur, curso.nombreCur))
		for profesor, horario in sesion.query(Profesor, Horario).filter(Profesor.idProf==Horario.profesor_id).filter(Horario.curso_id==idCur).all():
			print("{} {} {} {} {}".format(profesor.nombreProf, profesor.apellidoProf, horario.dia, horario.inicio, horario.fin))
	else:
		print("\nCurso no encontrado")

horarioCurso(1)
horarioCurso(2)
horarioCurso(3)