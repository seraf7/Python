class Divisa:
	#Constructor de la clase
	def __init__(self, nombre, simbolo, factor):
		self.nombre = nombre
		self.simbolo = simbolo
		self.factor = factor

	#Metodo magico para desplegar en consola
	def __repr__(self):
		return "{} {}".format(self.nombre, self.simbolo)

	#Metodo para convertir a valor base
	def convBase(self, cantidad):
		return self.factor * cantidad

	#Metodo para convertir a valor actual
	def convActual(self, cantidad):
		return cantidad / self.factor


class Dinero:
	#Constructor de la clase
	def __init__(self, divisa, cantidad):
		self.divisa = divisa
		self.cantidad = cantidad

	#Metodo magico para desplegar en consola
	def __repr__(self):
		return "{} {}".format(self.divisa.simbolo, self.cantidad)

	def convertirBase(self):
		return self.divisa.convBase(self.cantidad)

	def convertirActual(self):
		return self.divisa.convActual(self.cantidad)

	#Metodo magico para realizar suma
	def __add__(self, monto):
		d = self.convertirBase() + monto.convertirBase()
		d = self.divisa.convActual(d)
		return Dinero(self.divisa, d)

	#Metodo magico para realizar resta
	def __sub__(self, monto):
		d = self.convertirBase() - monto.convertirBase()
		d = self.divisa.convActual(d)
		return Dinero(self.divisa, d)

	#Metodo magico para realizar multiplicacion escalar
	def __mul__(self, escalar):
		return Dinero(self.divisa, self.cantidad * escalar)

	#Metodo magico para realizar division escalar
	def __truediv__(self, escalar):
		return Dinero(self.divisa, self.cantidad / escalar)


pesos = Divisa("Peso MXN", "$", 1.0/21.0)

euros = Divisa("Euro", "€", 1.18)

peso3 = Dinero(pesos, 3.0)

euro1 = Dinero(euros, 1.0)