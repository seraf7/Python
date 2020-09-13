import unittest

class Producto:
	def __init__(self, codigo, nombre, precio, descuento):
		self.codigo = codigo
		self.nombre = nombre
		self.precio = precio
		self.descuento = descuento

class Inventario:
	leche = Producto("AGF34", "Leche", 18, 0)
	pan = Producto("HDI44", "Pan", 5, 0)
	sopa = Producto("LDO09", "Sopa", 20, 0.15)

	almacen = [leche, pan, sopa]

	def buscar(self, ID):
		p = False
		for i in range(len(self.almacen)):
			if self.almacen[i].codigo == ID:
				p = self.almacen[i]
				break
		return p

class Escanner:
	inventario = Inventario()
	
	def scan(self, codigo):
		return self.inventario.buscar(codigo)

class Caja:
	def __init__(self):
		self.escanner = Escanner()
		self.listaCompras = []
		self.subtotal = 0
		self.descuento = 0

	def comprar(self, codigo):
		p = self.escanner.scan(codigo)
		if p:
			self.listaCompras.append(p)
			self.calcularSubtotal(p.precio)
		return self.listaCompras

	def calcularSubtotal(self, precio):
		self.subtotal += precio
		print("Subtotal\t${:0.2f}".format(self.subtotal))
		return self.subtotal

	def calcularTotal(self):
		return self.subtotal - self.descuento

	def aplicarDescuento(self):
		for i in range(len(self.listaCompras)):
			self.descuento += self.listaCompras[i].precio * self.listaCompras[i].descuento
		return self.descuento

	def pagar(self, dinero):
		total = self.calcularTotal()
		if dinero > total:
			return dinero - total
		else:
			return "Monto insuficiente"

	def imprimirLista():
		for i in range(len(self.listaCompras)):
			print("{:10} ${:0.2f}".format(self.listaCompras[i].nombre, self.listaCompras[i].precio))

	def transaccion(self):
		while True:
			try:
				p = input("Ingresa código de producto. Presiona CTRL + C, para finalizar")
				self.comprar(p)
				self.imprimirLista()
			except KeyboardInterrupt:
				return "Finalizar Compra"
				break
		self.aplicarDescuento()
		#dinero = int(input("Ingresa monto de pago"))
		#self.pagar()

class CajaTest(unittest.TestCase):
	def setUp(self):
		self.caja = Caja()
		self.escanner = Escanner()
		self.caja.comprar("AGF34")
		self.caja.comprar("LDO09")

	def test_escanearProductoExistente(self):
		producto = self.escanner.scan("AGF34")
		self.assertEqual("Leche", producto.nombre)

	def test_productoNoEncontrado(self):
		producto = self.escanner.scan("ATF34")
		self.assertFalse(producto)

	def test_listaCompras(self):
		l = []
		for i in range(len(self.caja.listaCompras)):
			l.append(self.caja.listaCompras[i].nombre)
		self.assertEqual(["Leche", "Sopa"], l)

	def test_calcularSubtotal(self):
		#Ya hay productos en la lista, se verifica el subtotal
		#al llamar la funcion
		subtotal = self.caja.calcularSubtotal(0)
		self.assertEqual(38, subtotal)

	def test_calcularDescuento(self):
		descuento = self.caja.aplicarDescuento()
		self.assertEqual(3, descuento)

	def test_calcularTotal(self):
		self.caja.aplicarDescuento()
		total = self.caja.calcularTotal()
		self.assertEqual(35, total)

	def test_pagarSuficiente(self):
		self.caja.aplicarDescuento()
		cambio = self.caja.pagar(200)
		self.assertEqual(165, cambio)

	def test_pagarInsuficiente(self):
		self.caja.aplicarDescuento()
		cambio = self.caja.pagar(20)
		self.assertEqual("Monto insuficiente", cambio)

	#Verificamos que la interrupcion por teclado finalice la compra
	def test_finalizarCompra(self):
		self.assertEqual("Finalizar Compra", self.caja.transaccion())


#Sentencia para ejecutar pruebas unitarias
if __name__ == '__main__':
	unittest.main()