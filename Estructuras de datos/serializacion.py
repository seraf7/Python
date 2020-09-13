import json

#Serializacion en un archivo
with open('/home/seraf/Documentos/Cursos/Python/json_test.txt', 'w') as a_file:
	json.dump([1, 2, 3, 4, 5], a_file)

with open('/home/seraf/Documentos/Cursos/Python/json_test.txt', 'r') as a_file:
	a_list = json.load(a_file)
	print(type(a_list))
	print(a_list)