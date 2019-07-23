import requests
import json
import sys
from multiprocessing import Process, Value
output_file = open("materias_output.txt", "a+")
SIA_URL = "https://siabog.unal.edu.co/buscador/JSON-RPC"
def get_typology(subjects, actual_iteration, length):
	for subj in subjects:
		try:
			params = {
				'method':'buscador.obtenerAsignaturas',
				'params':[subj, 'PRE', '', 'PRE', '', '', 1, 10]
			}
			response = json.loads(requests.post(SIA_URL, json=params).text)
			output_file.write(response['result']['asignaturas']['list'][0]['id_asignatura'] + ', ')
			output_file.write(response['result']['asignaturas']['list'][0]['tipologia'] + '\n')
			output_file.flush()
		except:
			pass
		actual_iteration.value += 1
		print(actual_iteration.value, '/', length)
def main(threads):
	threads = int(threads)
	input_file = open("assign_input.txt", "r")
	subjects = []
	[subjects.append([]) for i in range(threads)]
	it = 0
	for cod_subject in input_file.readlines():
		subjects[it % threads].append(cod_subject.replace('\n',''))
		it += 1
	input_file.close()
	counter = Value('i', 0)
	th = []
	for i in range(threads):
		tread = Process(target=get_typology, args=(subjects[i], counter, it))
		th.append(tread)
		tread.start()
	[tread.join() for t in th]
if __name__ == '__main__':
	main(16)
output_file.close()