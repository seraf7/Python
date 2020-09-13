import csv

a_list = ['Pedro', 'Florencia', 'Matías', 'Jorge', 'María', 'Inés']

with open('/home/seraf/Documentos/Cursos/Python/csv_test.csv', 'w') as f:
	lector = csv.writer(f)
	lector.writerow(a_list)