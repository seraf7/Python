#Recibe como parametro una funcion
def smart_division(div_fun):
	def div(a, b):
		if b == 0:
			print("No se puede dividir entre cero")
			return
		#Retorna el resultado de evaluar la funcion parametro
		return div_fun(a, b)
	return div

@smart_division
def division(a, b):
	return a / b

a = division(4, 2)
print(a)