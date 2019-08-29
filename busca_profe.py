import requests
import json
import sys
output_file = open("materias_output.txt", "a+")
def get_typology():
    SIA_URL = "https://siabog.unal.edu.co/buscador/JSON-RPC"
    for cod_program in ['2544', '2545']:
        try:
            params = {
                'method':'buscador.obtenerAsignaturas',
                'params':['', 'PRE', 'C', 'PRE', cod_program, '', 1, 100]
            }
            response = json.loads(requests.post(SIA_URL, json=params).text)
            array_subjects = response['result']['asignaturas']['list']
            for subject in array_subjects:
                params = {
                    'method':'buscador.obtenerGruposAsignaturas',
                    'params':[subject['codigo'], '0']
                }
                response = json.loads(requests.post(SIA_URL, json=params).text)
                array_groups = response['result']['list']
                for group in array_groups:
                    if group['nombredocente'] == '  ':
                        output_file.write('[NO DISPONIBLE]' + ', ' + subject['nombre'] + '\n')
                    else:
                        output_file.write(group['nombredocente'] + ', ' + subject['nombre'] + '\n')
                    output_file.flush()
        except Exception:
            print(Exception)
get_typology()
output_file.close()