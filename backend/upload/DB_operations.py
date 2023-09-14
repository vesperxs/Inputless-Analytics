# -*- coding: utf-8 -*-
from decouple import config
from arango import ArangoClient
from arango import ServerConnectionError
from customers.models import Client
from django.db import connection
import os
import logging



logger = logging.getLogger(__name__)

def initialize_db(actual_schema):
    """
    input: connection.schema_name
    
    Select the actual tenant's info 
    """
    #DB CONNECTION
    try:
        doc_counter = 0
        tenant_info = Client.objects.all()
        tenant_info_dict = [i for i in tenant_info.values()
                            if i['schema_name'] == actual_schema]
        #print(tenant_info_dict)


        client = ArangoClient(hosts=os.environ.get('ARANGO_HOST'))
        sys_db = client.db('_system',
                        username=os.environ.get('ARANGO_USERNAME'),
                        password=os.environ.get('ARANGO_PASSWORD'))

        if not sys_db.has_database(tenant_info_dict[0]['arango_db']):
            sys_db.create_database(name = tenant_info_dict[0]['arango_db'])

        db = client.db(tenant_info_dict[0]['arango_db'],
                    username=os.environ.get('ARANGO_USERNAME'),
                       password=os.environ.get('ARANGO_PASSWORD'))

        coll_dict = initialize_collections(db) #inizializza le collections
        return (db,coll_dict)
    except ServerConnectionError:
        logger.error("[-] Arango ServerConnectionError")

def initialize_collections(db):
    if db.has_collection('IDPROC'):
        id_proc_coll = db.collection('IDPROC')
    else:
        id_proc_coll = db.create_collection('IDPROC')

    if db.has_collection('FILENAME'):
        filename_coll = db.collection('FILENAME')
    else:
        filename_coll = db.create_collection('FILENAME')
        filename_coll.add_fulltext_index(fields=["name"])

    if db.has_collection('CASSAZIONE'):
        cass_coll = db.collection('CASSAZIONE')
    else:
        cass_coll = db.create_collection('CASSAZIONE')

    if db.has_collection('DECRETI'):
        decr_coll = db.collection('DECRETI')
    else:
        decr_coll = db.create_collection('DECRETI')

    if db.has_collection('ARTICOLI'):
        art_coll = db.collection('ARTICOLI')
    else:
        art_coll = db.create_collection('ARTICOLI')

    if db.has_collection('PERSON'):
        pers_coll = db.collection('PERSON')
    else:
        pers_coll = db.create_collection('PERSON')
        pers_coll.add_fulltext_index(fields=["name"])

    if db.has_collection('LOCATION'):
        loc_coll = db.collection('LOCATION')
    else:
        loc_coll = db.create_collection('LOCATION')
        loc_coll.add_fulltext_index(fields=["name"])

    #if db.has_collection('ORGANIZATION'):
    #    org_coll = db.collection('ORGANIZATION')
    #else:
    #    org_coll = db.create_collection('ORGANIZATION')
    #    org_coll.add_fulltext_index(fields=["name"])

    if db.has_collection('FILE_IDPROC'):
        f_to_id_coll = db.collection('FILE_IDPROC')
    else:
        f_to_id_coll = db.create_collection('FILE_IDPROC', edge=True)

    if db.has_collection('FILE_ARTICOLI'):
        f_to_art_coll = db.collection('FILE_ARTICOLI')
    else:
        f_to_art_coll = db.create_collection('FILE_ARTICOLI', edge=True)

    if db.has_collection('FILE_DECR'):
        f_to_decr_coll = db.collection('FILE_DECR')
    else:
        f_to_decr_coll = db.create_collection('FILE_DECR', edge=True)

    if db.has_collection('FILE_CASS'):
        f_to_cass_coll = db.collection('FILE_CASS')
    else:
        f_to_cass_coll = db.create_collection('FILE_CASS', edge=True)

    if db.has_collection('FILE_PERSON'):
        f_to_pers_coll = db.collection('FILE_PERSON')
    else:
        f_to_pers_coll = db.create_collection('FILE_PERSON', edge=True)

    if db.has_collection('FILE_LOCATION'):
        f_to_loc_coll = db.collection('FILE_LOCATION')
    else:
        f_to_loc_coll = db.create_collection('FILE_LOCATION', edge=True)

    #if db.has_collection('FILE_ORGANIZATION'):
    #    f_to_org_coll = db.collection('FILE_ORGANIZATION')
    #else:
    #    f_to_org_coll = db.create_collection('FILE_ORGANIZATION', edge=True)
    if db.has_collection('BLACKLIST'):
        blist = db.collection('BLACKLIST')
    else:
        blist = db.create_collection('BLACKLIST', edge=True)

    coll_dict = {
        "IDPROC"            : id_proc_coll,
        "FILENAME"          : filename_coll,
        "CASSAZIONE"        : cass_coll,
        "DECRETI"           : decr_coll,
        "ARTICOLI"          : art_coll,
        "PERSON"            : pers_coll,
        "LOCATION"          : loc_coll,
        #"ORGANIZATION"      : org_coll,
        "FILE_IDPROC"       : f_to_id_coll,
        "FILE_ARTICOLI"     : f_to_art_coll,
        "FILE_DECR"         : f_to_decr_coll,
        "FILE_CASS"         : f_to_cass_coll,
        "FILE_PERSON"       : f_to_pers_coll,
        "FILE_LOCATION"     : f_to_loc_coll,
        #"FILE_ORGANIZATION" : f_to_org_coll
        }
    return coll_dict

def idproc_search_populate(db, idp_obj, id_proc_coll, f_to_id_coll, file_index):
    cursor = db.aql.execute(
    """
    FOR idp IN IDPROC
        FILTER idp.code == @codice AND idp.date == @data
    return idp
    """,
        bind_vars = {'codice' : idp_obj.code,
                     'data'   : idp_obj.date
                     }
    )
    if cursor.empty():
        inserted = id_proc_coll.insert(idp_obj.export())
        f_to_id_coll.insert({'_from' : file_index, '_to' : inserted['_id']})
    else:
        idp_obj = cursor.pop()
        f_to_id_coll.insert({'_from' : file_index, '_to' : idp_obj["_id"]})

def person_search_populate(db, pers_obj, pers_coll, f_to_pers_coll, file_index):
    cursor = db.aql.execute(
    """
    FOR pers IN PERSON

        FILTER NGRAM_POSITIONAL_SIMILARITY(LOWER(pers.name), LOWER(@name), 3) > 0.60
    RETURN pers
    """,
        bind_vars = {'name' : pers_obj.name}
    )
    if cursor.empty():
        inserted = pers_coll.insert(pers_obj.export())
        f_to_pers_coll.insert({'_from' : file_index, '_to' : inserted["_id"]})
    else:
        pers_obj = cursor.pop()
        f_to_pers_coll.insert({'_from' : file_index, '_to' : pers_obj["_id"]})

def search_duplicate_filename(db, doc_obj, filename_coll):
    cursor = db.aql.execute(
    """
    FOR doc IN FILENAME
        FILTER doc.name == @name
        RETURN doc
    """,
        bind_vars = {'name' : doc_obj.name
                    }
    )
    if cursor.empty():
        inserted = filename_coll.insert(doc_obj.export())
        return inserted
    else:
        return None

def check_filename(db, file_name, filename_coll):
    cursor = db.aql.execute(
    """
    FOR doc IN FILENAME
        FILTER doc.name == @name
        RETURN doc
    """,
        bind_vars = {'name' : file_name
                    }
    )
    if cursor.empty():
        return True
    else:
        return False


def cass_search_populate(db, cass_obj, cass_coll, f_to_cass_coll, file_index):
    cursor = db.aql.execute(
    """
    FOR cass IN CASSAZIONE
        FILTER cass.type == @tipo AND cass.sez == @sez AND cass.year == @anno AND cass.num == @num
    return cass
    """,
        bind_vars = {'tipo' : cass_obj.type_,
                     'sez'   : cass_obj.sez,
                     'anno' : cass_obj.year,
                     'num'  : cass_obj.num
                     }
    )
    if cursor.empty():
        inserted = cass_coll.insert(cass_obj.export())
        f_to_cass_coll.insert({'_from' : file_index, '_to' : inserted["_id"]})
    else:
        cass_obj = cursor.pop()
        f_to_cass_coll.insert({'_from' : file_index, '_to' : cass_obj["_id"]})


def decr_search_populate(db, decr_obj, decr_coll, f_to_decr_coll, file_index):
    cursor = db.aql.execute(
    """
    FOR decr IN DECRETI
        FILTER decr.art == @art AND decr.num == @num AND decr.comma == @comma AND decr.lett == @lett
    return decr
    """,
        bind_vars = {'art'  : decr_obj.art,
                     'num'  : decr_obj.num,
                     'comma': decr_obj.comma,
                     'lett' : decr_obj.lett
                     }
    )
    if cursor.empty():
        inserted = decr_coll.insert(decr_obj.export())
        f_to_decr_coll.insert({'_from' : file_index, '_to' : inserted["_id"]})
    else:
        decr_obj = cursor.pop()
        f_to_decr_coll.insert({'_from' : file_index, '_to' : decr_obj["_id"]})

def loc_search_populate(db, loc_obj, loc_coll, f_to_loc_coll, file_index):
    cursor = db.aql.execute(
    """
    FOR loc IN LOCATION
        LET dist = NGRAM_POSITIONAL_SIMILARITY(LOWER(loc.name), LOWER(@name), 3)
        LET sim =  NGRAM_SIMILARITY(LOWER(loc.name), LOWER(@name), 3)
        LET lev = LEVENSHTEIN_DISTANCE(loc.name, @name)
        FILTER NGRAM_POSITIONAL_SIMILARITY(LOWER(loc.name), LOWER(@name), 3) > 0.60
    RETURN loc
    """,
        bind_vars = {'name' : loc_obj.name}
    )
    if cursor.empty():
        inserted = loc_coll.insert(loc_obj.export())
        f_to_loc_coll.insert({'_from' : file_index, '_to' : inserted["_id"]})
    else:
        loc_obj = cursor.pop()
        f_to_loc_coll.insert({'_from' : file_index, '_to' : loc_obj["_id"]})

def org_search_populate(db, org_obj, org_coll, f_to_org_coll, file_index):
    cursor = db.aql.execute(
    """
    FOR org IN ORGANIZATION
        LET dist = NGRAM_POSITIONAL_SIMILARITY(LOWER(org.name), LOWER(@name), 3)
        LET sim =  NGRAM_SIMILARITY(LOWER(org.name), LOWER(@name), 3)
        LET lev = LEVENSHTEIN_DISTANCE(org.name, @name)
        FILTER NGRAM_POSITIONAL_SIMILARITY(LOWER(org.name), LOWER(@name), 3) > 0.60
    RETURN org
    """,
        bind_vars = {'name' : org_obj.name}
    )
    if cursor.empty():
        inserted = org_coll.insert(org_obj.export())
        f_to_org_coll.insert({'_from' : file_index, '_to' : inserted["_id"]})
    else:
        org_obj = cursor.pop()
        f_to_org_coll.insert({'_from' : file_index, '_to' : org_obj["_id"]})

def art_search_populate(db, art_obj, art_coll, f_to_art_coll, file_index):
    cursor = db.aql.execute(
    """
    FOR art IN ARTICOLI
        FILTER art.type == @tipo AND art.num == @num AND art.comma == @comma AND art.lett == @lett
    return art
    """,
        bind_vars = {'tipo'  : art_obj.type_,
                     'num'   : art_obj.num,
                     'comma' : art_obj.comma,
                     'lett'  : art_obj.lett
                     }
    )
    if cursor.empty():
        inserted = art_coll.insert(art_obj.export())
        f_to_art_coll.insert({'_from' : file_index, '_to' : inserted["_id"]})
    else:
        art_obj = cursor.pop()
        f_to_art_coll.insert({'_from' : file_index, '_to' : art_obj["_id"]})

def create_graph(db):
    if db.has_graph('idb'):
        idb = db.graph('idb')
    else:
        idb = db.create_graph('idb')

    if not idb.has_edge_definition('FILE_ARTICOLI'):
        idb.create_edge_definition(
        edge_collection='FILE_ARTICOLI',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['ARTICOLI']
        )
    else:
        idb.replace_edge_definition(
        edge_collection='FILE_ARTICOLI',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['ARTICOLI']
        )
    if not idb.has_edge_definition('FILE_IDPROC'):
        idb.create_edge_definition(
        edge_collection='FILE_IDPROC',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['IDPROC']
        )
    else:
        idb.replace_edge_definition(
        edge_collection='FILE_IDPROC',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['IDPROC']
        )
    if not idb.has_edge_definition('FILE_CASS'):
        idb.create_edge_definition(
        edge_collection='FILE_CASS',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['CASSAZIONE']
        )
    else:
        idb.replace_edge_definition(
        edge_collection='FILE_CASS',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['CASSAZIONE']
        )
    if not idb.has_edge_definition('FILE_DECR'):
        idb.create_edge_definition(
        edge_collection='FILE_DECR',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['DECRETI']
        )
    else:
        idb.replace_edge_definition(
        edge_collection='FILE_DECR',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['DECRETI']
        )

    if not idb.has_edge_definition('FILE_PERSON'):
        idb.create_edge_definition(
        edge_collection='FILE_PERSON',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['PERSON']
        )
    else:
        idb.replace_edge_definition(
        edge_collection='FILE_PERSON',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['PERSON']
        )

    # if not idb.has_edge_definition('FILE_ORGANIZATION'):
    #     idb.create_edge_definition(
    #     edge_collection='FILE_ORGANIZATION',
    #     from_vertex_collections=['FILENAME'],
    #     to_vertex_collections=['ORGANIZATION']
    #     )
    # else:
    #     idb.replace_edge_definition(
    #     edge_collection='FILE_ORGANIZATION',
    #     from_vertex_collections=['FILENAME'],
    #     to_vertex_collections=['ORGANIZATION']
    #     )

    if not idb.has_edge_definition('FILE_LOCATION'):
        idb.create_edge_definition(
        edge_collection='FILE_LOCATION',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['LOCATION']
        )
    else:
        idb.replace_edge_definition(
        edge_collection='FILE_LOCATION',
        from_vertex_collections=['FILENAME'],
        to_vertex_collections=['LOCATION']
        )


def extract_coll_stats(db):
    aql = db.aql
    try:
        cursor = aql.execute(
            """
            FOR fname in FILENAME
                return fname.type
            """
        )
        fname_list = [i for i in cursor]

        cursor = aql.execute(
            """
            FOR art in ARTICOLI
                return art.type
            """
        )
        art_list = [i for i in cursor]

        return fname_list, art_list
    except AQLQueryExecuteError:
        logger.error("[-] AQLQueryExecuteError - DB not found")

def extract_coll_quantity(db):
    aql = db.aql
    try:
        cursor = aql.execute(
            """
            let arts = length(ARTICOLI)
            let fnames = length(FILENAME)
            let cass = length(CASSAZIONE)
            let decrs = length(DECRETI)
            let idprocs = length(IDPROC)
            let pers = length(PERSON)
            let locs = length(LOCATION)

            return {arts : arts, fnames : fnames, cass : cass, decrs : decrs, idprocs : idprocs, pers : pers, locs : locs}
            """
        )
        coll_list = [i for i in cursor]

        return coll_list[0]
    except AQLQueryExecuteError:
        logger.error("[-] AQLQueryExecuteError - DB not found")
