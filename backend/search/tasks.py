from celery.decorators import task
from django.db import connection
from customers.models import Client
from arango import ArangoClient 
from arango import AQLQueryExecuteError, ServerConnectionError
import os

import logging
logger = logging.getLogger(__name__)

@task(name='init_connection_db')
def init_connection_db():

    actual_schema = connection.schema_name 
    tenant_info = Client.objects.all()
    tenant_info_dict = [i for i in tenant_info.values()
                    if i['schema_name'] == actual_schema]
    #print(tenant_info_dict)

    try:
        client = ArangoClient(hosts=os.environ.get('ARANGO_HOST'))
        db = client.db(tenant_info_dict[0]['arango_db'],
                    username=os.environ.get('ARANGO_USERNAME'),
                    password=os.environ.get('ARANGO_PASSWORD'))
        aql = db.aql
        return aql
    except ServerConnectionError:
        logger.error("[-] Arango ServerConnectionError")


#person filename location su questa query
@task(name="multiscope_query", bind=True)
def multiscope_query(self, query_dict):
    try:
        aql = init_connection_db()

        if query_dict['file_type'] == 'None':
            cursor = aql.execute(

                """
                    FOR element IN FULLTEXT(@collection, 'name', @searched)

                        LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)

                        LET Vertices = (
                            FOR v, e, g in 1..@deep ANY element GRAPH idb
                            FILTER v.name NOT IN BLACKLIST[*].name

                            LET EdgesCount = v.type == 'FILENAME'? LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1) -2 : LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)

                            RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

                        LET Edges = (
                            FOR v, e, g in 1..@deep ANY element GRAPH idb
                            FILTER v.name NOT IN BLACKLIST[*].name

                            RETURN DISTINCT e)

                    RETURN {element, elem_weight, Vertices, Edges}
                """,
                bind_vars = {'searched' : query_dict['query'],
                            'collection' : query_dict['type'], # always check if list is not empty
                            'deep' : int(query_dict['deep'])}
                )

        elif query_dict['type'] == 'FILENAME':

            cursor = aql.execute(

            """
                FOR element IN FULLTEXT(@collection, 'name', @searched)
                    FILTER element.type == @type

                    LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)

                    LET Vertices = (
                        FOR v, e, g in 1..@deep ANY element GRAPH idb
                        FILTER v.name NOT IN BLACKLIST[*].name

                        LET EdgesCount = v.type == 'FILENAME'? LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1) -2 : LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)

                        RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

                    LET Edges = (
                        FOR v, e, g in 1..@deep ANY element GRAPH idb
                        FILTER v.name NOT IN BLACKLIST[*].name

                        RETURN DISTINCT e)

                RETURN {element, elem_weight, Vertices, Edges}
            """,
            bind_vars = {'searched' : query_dict['query'],
                        'collection' : query_dict['type'], # always check if list is not empty
                        'deep' : int(query_dict['deep']),
                        'type' : query_dict['file_type']}
            )

        else:
            cursor = aql.execute(

                    """
                        FOR element IN FULLTEXT(@collection, 'name', @searched)
                            LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)

                            LET Vertices = (
                                FOR v, e, g in 1..@deep ANY element GRAPH idb
                                FILTER v.name NOT IN BLACKLIST[*].name
                                FILTER v.type == @type

                                LET EdgesCount = v.type == 'FILENAME'? LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1) -2 : LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)

                                RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

                            LET Edges = (
                                FOR v, e, g in 1..@deep ANY element GRAPH idb
                                FILTER v.name NOT IN BLACKLIST[*].name
                                FILTER v.type == @type

                                RETURN DISTINCT e)

                        RETURN {element, elem_weight, Vertices, Edges}
                    """,
                    bind_vars = {'searched' : query_dict['query'],
                                'collection' : query_dict['type'], # always check if list is not empty
                                'deep' : int(query_dict['deep']),
                                'type' : query_dict['file_type']}
                    )

            # gestire AQLQueryExecuteError se input_query e' vuoto!!!
        res_list = [i for i in cursor]
        return res_list
    except AQLQueryExecuteError:
        logger.error("[-] AQLQueryExecuteError - DB not found")

@task(name='articles_query', bind=True)
def articles_query(self, query_dict):
    try:

        #print(query_dict)

        aql = init_connection_db()

        art_num = query_dict['art']
        art_opt = query_dict['opt']
        art_lett = query_dict['lett'] if query_dict['lett'] != '' else None
        art_comma = query_dict['comma']
        art_type  = query_dict['type']

        #print(art_num, art_lett, art_comma, art_type)

        #aggiungere il campo attr per dare l'attributo dell'articolo
        #quindi migliorare la query al fine di interpretare la mancata immissione di attr

        if (art_lett == None and art_comma == None):
            cursor = aql.execute(
                """
                FOR element IN ARTICOLI
                    FILTER element.type == @art_type
                    FILTER element.num_no_attr == @art_num
                    FILTER element.attr == @art_attr

                LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)


                LET Vertices = (
                    FOR v, e, g in 0..@deep ANY element GRAPH idb

                    FILTER v.name NOT IN BLACKLIST[*].name
                    LET EdgesCount = LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)
                    RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

                LET Edges = (
                    FOR v, e, g in 1..@deep ANY element GRAPH idb

                    FILTER v.name NOT IN BLACKLIST[*].name
                    RETURN DISTINCT e)

                RETURN {element, elem_weight, Vertices, Edges}
                """,
                bind_vars = {'art_type' : art_type,
                        'art_num': art_num,
                        'art_attr' : art_opt,
                        'deep' : int(query_dict['deep'])}
            )

        else:
            cursor = aql.execute(
                    """
                    FOR element IN ARTICOLI
                        FILTER element.type == @art_type
                        FILTER element.num_no_attr == @art_num
                        FILTER element.attr == @art_attr
                        FILTER element.comma == @comma
                        FILTER element.lett == @lett

                    LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)


                    LET Vertices = (
                        FOR v, e, g in 0..@deep ANY element GRAPH idb

                        FILTER v.name NOT IN BLACKLIST[*].name
                        LET EdgesCount = LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)
                        RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

                    LET Edges = (
                        FOR v, e, g in 1..@deep ANY element GRAPH idb

                        FILTER v.name NOT IN BLACKLIST[*].name
                        RETURN DISTINCT e)

                    RETURN {element, elem_weight, Vertices, Edges}
                    """,
                    bind_vars = {'art_type' : art_type,
                            'art_num': art_num,
                            'art_attr' : art_opt,
                            'comma': art_comma,
                            'lett': art_lett,
                            'deep' : int(query_dict['deep'])}
            )
        res_list = [i for i in cursor]
        #print(res_list)
        return res_list
    except AQLQueryExecuteError:
        logger.error("[-] AQLQueryExecuteError DB not found!")
        

@task(name="rgnr_query", bind=True)
def rgnr_query(self, query_dict):
    try:
        aql = init_connection_db()
    
        idp_code, idp_date, idp_type = query_dict['query'], query_dict['date'], query_dict['type']

        cursor    = aql.execute(
                """
                FOR element IN IDPROC
                    FILTER element.type == @idp_type
                    FILTER element.code == @idp_code
                    FILTER element.date == @idp_date

                LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)


                LET Vertices = (
                    FOR v, e, g in 0..@deep ANY element GRAPH idb
                    FILTER v.name NOT IN BLACKLIST[*].name
                    LET EdgesCount = LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)
                    RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

                LET Edges = (
                    FOR v, e, g in 1..@deep ANY element GRAPH idb
                    FILTER v.name NOT IN BLACKLIST[*].name
                    RETURN DISTINCT e)

                RETURN {element, elem_weight, Vertices, Edges}
                """,
                bind_vars = {'idp_type' : idp_type,
                        'idp_code': idp_code,
                        'idp_date': idp_date,
                        'deep' : int(query_dict['deep']) }
        )
        res_list = [i for i in cursor]
        #print(res_list)
        return res_list
    except AQLQueryExecuteError:
        logger.error("[-] AQLQueryExecuteError DB not found!")
        
@task(name="decr_query", bind=True)
def decr_query(self, query_dict):

    try:

        aql = init_connection_db()
        art_num   = query_dict['art']
        art_opt   = query_dict['opt']
        art_comma = str(query_dict['comma']) if query_dict['comma'] else None
        art_lett  = str(query_dict['lett']) if query_dict['lett'] else None
        art_type  = query_dict['type']
        num       = query_dict['num']
        year      = query_dict['year']


        if (art_comma == None and art_lett == None and num == None and year == None):
            cursor = aql.execute(
            """
            FOR element IN DECRETI
                FILTER element.type == @art_type
                FILTER element.art_no_attr == @art_num
                FILTER element.attr[0] == @art_attr

            LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)


            LET Vertices = (
                FOR v, e, g in 0..@deep ANY element GRAPH idb
                LET EdgesCount = LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)
                RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

            LET Edges = (
                FOR v, e, g in 1..@deep ANY element GRAPH idb
                RETURN DISTINCT e)

            RETURN {element, elem_weight, Vertices, Edges}
            """,
            count = True,
            bind_vars = {
                    'art_type' : art_type,
                    'art_num'  : str(art_num),
                    'art_attr' : str(art_opt),
                    'deep'     : int(query_dict['deep'])
                }
            )

        elif art_comma == None and art_lett == None:
            cursor = aql.execute(
            """
            FOR element IN DECRETI
                FILTER element.type == @art_type
                FILTER element.art_no_attr == @art_num
                FILTER element.attr[0] == @art_attr
                FILTER element.num == @num

            LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)


            LET Vertices = (
                FOR v, e, g in 0..@deep ANY element GRAPH idb
                LET EdgesCount = LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)
                RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

            LET Edges = (
                FOR v, e, g in 1..@deep ANY element GRAPH idb
                RETURN DISTINCT e)

            RETURN {element, elem_weight, Vertices, Edges}
            """,
            count = True,
            bind_vars = {
                    'art_type' : art_type,
                    'art_num'  : str(art_num),
                    'art_attr' : str(art_opt),
                    'num'      : str(num),
                    'deep'     : int(query_dict['deep'])
                }
            )
        elif num == None and year == None:
            cursor = aql.execute(
            """
            FOR element IN DECRETI
                FILTER element.type == @art_type
                FILTER element.art_no_attr == @art_num
                FILTER element.attr[0] == @art_attr
                FILTER element.comma == @comma
                FILTER element.lett == @lett

            LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)


            LET Vertices = (
                FOR v, e, g in 0..@deep ANY element GRAPH idb
                LET EdgesCount = LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)
                RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

            LET Edges = (
                FOR v, e, g in 1..@deep ANY element GRAPH idb
                RETURN DISTINCT e)

            RETURN {element, elem_weight, Vertices, Edges}
            """,
            count = True,
            bind_vars = {
                    'art_type' : art_type,
                    'art_num'  : str(art_num),
                    'art_attr' : str(art_opt),
                    'comma'    : art_comma,
                    'lett'     : art_lett,
                    'deep'     : int(query_dict['deep'])
                }
            )
        else:
            cursor = aql.execute(
            """
            FOR element IN DECRETI
                FILTER element.type == @art_type
                FILTER element.art_no_attr == @art_num
                FILTER element.attr[0] == @art_attr
                FILTER element.comma == @comma
                FILTER element.lett == @lett
                FILTER element.num == @num
                FILTER element.year == @year

            LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)


            LET Vertices = (
                FOR v, e, g in 0..@deep ANY element GRAPH idb
                LET EdgesCount = LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)
                RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

            LET Edges = (
                FOR v, e, g in 1..@deep ANY element GRAPH idb
                RETURN DISTINCT e)

            RETURN {element, elem_weight, Vertices, Edges}
            """,
            count = True,
            bind_vars = {
                    'art_type' : art_type,
                    'art_num'  : str(art_num),
                    'art_attr' : str(art_opt),
                    'comma'    : art_comma,
                    'lett'     : art_lett,
                    'num'      : str(num),
                    'year'     : str(year),
                    'deep'     : int(query_dict['deep'])
                }
            )

        res_list = [i for i in cursor]
        return res_list
    except AQLQueryExecuteError:
        logger.error("[-] AQLQueryExecuteError DB not found!")


@task(name='cass_query', bind=True)    
def cass_query(self,query_dict):
    
    try:
        aql = init_connection_db()
        
        cass_num = query_dict['num']
        cass_year = query_dict['year']
        cass_sez = query_dict['sez']
        cass_type = query_dict['type']
        
        
        if cass_year != '':
            cursor = aql.execute(
                    """
                    FOR element IN CASSAZIONE
                        FILTER element.type == @cass_type
                        FILTER element.sez == @sez
                        FILTER element.num == @num
                        FILTER element.year == @year

                    LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)

                    LET Vertices = (
                        FOR v, e, g in 0..@deep ANY element GRAPH idb
                        LET EdgesCount = LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)
                        RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

                    LET Edges = (
                        FOR v, e, g in 1..@deep ANY element GRAPH idb
                        RETURN DISTINCT e)

                    RETURN {element, elem_weight, Vertices, Edges}
                    """,
                    count = True,
                    bind_vars = {
                        'cass_type' : cass_type,
                        'sez'       : cass_sez,
                        'num'       : str(cass_num),
                        'year'      : str(cass_year),
                        'deep'      : int(query_dict['deep'])
                    }
            )
        else:
            cursor = aql.execute(
                    """
                    FOR element IN CASSAZIONE
                        FILTER element.type == @cass_type
                        FILTER element.sez == @sez
                        FILTER element.num == @num

                    LET elem_weight = LENGTH(FOR v1 IN 1..1 ANY element GRAPH idb RETURN 1)

                    LET Vertices = (
                        FOR v, e, g in 0..@deep ANY element GRAPH idb
                        LET EdgesCount = LENGTH(FOR v1 IN 1..1 ANY v GRAPH idb RETURN 1)
                        RETURN DISTINCT {'node':v, 'weight' : EdgesCount})

                    LET Edges = (
                        FOR v, e, g in 1..@deep ANY element GRAPH idb
                        RETURN DISTINCT e)

                    RETURN {element, elem_weight, Vertices, Edges}
                    """,
                    count = True,
                    bind_vars = {
                        'cass_type' : cass_type,
                        'sez'       : cass_sez,
                        'num'       : str(cass_num),
                        'deep'      : int(query_dict['deep'])
                    }
            )
        res_list = [i for i in cursor]
        #print(res_list)
        return res_list
    except AQLQueryExecuteError:
        logger.error("[-] AQLQueryExecuteError DB not found!")


@task(name='blacklist', bind=True)
def blacklist(self, content_to_read):

    aql = init_connection_db()
    res_list = list()
    b_l_elements = list()

    line = content_to_read[1:-1]
    b_l_elements = (line.strip().split('", "'))
    #print(b_l_elements)

    for element in b_l_elements:
        # Configure AQL query cache properties
        cursor = aql.execute(
            """
            FOR collection IN [PERSON, FILENAME, LOCATION]
                FOR elem IN collection
                FILTER NGRAM_POSITIONAL_SIMILARITY(LOWER(elem.name), LOWER(@searched), 3) > 0.88
                return elem
            """,
            count = True,
            bind_vars = {
                'searched' : element,
             }
            )
        if cursor.count() == 1:
            res_list.append(cursor.pop())
        elif cursor.count() == 0:
            print(f"no result for {element}")
        else:
            print(f"{cursor.count()} result for {element}: {[n for n in cursor]}")


    if aql.has_collection('BLACKLIST'):
        aql.delete_collection('BLACKLIST')
        blist = aql.create_collection('BLACKLIST')
    else:
        blist = aql.create_collection('BLACKLIST')

    for elem in res_list:
        blist.insert({'name' : elem['name']})





