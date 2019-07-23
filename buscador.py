import requests
import json
import multiprocessing
input_file = open("assign_input.txt", "r")
output_file = open("materias_output.txt", "a+")
lines = input_file.readlines()
SIA_URL = "https://siabog.unal.edu.co/buscador/JSON-RPC"
trheads = multiprocessing.cpu_count()
data_source = []
for i in range(trheads):
	data_source.append([])
count = 0
for line in lines:
	data_source[count % 8].append(line)
	count = count + 1
params = {
	'method':'buscador.obtenerAsignaturas',
	'params':['2015204', 'PRE', '', 'PRE', '', '', 1, 10]
}
r = requests.post(SIA_URL, json=params)
output_file.write(line + " " + json.loads(r.text)['result']['asignaturas']['list'][0]['tipologia'])
output_file.flush()