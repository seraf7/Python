for x in range(1, 11):
	print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
	#end indica el tipo de impresión al final de la linea
	print(repr(x*x*x).rjust(4))

print()
print()

for x in range(1, 11):
	print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))