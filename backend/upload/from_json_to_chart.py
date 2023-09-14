import json
import random


coll_d = {'arts': 30, 'fnames': 16, 'cass': 8, 'decrs': 7, 'idprocs': 7, 'pers': 22, 'locs': 15}
fname_d = {'Appello': 1, 'Altro': 9, 'Citazione': 1, 'Decreto': 1, 'Informativa': 1, 'Istanza': 1, 'Memoria': 2}
art_d = {'C.P.': 11, 'C.P.P.': 14, 'TESTO UNICO': 2, 'C.C.': 3}

def generate_color():
    color = "%06x" % random.randint(0, 0xFFFFFF)
    return color.upper()

def create_data(label, coll):
    num_of_fields = len(coll)
    data_coll = dict()
    data_coll['labels'] = [k for k in coll.keys()]
    data_coll['datasets'] = list()
    datasets = dict()
    datasets['label'] = label
    datasets['data'] = [v for v in coll.values()] 
    datasets['backgroundColor'] = ['#' + generate_color() for i in range(num_of_fields)]
    datasets['borderColor'] = datasets['backgroundColor']
    datasets['borderWidth'] = [1 for i in range(num_of_fields)]
    data_coll['datasets'].append(datasets)
    return data_coll

def file_writer():

	data_coll = create_data('Collections', coll_d)
	data_fname = create_data('Tipo Documenti', fname_d)
	data_art = create_data('Tipo Articoli', art_d)

	with open('coll_d.json', 'w') as fp:
	    json.dump(data_coll, fp)

	with open('fname_d.json', 'w') as fp:
	    json.dump(data_fname, fp)

	with open('art_d.json', 'w') as fp:
	    json.dump(data_art, fp)