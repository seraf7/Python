import random

turnos = 0

def imprimir_tablero(tablero):
	for x in range(len(tablero)):
		s = "|{}|{}|{}|\n".format(tablero[x][0], tablero[x][1], tablero[x][2])
		print(s)
	return

def validar_casilla(fun_ocupado):
	def tiro(c, jugador, tablero):
		if int(c[0]) > 2 or int(c[1]) > 2:
			print("Casilla no valida")
			return
		return fun_ocupado(c, jugador, tablero)
	return tiro

def validar_ocupacion(fun_tiro):
	def tirar(c, jugador, tablero):
		if tablero[int(c[0])][int(c[1])] != '_':
			if(type(c[0]) != int):
				#Impresion solo cuando es turno del usuario
				print("Casilla ocupada")
			return
		return fun_tiro(c, jugador, tablero)
	return tirar

@validar_casilla
@validar_ocupacion
def jugar(c, jugador, tablero):
	tablero[int(c[0])][int(c[1])] = jugador
	return True

def computadora():
	b = []
	b.append(random.randint(0,2))
	b.append(random.randint(0,2))
	return b

def turnoCPU(cpu, tablero):
	global turnos
	print("Turno de {}".format(cpu))
	j = computadora()
	while(jugar(j, cpu, tablero) != True):
		j = computadora()
	turnos = turnos + 1
	imprimir_tablero(tablero)

def turnoJugador(usuario, tablero):
	global turnos
	j = input("Turno de {}. Ingresa la casilla en que deseas tirar: \t".format(usuario))
	while(jugar(j.split(','), usuario, tablero) != True):
		print("Vuelve a intentar")
		j = input("Turno de {}. Ingresa la casilla en que deseas tirar: \t".format(usuario))
	turnos = turnos + 1
	imprimir_tablero(tablero)

def ganar(tablero):
	ganador = ''
	#Jugadas ganadoras diagonales
	if(tablero[0][0] == tablero[1][1] == tablero[2][2] != '_'):
		return tablero[0][0]
	elif(tablero[0][2] == tablero[1][1] == tablero[2][0] != '_'):
		return tablero[1][1]
	else:
		for i in range(len(tablero)):
			#Jugadas horizontales
			if(tablero[i][0] == tablero[i][1] == tablero[i][2] != '_'):
				ganador = tablero[i][0]
				break
			#Jugadas verticales
			elif(tablero[0][i] == tablero[1][i] == tablero[2][i] != '_'):
				ganador = tablero[0][i]
				break
			#Sin ganador
			else:
				ganador = ''
		return ganador

def gato():
	global turnos
	tablero = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
	ganador = ''

	usuario = ''
	cpu = ''
	while usuario != 'X' and usuario != 'O':
		usuario = input("Selecciona tu ficha. X, O:\t")

	if usuario == 'X':
		cpu = 'O'
	else:
		cpu = 'X'

	print("Seleccionaste {}. Las X inician\n".format(usuario))
	imprimir_tablero(tablero)

	if(usuario == 'X'):
		while turnos < 9:
			turnoJugador(usuario, tablero)
			ganador = ganar(tablero)
			if ganador == 'X' or turnos == 9:
				break
			turnoCPU(cpu, tablero)
			ganador = ganar(tablero)
			if ganador == 'O' or turnos == 9:
				break
	else:
		while turnos < 9:
			turnoCPU(cpu, tablero)
			ganador = ganar(tablero)
			if ganador == 'X' or turnos == 9:
				break
			turnoJugador(usuario, tablero)
			ganador = ganar(tablero)
			if ganador == 'O' or turnos == 9:
				break

	if ganador == '':
		print("El juego terminó en empate")
	else:
		print("Fin del juego. El ganador es {}".format(ganador))

gato()