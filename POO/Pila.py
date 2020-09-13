class EmptySatck(Exception):
	pass

class Pila:
	def __init__(self):
		self.stack = []
		self.tope = len(self.stack)

	def lenS(self):
		return self.tope

	def is_empty(self):
		if not self.stack:
			return True
		else:
			return False

	def top(self):
		if self.is_empty():
			raise EmptySatck("La pila está vacía")
		else:
			return self.stack[self.tope - 1]

	def pushS(self, elemento):
		self.stack.append(elemento)
		self.tope = self.tope + 1

	def popS(self):
		if self.is_empty():
			raise EmptySatck("La pila está vacía")
		else:
			self.tope = self.tope - 1
			return self.stack.pop()

p = Pila()