from spacy.tokens.doc import Doc  # type: ignore

from django.conf import settings
from .offsets import Case
import json
# arangodb

def clean_data():
    pass


def jsonize_data(case: Case, person, law, org, judge, id_proc, loc):
    doc = case.case_id.split('/')[-1]
    d = {
        # 'doc': processing_filename(doc),
        'doc': doc,
        'person': person,
        'id_proc': id_proc,
        'law': law,
        'org': org,
        'judge': judge,
        'loc': loc
        }
    # call db
    #with open("temp/test.json", 'a') as f:
    #    f.write(json.dumps(d))

    #save_to_arango(d)

    return d


def build_dataframe(case: Case):
    nlp = settings.MODEL
    # get entities from spacy_doc
    spacy_doc = nlp(case.extracted_text)
    ents = [(ent.text, ent.label_) for ent in spacy_doc.ents]
    cleaned = list(set(ents))

    person = []
    law = []
    org = []
    judge = []
    id_proc = []
    loc = []
    # unknown = [procs_list = ]

    for idx in cleaned:
        if idx[1] == 'PERSON':
            person.append(idx[0])
        elif idx[1] == 'LAW':
            law.append(idx[0])
        # elif idx[1] == 'ORG':
        #    org.append(idx[0])
        elif idx[1] == 'ID_PROC':
            id_proc.append(idx[0])
        #elif idx[1] == 'JUDGE':
        #    judge.append(idx[0])
        elif idx[1] == 'LOC':
            loc.append(idx[0])
        # elif idx[1] == 'UNKNOWN':
        #    unknown.append(idx[0])

    ret = jsonize_data(case, person, law, org, judge, id_proc, loc)
    return ret
    # processing(case.case_id,
    #           law,
    #           id_proc)
    # for elem in id_procs_list:
    #    print(elem.print_class())
