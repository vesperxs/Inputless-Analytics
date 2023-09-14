# -*- coding: utf-8 -*-

import re

def find_person_name(pers_str):
    #(([A-Z][a-z]+\s){1,2}(L(A|a)\s|L\'\s?|D(I|i)\s|D(E|e)\s|D(ELLA|ella)\s|D(ALLA|alla)\s|D(A|a)\s|D(EL|el)\s|D'\s?)?([A-Z]([A-Za-z]+))|((L(A|a)\s|L\'\s?|D(I|i)\s|D(E|e)\s|D(ELLA|ella)\s|D(ALLA|alla)\s|D(A|a)\s|D(EL|el)\s|D'\s?)?([A-Z][A-Za-z]+)(\s[A-Z][a-z]+)((\s[A-Z][a-z]+)?)))|(([A-Z]\.\s*(LA\s|L\'\s?|DI\s|DE\s|DELLA\s|DALLA\s|DA\s|DEL\s|D'\s?)?[A-Z][A-Z]+)|((LA\s|L\'\s?|DI\s|DE\s|DELLA\s|DALLA\s|DA\s|DEL\s|D'\s?)?[A-Z][A-Z]+\s[A-Z]\.))
    #name = re.search(r"((([A-Z][a-z]+\s){1,2}(LA\s|L\'\s?|DI\s|DE\s|DELLA\s|DALLA\s|DA\s|DEL\s|D'\s?)?([A-Z][A-Z]+))|((LA\s|L\'\s?|DI\s|DE\s|DELLA\s|DALLA\s|DA\s|DEL\s|D'\s?)?" + \
    #                 r"([A-Z][A-Z]+)(\s[A-Z][a-z]+)((\s[A-Z][a-z]+)?)))|(([A-Z]\.\s*(LA\s|L\'\s?|DI\s|DE\s|DELLA\s|DALLA\s|DA\s|DEL\s|D'\s?)?[A-Z][A-Z]+)|" + \
    #                 r"((LA\s|L\'\s?|DI\s|DE\s|DELLA\s|DALLA\s|DA\s|DEL\s|D'\s?)?[A-Z][A-Z]+\s[A-Z]\.))",
    #                 pers_str
    #                 )
    name = re.search(r"([A-Z][a-z]+ ([A-Z][a-z]+ )?((LA|la|La) |((L|l)\' ?)|(DI|di|Di) |(DE|de|De) |(DELLA|della|Della) |(DALLA|dalla|Dalla) |(DA|da|Da) |(DEL|del|Del) |(D|d)\' ?)?([A-Z][A-Za-z]+))|" + \
                     r"(((LA|la|La) |((L|l)\' ?)|(DI|di|Di) |(DE|de|De) |(DELLA|della|Della) |(DALLA|dalla|Dalla) |(DA|da|Da) |(DEL|del|Del) |(D|d)\' ?)?([A-Z][A-Za-z]+) ([A-Z][a-z]+( [A-Z][a-z]+)?))", \
                     pers_str)

    return name.group() if name else None

def check_loc(loc_str):
    pass


def check_org(org_str):
    pass

def filename_cleaning(file_name):
    file_name = re.sub('_',' ',file_name)
    return file_name