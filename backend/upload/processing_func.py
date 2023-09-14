# -*- coding: utf-8 -*-

from .pattern_types import *
from .categorization_funcs import *
from .search_funcs import *
from .search_string_funcs import *
from .DB_operations import *



def process_all(db, coll_dict, obj):
    inserted = processing_filename(db, coll_dict, obj['doc'])
    if inserted: #se il documento non è già presente nel database
        processing_id_proc(db, coll_dict, obj['id_proc'], inserted['_id'])
        processing_law(db, coll_dict, obj['law'], inserted['_id'])
        processing_person(db, coll_dict, obj['person'], inserted['_id'])
        processing_locs(db, coll_dict, obj['loc'], inserted['_id'])
        #processing_orgs(db, coll_dict, obj['org'], inserted['_id'])

def processing_filename(db, coll_dict, file_name):
    file_type = categorize_file(file_name)
    file_name = filename_cleaning(file_name)
    #print(index)
    doc = Filename(name=file_name, type_=file_type)
    is_not_dup = search_duplicate_filename(db, doc, coll_dict['FILENAME'])
    return is_not_dup

def processing_id_proc(db, coll_dict, id_proc_l, file_index):
    for proc_id_str in id_proc_l:
        code, year = find_rg_code(proc_id_str)
        if code:
            rg_type = categorize_idproc(proc_id_str)
            if rg_type != 'NaN':
                mod = mod_search(proc_id_str)
                idp_obj = Id_proc(code=code,
                                  type_=rg_type,
                                  mod=mod, date=year,
                                  raw_s=proc_id_str)
                
                idproc_search_populate(db,
                                       idp_obj,
                                       coll_dict['IDPROC'],
                                       coll_dict['FILE_IDPROC'],
                                       file_index)


def processing_law(db, coll_dict, law_l, file_index):

    decr_types = ['D.P.G.R.', 'DLGS', 'D.L.', 'D.M.', 'LEGGE', 'D.P.R.', 'REGIO DECRETO']

    #CASSAZIONE
    for law_str in law_l:
        law_type = categorize_law(law_str) #search law type
        if law_type != 'NaN':
            if law_type == 'CASSAZIONE':
                cass_type = find_cass_type(law_str)
                cass_sez = find_cass_sez(law_str)
                cass_num, cass_year = find_number(law_str)
                cass_date = find_dates(law_str)
                if cass_num:
                    if cass_date and (not cass_year):
                        cass_year = find_years(cass_date)
                        
                    cass_obj = Cassazione(type_=cass_type,
                                        sez=cass_sez,
                                        year=cass_year,
                                        date=cass_date,
                                        num=cass_num,
                                        raw_s=law_str)
                    
                    cass_search_populate(db,
                                        cass_obj,
                                        coll_dict["CASSAZIONE"],
                                        coll_dict["FILE_CASS"],
                                        file_index)

            # DECRETI
            elif law_type in decr_types:
                decr_arts = find_articles_in_codes(law_str)
                commas_and_letters_decr_list = find_arts_with_commas_and_letters(law_str)
                decr_num, decr_year = find_numbers_in_decr(law_str)
                decr_date = find_dates(law_str)
                if decr_date and (not decr_year):
                    decr_year = find_years(decr_date)
                for art_ in decr_arts:
                    art_no_attr, attr = separate_num_attr(art_)
                    decr_obj = Decreto(type_=law_type,
                                    art=art_,
                                    art_no_attr = art_no_attr,
                                    attr = attr,
                                    num=decr_num,
                                    year=decr_year,
                                    date=decr_date,
                                    comma=None,
                                    lett=None,
                                    raw_s=law_str)
                    
                    decr_search_populate(db,
                                        decr_obj,
                                        coll_dict["DECRETI"],
                                        coll_dict["FILE_DECR"],
                                        file_index)

                for decr_c_l in commas_and_letters_decr_list:
                    art_, commas, letters = decr_c_l
                    art_no_attr, attr = separate_num_attr(art_)
                    for c_i in range(0, len(commas) - 1):
                        #if c_i != (len(commas) - 1):
                        decr_obj = Decreto(type_=law_type,
                                        art = art_,
                                        art_no_attr = art_no_attr,
                                        attr = attr,
                                        num = decr_num,
                                        year = decr_year,
                                        date = decr_date,
                                        comma = commas[c_i],
                                        lett = None,
                                        raw_s = law_str)
                        
                        decr_search_populate(db,
                                            decr_obj,
                                            coll_dict["DECRETI"],
                                            coll_dict["FILE_DECR"],
                                            file_index)
                    if commas:
                        for let in letters:
                            decr_obj = Decreto(type_=law_type,
                                            art=art_,
                                            art_no_attr = art_no_attr,
                                            attr = attr,
                                            num=decr_num,
                                            year=decr_year,
                                            date=decr_date,
                                            comma=commas[-1],
                                            lett=let,
                                            raw_s=law_str)
                            
                            decr_search_populate(db,
                                                decr_obj,
                                                coll_dict["DECRETI"],
                                                coll_dict["FILE_DECR"],
                                                file_index)


                        decr_obj = Decreto(type_=law_type,
                                        art=art_,
                                        art_no_attr = art_no_attr,
                                        attr = attr,
                                        num=decr_num,
                                        year=decr_year,
                                        date=decr_date,
                                        comma=commas[-1],
                                        lett=None,
                                        raw_s=law_str)
                        
                        decr_search_populate(db,
                                            decr_obj,
                                            coll_dict["DECRETI"],
                                            coll_dict["FILE_DECR"],
                                            file_index)

            else:  # if law_type è un articolo
                codes = find_articles_in_codes(law_str)
                commas_and_letters_list = find_arts_with_commas_and_letters(law_str)
                for code_ in codes:
                    if code_:
                        num_no_attr, attr = separate_num_attr(code_)
                        art_obj = Articolo(
                            type_=law_type,
                            num=code_,
                            num_no_attr=num_no_attr,
                            attr= attr,
                            comma=None,
                            lett=None,
                            raw_s=law_str)
                        
                        art_search_populate(db,
                                            art_obj,
                                            coll_dict["ARTICOLI"],
                                            coll_dict["FILE_ARTICOLI"],
                                            file_index)

                for art_c_l in commas_and_letters_list:
                    code_, commas, letters = art_c_l
                    num_no_attr, attr = separate_num_attr(code_)
                    for c_i in range(0, len(commas)-1):
                            art_obj = Articolo(type_=law_type,
                                            num=code_,
                                            num_no_attr=num_no_attr,
                                            attr= attr,
                                            comma=commas[c_i],
                                            lett=None,
                                            raw_s=law_str)
                            
                            art_search_populate(db,
                                                art_obj,
                                                coll_dict["ARTICOLI"],
                                                coll_dict["FILE_ARTICOLI"],
                                                file_index)
                    if commas:
                        for let in letters:
                            art_obj = Articolo(type_=law_type,
                                            num=code_,
                                            num_no_attr=num_no_attr,
                                            attr= attr,
                                            comma=commas[-1],
                                            lett=let,
                                            raw_s=law_str)
                            
                            art_search_populate(db,
                                                art_obj,
                                                coll_dict["ARTICOLI"],
                                                coll_dict["FILE_ARTICOLI"],
                                                file_index)

                        art_obj = Articolo(type_=law_type,
                                        num=code_,
                                        num_no_attr=num_no_attr,
                                        attr= attr,
                                        comma=commas[-1],
                                        lett=None,
                                        raw_s=law_str)
                        
                        art_search_populate(db,
                                            art_obj,
                                            coll_dict["ARTICOLI"],
                                            coll_dict["FILE_ARTICOLI"],
                                            file_index)


def processing_person(db, coll_dict, pers_list, file_index):
    for pers in pers_list:
        name = find_person_name(pers)
        if name:
            pers_obj = Person(name = name, raw_s = pers)
            person_search_populate(db,
                                   pers_obj,
                                   coll_dict['PERSON'],
                                   coll_dict['FILE_PERSON'],
                                   file_index)

def processing_locs(db, coll_dict, locs_list, file_index):
    for loc_str in locs_list:
        loc_name = loc_str#check_loc(loc_str)
        if loc_name:
            loc_obj = Location(name = loc_name, raw_s = loc_str)
            loc_search_populate(db,
                                loc_obj,
                                coll_dict['LOCATION'],
                                coll_dict['FILE_LOCATION'],
                                file_index)

def processing_orgs(db, coll_dict, orgs_list, file_index):
    for org_str in orgs_list:
        org_name = org_str#check_org(org_str)
        if org_name:
            org_obj = Organization(name = org_name, raw_s = org_str)
            org_search_populate(db,
                                org_obj,
                                coll_dict['ORGANIZATION'],
                                coll_dict['FILE_ORGANIZATION'],
                                file_index)