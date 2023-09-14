# -*- coding: utf-8 -*-

import regex as re

def find_rg_code(proc_id):
    """Identifica l'ID del processo e lo divide in codice ed anno

    Args:
        proc_id ([string]): [identificativo del processo, es: '222/2019 mod.21 RGNR']

    Returns:
        [tuple]: [num = codice del processo
                  year = anno del processo]
        [None]: if proc_id is not a valid ID
    """
    reg_1 = r"(?<!\/|\d+)([0-9]{3,}\/[0-9]{2,})\/([0-9][0-9]){1,2}(?!\d|\/)"
    reg_2 = r"(?<!\/|\d+)([0-9]{3,})\/([0-9][0-9]){1,2}(?!\d|\/)"
    if re.search(reg_1, proc_id):
        code = re.search(reg_1, proc_id)
    elif re.search(reg_2, proc_id):
        code = re.search(reg_2, proc_id)
    else:
        code = None
    num  = code.group(1) if code else None
    year = code.group(2) if code else None
    return (num, year)



def mod_search(proc_id):
    """Trova l'eventuale codice 'mod' associato ad un id_proc

    Args:
        proc_id ([string]): [identificativo del processo, es: '222/2019 mod.21 RGNR']

    Returns:
        [int]: [eventuale numero del mod. associato]
    """
    if re.search(r"((mod\.?\s?)(\d\d))", proc_id, re.IGNORECASE):
        mod_num = re.search(r"((mod\.?\s?)(\d\d))", proc_id, re.IGNORECASE)
        if mod_num:
            mod_num = mod_num.group(3)
    else:
        mod_num = None
    #print(mod_num)
    return mod_num


def find_articles_in_codes(law):
    """Trova i numeri che si riferiscono agli articoli del codice, dei decreti, ecc,
        escludendo gli articoli cui è associato un comma
        law: stringa in cui trovare l'inforamzione
    """
    regex = r"(?<!\.\s)(?<!\/(\'|\’))(?<!\.)(?<!\/)" + \
            r"(?<!(((co\.)|(c\.)|(comm(a|i)))\s(\d+\s?(e|\,)\s)*))(?<!(lett\.?(er(a|e))?\s(\w\s?(e|\,)\s)*))(?<!\d)" + \
            r"([0-9]+((\s|\-|\s\-)?" + \
            r"((bis)|(ter)|(quater)|(qinques)|(sexies)|(septies)|(octies)|(nonies)|(decies)|(undecies)|(duodecies)))*" + \
            r"(?=\s\d|\s\-\s|\,\s?\d|\se\s|\,?\sc\.[a-z]|\,?\sd\.m\.|\sdella\s|\sdel\s|\,?\s(?=(cost)|(cod)|(I|V|X))))|((?<!(lett\.?(er(a|e))?\s(\w\s?(e|\,)\s)*))" + \
            r"(?<!(comm(a|i)\s(\d+\s?(e|\,)\s)*))(?<=((\se)|(\s?art\.?))\s)" + \
            r"(([0-9]+)(\s|\,\s)((\s|\-|\s\-)?" + \
            r"((bis)|(ter)|(quater)|(qinques)|(sexies)|(septies)|(octies)|(nonies)|(decies)|(undecies)|(duodecies))){0,2}))" + \
            r"(?!(co\.)|(c\.)|(comm(a|i)|(lett\.?)|(lettera\.)))"

    result = re.findall(regex, law, re.IGNORECASE)
    codes  = [item[14] for item in result if item[14]!=''] +\
             [item[46] for item in result if item[46]!='']
    return codes

def separate_num_attr(code_num):
    num_re = r"\d+"
    num = re.search(num_re, code_num)
    attr_re = r"[a-z]+"
    attr = re.search(attr_re, code_num, re.IGNORECASE)
    if attr:
        return (num.group(), attr.group().upper())
    else:
        return (num.group(), 'None')

"""
TODO: 1) FATTO!!!
         aggiornare prendendo anche i pattern in cui il numero del comma appare prima
         della dicitura comma (es art 12, 2 comma del cp)
      2) gestire il caso in cui a seguito delle lettere riferite ad un comma ci siano
         altri commi, riferiti allo stesso articolo (es: art 12 comma 2, 3 lett c, 4 e 5 lett e ).
         COME: trovare comma dopo aver matchato art, comma e lettera, e avvalorare
               il campo dell'articolo con quello della sottolista precedente
"""

def find_arts_with_commas_and_letters(law):
    """Estrae le stringhe in cui è presente un articolo con relativo comma ed eventuale lettera
        law: stringa in cui trovare l'informazione
        return lista di liste contenenti tre campi, il primo per l'articolo, il secondo per i commi ad esso associati,
        ed il terzo per le lettere, che si riferiscono all'ultimo comma individuato
    """
    comma_first = r"(((co\.)|(c\.)|(comm(a|i)))\s(\d+)(\s?(e|\,|ed)\s(\d+)\s?)*(?!\s((co\.)|(c\.)|(comm(a|i))))*)(\s|\,\s)?" + \
                  r"(((lett\.?)|(lettera))\s([a-z]\)?)(\s?(e|\,|ed)(?!\sn(r)?\.)\s([a-z]\)?))*)?(\s|\,\s)?" + \
                  r"((dell')?\s?art\.?\s)((\d+)((\s|\-|\s\-)?" + \
                  r"((bis)|(ter)|(quater)|(qinques)|(sexies)|(septies)|(octies)|(nonies)|(decies)|(undecies)|(duodecies)))*)"

    art_first = r"((\d+)((\s|\-|\s\-)?" + \
                r"((bis)|(ter)|(quater)|(qinques)|(sexies)|(septies)|(octies)|(nonies)|(decies)|(undecies)|(duodecies)))*)(\s|\,\s)" + \
                r"(((co\.)|(c\.)|(comm(a|i)))\s(\d+)(\s?(e|\,|ed)\s(\d+)\s?)*(?!\s((co\.)|(c\.)|(comm(a|i))))*)(\s|\,\s)?" + \
                r"(((lett\.?)|(lettera))\s([a-z]\)?)(\s?(e|\,|ed)(?!\sn(r)?\.)\s([a-z]\)?))*)?"

    commas_and_letters_list = []
    if re.search(art_first, law, re.IGNORECASE):
        commas_and_letters = re.findall(art_first, law, re.IGNORECASE)
        for c_l in commas_and_letters:
            commas   = []
            letters  = []
            let_list = []
            if c_l[0]:
                art = c_l[0]
                if c_l[17]:
                    commas = re.findall(r"\d+", c_l[17])
                    if c_l[33]:
                        letters = re.findall(
                            r"(?<=(\se(d?)\s)|(\,\s)|(tt\.?\s)|(era\s))([a-z])\)?(?=(\s|\,|\se|$))",
                            c_l[33]
                            )
                        let_list = [let[5] for let in letters]
                commas_and_letters_list.append((art,commas, let_list))
    if re.search(comma_first, law, re.IGNORECASE):
        commas_and_letters = re.findall(comma_first, law, re.IGNORECASE)
        commas_and_letters_list = []
        for c_l in commas_and_letters:
            commas, letters = 0,0
            let_list=[]
            if c_l[28]:
                art = c_l[28]
                if c_l[0]:
                    commas = re.findall('\d+', c_l[0])
                    if c_l[16]:
                        letters = re.findall(
                            r"(?<=(\se(d?)\s)|(\,\s)|(tt\.?\s)|(era\s))([a-z])\)?(?=(\s|\,|\se|$))",
                            c_l[16]
                            )
                        let_list = [let[5] for let in letters]
                commas_and_letters_list.append((art,commas, let_list))

    return commas_and_letters_list


def find_dates(text):
    """
    Ritorna una tupla contenente una data contenuta nel testo in formato numerico
    """
    date = re.search(
        r"(([0123]?\d)(\s|\/|\-|\.)" + \
        r"([01]\d|\d|gen(naio)?|feb(braio)?|mar(zo)?|apr(ile)?|mag(gio)?|giu(gno)?|lug(lio)?|ago(sto)?|set(tembre)?|ott(obre)?|nov(embre)?|dic(embre)?)" + \
        r"\.?(\s|\/|-|\.)\'?(\d\d\d\d|\'?\d\d))",
        text,
        re.IGNORECASE
        )
    #print(date)
    if date:
        day = date.group(2)
        month = date.group(4)
        year = date.group(18)
        months_d = {'gennaio'   : 1,    'gen' : 1,    '1'  : 1,    '01' : 1,
                    'febbraio'  : 2,    'feb' : 2,    '2'  : 2,    '02' : 2,
                    'marzo'     : 3,    'mar' : 3,    '3'  : 3,    '03' : 3,
                    'aprile'    : 4,    'apr' : 4,    '4'  : 4,    '04' : 4,
                    'maggio'    : 5,    'mag' : 5,    '5'  : 5,    '05' : 5,
                    'giugno'    : 6,    'giu' : 6,    '6'  : 6,    '06' : 6,
                    'luglio'    : 7,    'lug' : 7,    '7'  : 7,    '07' : 7,
                    'agosto'    : 8,    'ago' : 8,    '8'  : 8,    '08' : 8,
                    'settembre' : 9,    'set' : 9,    '9'  : 9,    '09' : 9,
                    'ottobre'   : 10,   'ott' : 10,   '10' : 10,
                    'novembre'  : 11,   'nov' : 11,   '11' : 11,
                    'dicembre'  : 12,   'dic' : 12,   '12' : 12,
                   }
        month = months_d.get(month.lower(), 'NaN')
        date = f'{day}/{month}/{year}'
        return date
    else:
        return None




def find_number(law):
    """
    Torna un tupla contenente tutti i numeri presenti in una stringa, caratterizzati dalla
    presenza del token n. or numero prima di essi
    """
    num = re.search(r"((n(\.|\°)|nr(\.|\°)|numero)\s?)((\d+)" + \
                    r"((\/|\\\\|\sdel\s)(\d{2}|\d{4}))?(\s|$|\,))" + \
                    r"(?!(gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic))",
                    law,
                    re.IGNORECASE
                    )
    decr_num  = None
    decr_year = None
    if num:
        decr_num  = num.group(6)
        decr_year = num.group(9)
    return (decr_num if decr_num else None, str(decr_year[-2:]) if decr_year else None)



def find_cass_sez(law):
    """
    Ritorna la sezione associata alla cassazione, un numero o un per sezioni unite
    """
    if re.search('ss\.\s?uu\.', law, re.IGNORECASE):
        sez = 'SEZ. UN.'
    else:
        sez = re.search('((sez\.)|(sezione))\s?([IVX]+|\d+|un)', law, re.IGNORECASE)
        sez = sez.group(4) if sez else 'NoSez'
    return sez



def find_cass_type(law):
    """
    Ritorna una stringa contenente il tipo di cassazione (penale o civile o nd)
    """
    if re.search('pen', law, re.IGNORECASE):
        cass_type = "PEN."
    elif re.search('civ', law, re.IGNORECASE):
        cass_type = "CIV."
    else:
        cass_type='GEN.'
    return cass_type




def find_numbers_in_decr(law):
    """
    Torna il numero di un decreto, e se nella forma nn/yyyy torna anche l'eventuale anno in formato yy
    """
    num = re.search(r"(((d\.?m\.\s)|(decr(\.|eto)?(\s)?min(\.|isteriale)?\s))|(((lgs\.?)|legislativo|l\.)\s)|((n(\.|\°)?|nr(\.|\°)?|numero)\s?))" + \
                    r"((\d+)((\/|\\\\|\sdel\s)(\d{2}|\d{4}))?(\s|$|\,))(?!(gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic))",
                    law,
                    re.IGNORECASE
                    )
    #print(num.group(10))
    decr_num  = None
    decr_year = None
    if num:
        decr_num  = num.group(16)
        decr_year = num.group(19)
    return (decr_num if decr_num else None, str(decr_year[-2:]) if decr_year else None)




def find_years(text):
    """
    Trova la stringa corrispondente ad una data e torna l'anno nel formato yy
    """
    date = re.search(r"(([0123]?\d)" + \
                     r"(\s|\/|\-|\.)([01]\d|\d|gen(naio)?|feb(braio)?|mar(zo)?|apr(ile)?|mag(gio)?|giu(gno)?|lug(lio)?|ago(sto)?|set(tembre)?|ott(obre)?|nov(embre)?|dic(embre)?)" + \
                     r"\.?(\s|\/|-|\.)\'?(\d\d\d\d|\'?\d\d))",
                     text,
                     re.IGNORECASE
                    )
    #print(date)
    if date:
        year = date.group(18)
        return year[-2:]
    else:
        return None