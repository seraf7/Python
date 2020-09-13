import unittest

class Romano:
	enteros = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
	simbolos = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

	def entero_Romano(self, n):
		numero = ""
		resto = n

		for i in range(len(self.enteros)):
			numero, resto = self.valoresRepresentativos(resto,
				self.enteros[i], self.simbolos[i], numero)

		return numero

	def valoresRepresentativos(self, n, numero, romano, cadena):
		resto = n
		while resto >= numero:
			cadena += romano
			resto -= numero
		return cadena, resto


class RomanosTest(unittest.TestCase):
	def setUp(self):
		self.numeroRomano = Romano()

	def test_uno(self):
		romano = self.numeroRomano.entero_Romano(1)
		self.assertEqual("I", romano)

	def test_dos(self):
		romano = self.numeroRomano.entero_Romano(2)
		self.assertEqual("II", romano)

	def test_tres(self):
		romano = self.numeroRomano.entero_Romano(3)
		self.assertEqual("III", romano)

	def test_cuatro(self):
		romano = self.numeroRomano.entero_Romano(4)
		self.assertEqual("IV", romano)

	def test_cinco(self):
		romano = self.numeroRomano.entero_Romano(5)
		self.assertEqual("V", romano)

	def test_seis(self):
		romano = self.numeroRomano.entero_Romano(6)
		self.assertEqual("VI", romano)

	def test_nueve(self):
		romano = self.numeroRomano.entero_Romano(9)
		self.assertEqual("IX", romano)

	def test_diez(self):
		romano = self.numeroRomano.entero_Romano(10)
		self.assertEqual("X", romano)

	def test_cuarenta(self):
		romano = self.numeroRomano.entero_Romano(40)
		self.assertEqual("XL", romano)

	def test_cincuenta(self):
		romano = self.numeroRomano.entero_Romano(50)
		self.assertEqual("L", romano)

	def test_noventa(self):
		romano = self.numeroRomano.entero_Romano(90)
		self.assertEqual("XC", romano)

	def test_cien(self):
		romano = self.numeroRomano.entero_Romano(100)
		self.assertEqual("C", romano)

	def test_cuatrocientos(self):
		romano = self.numeroRomano.entero_Romano(400)
		self.assertEqual("CD", romano)

	def test_quinientos(self):
		romano = self.numeroRomano.entero_Romano(500)
		self.assertEqual("D", romano)

	def test_novecientos(self):
		romano = self.numeroRomano.entero_Romano(900)
		self.assertEqual("CM", romano)

	def test_mil(self):
		romano = self.numeroRomano.entero_Romano(1000)
		self.assertEqual("M", romano)

#Para correr las pruebas unitarias
if __name__ == '__main__':
	unittest.main()