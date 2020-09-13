class EmptyStack(Exception):
	pass

#Definicion de la clase pila
class Pila:
	def __init__(self):
		#Guarda el elemento que se encuentra en el tope de la pila
		self.head = PilaBase()

	def top(self):
		return self.head

	def push(self, value):
		self.head = self.head.push(value)

	def pop(self):
		oldHead = self.head
		self.head = self.head.pop()
		return oldHead

	def len(self):
		return self.head.len()

	def is_empty(self):
		return self.head.is_empty()


#Definicion de la base de la pila
class PilaBase():
	def push(self, value):
		return PilaItem(padre = self, valor = value)

	def pop(self):
		#Debido a que la pila está vacía, se levanta excepción
		raise EmptyStack("Pila Vacía")

	def len(self):
		return 0

	def is_empty(self):
		return True

	def __repr__(self):
		return "Base de la Pila"

#Definicion de un elemento de la pila
class PilaItem:
	def __init__(self, padre, valor):
		self.padre = padre
		self.valor = valor

	def push(self, value):
		return PilaItem(padre = self, valor = value)

	def pop(self):
		return self.padre

	def len(self):
		#Recursion sobre elementos padre
		return self.padre.len() + 1

	def is_empty(self):
		return False

	def __repr__(self):
		return str(self.valor)


stack = Pila()