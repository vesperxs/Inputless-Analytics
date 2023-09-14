import json
import re
from typing import *
import itertools

def id_to_node(node_id, data):
    for k,v in data.items():
        for node in v['nodes']:
            if node['id'] == node_id:
                return node


def normalize_weight(weight):
    return 100

def sub_data_creation(struct, roots_ids):
    struct2 = dict()
    root2 = []
    for k,v in struct.items():
        for edge in v['edges']:
            struct2.setdefault(edge['target'], {})
            struct2[edge['target']].setdefault('nodes', [])
            struct2[edge['target']].setdefault('edges', [])
            app_node1 = id_to_node(edge['source'], struct)
            if app_node1 and app_node1 not in struct2[edge['target']]['nodes']:
                struct2[edge['target']]['nodes'].append(app_node1)
                struct2[edge['target']]['edges'].append(edge)

            struct2.setdefault(edge['source'], {})
            struct2[edge['source']].setdefault('nodes', [])
            struct2[edge['source']].setdefault('edges', [])
            app_node2 = id_to_node(edge['target'], struct)
            if app_node2 and app_node2 not in struct2[edge['source']]['nodes'] :
                struct2[edge['source']]['nodes'].append(app_node2)
                struct2[edge['source']]['edges'].append(edge)
    return struct2


def jsonize_data(res_list):
    ids_dict           = dict()
    duplicates_list    = list()
    struct             = dict()
    roots              = dict()
    roots_nodes        = list()
    roots_nodes        = list()
    roots_ids          = list()
    for el in range(len(res_list)): #cicla su ogni risultato della query
        source_id = res_list[el]['element']['_id'] #il risultato corrente della query di livello 0
        struct.setdefault(source_id, {}) #crea un dizionario per ogni source_id che sara' popolato con i propri nodi e edges
        struct[source_id].setdefault('nodes', [])
        struct[source_id].setdefault('edges', [])

        res = res_list[el]
        r_type = re.search('[A-Z]+', res['element']['_id'] ).group()

        if r_type == 'FILENAME':
            root_el = create_fname_elem(res['element'], res['elem_weight'], is_root = True)

        elif r_type in ['PERSON', 'LOCATION', 'ORGANIZATION']:
            root_el = create_simple_elem(res['element'], res['elem_weight'], is_root = True)

        elif r_type == 'IDPROC':
            root_el = create_idp_elem(res['element'], res['elem_weight'], is_root = True)

        elif r_type == 'ARTICOLI':
            root_el, _ = create_art_elem(res['element'], res['elem_weight'], is_root = True)

        elif r_type == 'DECRETI':
            root_el = create_decr_elem(res['element'], res['elem_weight'], is_root = True)

        elif r_type == 'CASSAZIONE':
            root_el = create_cass_elem(res['element'], res['elem_weight'], is_root = True)

        roots_nodes.append(root_el)
        roots_ids.append(res['element']['_id'])
        ids_dict[res['element']['_id']] = set()

        for v in res['Vertices']:
            #check duplicate
            if v['node']['_id'] not in duplicates_list:
                ids_dict[res['element']['_id']].add(v['node']['_id'])

            if 'FILENAME' in str(v['node']['_id']):
                attr_d = create_fname_elem(v['node'], v['weight'], is_root=False )
                struct[source_id]['nodes'].append(attr_d)

            if 'IDPROC' in str(v['node']['_id']):
                attr_d = create_idp_elem(v['node'], v['weight'], is_root=False )
                if attr_d['id'] not in duplicates_list:
                    duplicates_list.append(attr_d['id'])
                    struct[source_id]['nodes'].append(attr_d)

            if 'ARTICOLI' in str(v['node']['_id']):
                attr_d, cod_type = create_art_elem(v['node'], v['weight'], is_root=False )
                if (attr_d['id'] not in duplicates_list) and cod_type:
                    duplicates_list.append(attr_d['id'])
                    struct[source_id]['nodes'].append(attr_d)

            if 'DECRETI' in str(v['node']['_id']):
                attr_d = create_decr_elem(v['node'], v['weight'], is_root=False )
                if attr_d['id'] not in duplicates_list:
                    duplicates_list.append(attr_d['id'])
                    struct[source_id]['nodes'].append(attr_d)

            if 'CASSAZIONE' in str(v['node']['_id']):
                attr_d = create_cass_elem(v['node'], v['weight'], is_root=False )
                if attr_d['id'] not in duplicates_list:
                    duplicates_list.append(attr_d['id'])
                    struct[source_id]['nodes'].append(attr_d)

            if 'LOCATION' in str(v['node']['_id']):
                attr_d = create_simple_elem(v['node'], v['weight'], is_root=False )
                if attr_d['id'] not in duplicates_list:
                    duplicates_list.append(attr_d['id'])
                    struct[source_id]['nodes'].append(attr_d)

            if 'PERSON' in str(v['node']['_id']):
                attr_d = create_simple_elem(v['node'], v['weight'], is_root=False )
                if attr_d['id'] not in duplicates_list:
                    duplicates_list.append(attr_d['id'])
                    struct[source_id]['nodes'].append(attr_d)

            if 'ORGANIZATION' in str(v['node']['_id']):
                attr_d = create_simple_elem(v['node'], v['weight'], is_root=False )
                if attr_d['id'] not in duplicates_list:
                    duplicates_list.append(attr_d['id'])
                    struct[source_id]['nodes'].append(attr_d)

        for e in res['Edges']:
            edge = {
                'source' : e['_from'],
                'target' : e['_to'],
                'edge_type' : 'doc_attr_edge'
            }
            struct[source_id]['edges'].append(edge)

    #creazione di sub_data
    for k,v in struct.items():
        struct2 = dict()
        for edge in v['edges']:
            if edge['source'] not in roots_ids:
                struct2.setdefault(edge['target'], {})
                struct2[edge['target']].setdefault('nodes', [])
                struct2[edge['target']].setdefault('edges', [])
                app_node1 = id_to_node(edge['source'], struct)
                if app_node1 and app_node1 not in struct2[edge['target']]['nodes']:
                    struct2[edge['target']]['nodes'].append(app_node1)
                    struct2[edge['target']]['edges'].append(edge)
            else:
                struct2.setdefault(edge['source'], {})
                struct2[edge['source']].setdefault('nodes', [])
                struct2[edge['source']].setdefault('edges', [])
                app_node2 = id_to_node(edge['target'], struct)
                if app_node2 and app_node2 not in struct2[edge['source']]['nodes'] :
                    struct2[edge['source']]['nodes'].append(app_node2)
                    struct2[edge['source']]['edges'].append(edge)

    struct2 = sub_data_creation(struct, roots_ids)

    struct2['root'] = dict()
    struct2['root']['nodes'] = roots_nodes
    struct2['root']['edges'] = []

    return struct2


def id_to_label(res_list, id):
    for el in range(len(res_list)):
        for v in res_list[el]['Vertices']:
            if v['node']['_id'] == id:
                if 'ARTICOLI' in id:
                    elem, cod_type = create_art_elem(v['node'],0,False)
                    if cod_type:
                        label = re.sub('\n',' ',elem['label'])
                    else:
                        label = None
                elif 'IDPROC' in id:
                    elem = create_idp_elem(v['node'],0,False)
                    label = re.sub('\n',' ',elem['label'])
                elif 'CASSAZIONE' in id:
                    elem = create_cass_elem(v['node'],0,False)
                    label = re.sub('\n',' ',elem['label'])
                elif 'DECRETI' in id:
                    elem = create_decr_elem(v['node'],0,False)
                    label = re.sub('\n',' ',elem['label'])
                else:
                    label = v['node']['name']
                return label


def create_table(res_list):
    table_dict = dict()
    for el in range(len(res_list)): #cicla su ogni risultato della query
        if 'FILENAME' in (res_list[el]['element']['_id']):
            table_dict[res_list[el]['element']['name']] = dict()
        else:
            root_el = res_list[el]['element']
        for e in res_list[el]['Edges']:
            if res_list[el]['element']['_id'] in e['_from']:
                if 'ARTICOLI' in (e['_to']):
                    table_dict[res_list[el]['element']['name']].setdefault('ARTICOLI', set())
                    elem = id_to_label(res_list, e['_to'])
                    if elem:
                        table_dict[res_list[el]['element']['name']]['ARTICOLI'].add(elem)
                elif 'IDPROC' in (e['_to']):
                    table_dict[res_list[el]['element']['name']].setdefault('IDPROC', set())
                    elem = id_to_label(res_list, e['_to'])
                    table_dict[res_list[el]['element']['name']]['IDPROC'].add(elem)
                elif 'DECRETI' in (e['_to']):
                    table_dict[res_list[el]['element']['name']].setdefault('DECRETI', set())
                    elem = id_to_label(res_list, e['_to'])
                    table_dict[res_list[el]['element']['name']]['DECRETI'].add(elem)
                elif 'CASSAZIONE' in (e['_to']):
                    table_dict[res_list[el]['element']['name']].setdefault('CASSAZIONE', set())
                    elem = id_to_label(res_list, e['_to'])
                    table_dict[res_list[el]['element']['name']]['CASSAZIONE'].add(elem)
                elif 'PERSON' in (e['_to']):
                    table_dict[res_list[el]['element']['name']].setdefault('PERSON', set())
                    elem = id_to_label(res_list, e['_to'])
                    table_dict[res_list[el]['element']['name']]['PERSON'].add(elem)
                elif 'LOCATION' in (e['_to']):
                    table_dict[res_list[el]['element']['name']].setdefault('LOCATION', set())
                    elem = id_to_label(res_list, e['_to'])
                    table_dict[res_list[el]['element']['name']]['LOCATION'].add(elem)

        for v in res_list[el]['Vertices']:
            if 'FILENAME' in v['node']['_id'] and (v['node']['name'] not in table_dict.keys()):
                table_dict[v['node']['name']] = dict()
                for e in res_list[el]['Edges']:
                    if v['node']['_id'] in e['_from']:
                        if 'ARTICOLI' in (e['_to']):
                            table_dict[v['node']['name']].setdefault('ARTICOLI', set())
                            elem = id_to_label(res_list, e['_to'])
                            if elem:
                                table_dict[v['node']['name']]['ARTICOLI'].add(elem)
                        elif 'IDPROC' in (e['_to']):
                            table_dict[v['node']['name']].setdefault('IDPROC', set())
                            elem = id_to_label(res_list, e['_to'])
                            table_dict[v['node']['name']]['IDPROC'].add(elem)
                        elif 'DECRETI' in (e['_to']):
                            table_dict[v['node']['name']].setdefault('DECRETI', set())
                            elem = id_to_label(res_list, e['_to'])
                            table_dict[v['node']['name']]['DECRETI'].add(elem)
                        elif 'CASSAZIONE' in (e['_to']):
                            table_dict[v['node']['name']].setdefault('CASSAZIONE', set())
                            elem = id_to_label(res_list, e['_to'])
                            table_dict[v['node']['name']]['CASSAZIONE'].add(elem)
                        elif 'PERSON' in (e['_to']):
                            table_dict[v['node']['name']].setdefault('PERSON', set())
                            elem = id_to_label(res_list, e['_to'])
                            table_dict[v['node']['name']]['PERSON'].add(elem)
                        elif 'LOCATION' in (e['_to']):
                            table_dict[v['node']['name']].setdefault('LOCATION', set())
                            elem = id_to_label(res_list, e['_to'])
                            table_dict[v['node']['name']]['LOCATION'].add(elem)
    #with open('table.json','w') as f:
    #    f.write(json.dumps(table_dict))
    #return table_dict
    return table_dict


# def create_table(struct):
#     roots = list()
#     nodes_dict = dict()
#     for root in struct['root']['nodes']:
#         roots.append(root['id'])
#     for item in struct:
#         if 'FILENAME' in item:
#             item_node = id_to_node(item, struct)
#             item_label = item_node['label'].replace('\n', ' ')
#             nodes_dict[item_label] = dict()
#             for elem in struct[item]['nodes']:
#                 label = elem['label'].replace('\n', ' ')
#                 is_root = 'True' if elem['id'] in roots else 'False'
#                 nodes_dict[item_label].setdefault(elem['type'], list())
#                 nodes_dict[item_label][elem['type']].append(label)
#     nodes_dict['roots']=roots

#     #with open('table.json','w') as f:
#     #    f.write(json.dumps(nodes_dict))
#     return nodes_dict



def create_simple_elem(elem_d, elem_weight, is_root):
    elem_type = re.search('[A-Z]+', elem_d['_id'] ).group()
    size = normalize_weight(elem_weight)
    struct_obj = {
        'id'       : elem_d['_id'],
        'label'    : (elem_d['name']).replace(" ", "\n"),
        'type'     : elem_type,
        'weight'   : elem_weight,
        'origSize' : size,
        'size'     : size,
        'isRoot'   : is_root
    }
    return struct_obj

def create_fname_elem(elem_d, elem_weight, is_root):
    size = normalize_weight(elem_weight)
    struct_obj = {
        'id'       : elem_d['_id'],
        'label'    : (elem_d['name']).replace(" ", "\n"),
        'category' : elem_d['type'],
        'type'     : 'FILENAME',
        'weight'   : elem_weight,
        'origSize' : size,
        'size'     : size,
        'isRoot'   : is_root
    }
    return struct_obj

def create_idp_elem(elem_d, elem_weight, is_root):
    type_   = elem_d['type']
    cod     = elem_d['code'] + '/' + elem_d['date']
    mod     = ' mod.' + elem_d['mod'] if elem_d['mod'] else ''
    size = normalize_weight(elem_weight)
    struct_obj = {
        'id'       : elem_d['_id'],
        'label'    : f"{type_}\n{cod}{mod}",
        'type'     : 'IDPROC',
        'weight'   : elem_weight,
        'origSize' : size,
        'size'     : size,
        'isRoot'   : is_root
    }
    return struct_obj

def create_art_elem(elem_d, elem_weight, is_root):
    cod      = elem_d['num']
    comma    = '\nco.'  + elem_d['comma'] if elem_d['comma'] else ''
    lett     = '\nlet. ' + elem_d['lett']  if elem_d['lett']  else ''
    cod_type = '\n' + elem_d['type'] if elem_d['type'] != 'UNKNOW' and elem_d['type'] != 'NaN' else None
    size = normalize_weight(elem_weight)
    struct_obj  = {
        'id'       : elem_d['_id'],
        'label'    : f"art. {cod}{comma}{lett}{cod_type}",
        'type'     : 'ARTICOLI',
        'weight'   : elem_weight,
        'origSize' : size,
        'size'     : size,
        'isRoot'   : is_root
    }
    return struct_obj, cod_type

def create_decr_elem(elem_d, elem_weight, is_root):
    cod      = elem_d['art']
    comma    = '\nco.'  + elem_d['comma'] if elem_d['comma'] else ''
    lett     = '\nlet. ' + elem_d['lett']  if elem_d['lett']  else ''
    cod_type = '\n' + elem_d['type']
    num      = '\nn.' + elem_d['num']  if elem_d['num']  else ''
    date     = '\n' + elem_d['date'] if elem_d['date'] else ''
    year     = '\n' + elem_d['year'] if elem_d['year'] and date == '' else ''
    size = normalize_weight(elem_weight)
    struct_obj  = {
        'id'       : elem_d['_id'],
        'label'    : f"art. {cod}{comma}{lett} {cod_type}{num}{date}{year}",
        'type'     : 'DECRETI',
        'weight'   : elem_weight,
        'origSize' : size,
        'size'     : size,
        'isRoot'   : is_root
    }
    return struct_obj

def create_cass_elem(elem_d, elem_weight, is_root):
    type_    = elem_d['type']
    sez      = '\nsez. ' + elem_d['sez']  if elem_d['sez'] != 'NoSez' else '\nNoSez'
    num      = '\nn.'  + elem_d['num']  if elem_d['num']  else ''
    date     = '\n' + elem_d['date'] if elem_d['date'] else ''
    year     = '\n' + elem_d['year'] if elem_d['year'] and date == '' else ''
    size     = normalize_weight(elem_weight)
    struct_obj   = {
        'id'       : elem_d['_id'],
        'label'    : f'CASS. {type_}{sez}{num}{date}{year}',
        'type'     : 'CASSAZIONE',
        'weight'   : elem_weight,
        'origSize' : size,
        'size'     : size,
        'isRoot'   : is_root
    }
    return struct_obj
