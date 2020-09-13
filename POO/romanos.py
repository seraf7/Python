import unittest
import re

class WrongSimbols(Exception):
	pass

def validar(numero):
	#Descartar numeros no romanos
	if re.search("[a-z0-9A-BE-HJ-KN-WY-Z]", numero):
		return False
	return True

def invertir(numero):
	return numero[::-1]

def uno(numero, indice):
	suma = 0
	contador = 0
	while indice < len(numero):
		if numero[indice] != "I":
			break
		if numero[indice] == "I" and contador < 3:
			suma += 1
			contador += 1
		else:
			suma = False
			break
		indice += 1
	return suma

def cinco(numero, indice):
	suma = 0
	contador = 0
	while indice < len(numero):
		if numero[indice] != "V" and numero[indice] != "I":
			break
		if numero[indice] == "V" and contador == 0:
			suma += 5
		elif numero[indice] == "I" and contador == 1:
			suma -= 1
		else:
			suma = False
			break
		indice += 1
		contador += 1
	return suma
	

def romanos(numero):
	if not validar(numero):
		return False

	nInv = invertir(numero)

class RomanosTest(unittest.TestCase):
	def test_simbolosRechazados(self):
		resultado = validar("MCT")
		self.assertFalse(resultado)

	def test_simbolosAceptados(self):
		resultado = validar("MII")
		self.assertTrue(resultado)

	def test_invertirCadena(self):
		resultado = invertir("MDDCI")
		self.assertEqual("ICDDM", resultado)

	def test_validarUno(self):
		resultado = uno("I", 0)
		self.assertEqual(1, resultado)

	def test_unoExcesivos(self):
		resultado = uno("IIII", 0)
		self.assertFalse(resultado)

	def test_validarCinco(self):
		resultado = cinco("V", 0)
		self.assertEqual(5, resultado)

	def test_restarUno(self):
		n = invertir("IV")
		resultado = cinco(n, 0)
		self.assertEqual(4, resultado)

	def test_cincoExcesivos(self):
		resultado = cinco("VV", 0)
		self.assertFalse(resultado)

#Para correr las pruebas unitarias
if __name__ == '__main__':
	unittest.main()