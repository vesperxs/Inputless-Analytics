# -*- coding: utf-8 -*-

import re



"""
TO-DO: gestire i nomi di file con keyword multiple
        SOLUZ 1: se il database lo consente type_ può diventare una lista in cui appendere ogni tipo trovato
        SOLUZ 2: stabilire un ordine di priorità in modo da estrarre solo la keyword più rilevante
"""
def categorize_file(file):
    """[Determina il tipo di documento]

    Args:
        file ([str]): [nome del documento]

    Raises:
        IOError: [se la lunghezza del documento e' < 4 caratteri]

    Returns:
        [str]: [Tipo di documento, "Altro" se non e' nell'elenco]
    """

    if re.search(r'appell(o|i)', file, re.IGNORECASE):
        type_ = "Appello"
    elif re.search(r'sentenz(a|e)', file, re.IGNORECASE):
        type_ = "Sentenza"
    elif re.search(r'mem(\.|ori(a|e))', file, re.IGNORECASE):
        type_ = "Memoria"
    elif re.search(r'informativ(a|e)', file, re.IGNORECASE):
        type_ = "Informativa"
    elif re.search(r'parcell(a|e)', file, re.IGNORECASE):
        type_ = "Parcella"
    elif re.search(r'parere', file, re.IGNORECASE):
        type_ = "Parere"
    elif re.search(r'rinunc(ia|e)', file, re.IGNORECASE):
        type_ = "Rinuncia"
    elif re.search(r'(?<![a-z])not(a|e)', file, re.IGNORECASE):
        type_ = "Nota"
    elif re.search(r'opposizion(e|i)', file, re.IGNORECASE):
        type_ = "Opposizione"
    elif re.search(r'(?<![a-z])att(o|i)', file, re.IGNORECASE):
        type_ = "Atto"
    elif re.search(r'accertamento', file, re.IGNORECASE):
        type_ = "Accertamento"
    elif re.search(r'ud(\.|ienza)', file, re.IGNORECASE):
        type_ = "Udienza"
    elif re.search(r'consulenza', file, re.IGNORECASE):
        type_ = "Consulenza"
    elif re.search(r'relaz(\.|ion(e|i))', file, re.IGNORECASE):
        type_ = "Relazione"
    elif re.search(r'lett(\.|er(a|e))', file, re.IGNORECASE):
        type_ = "Lettera"
    elif re.search(r'sollecito', file, re.IGNORECASE):
        type_ = "Sollecito"
    elif re.search(r'(?<![a-z])ist(\.|anza)', file, re.IGNORECASE):
        type_ = "Istanza"
    elif re.search(r'interrogatorio', file, re.IGNORECASE):
        type_ = "Interrogatorio"
    elif re.search(r'delega', file, re.IGNORECASE):
        type_ = "Delega"
    elif re.search(r'(?<![a-z])legge', file, re.IGNORECASE):
        type_ = "Legge"
    elif re.search(r'decr(\.|et(o|i))', file, re.IGNORECASE):
        type_ = "Decreto"
    elif re.search(r'giudizio', file, re.IGNORECASE):
        type_ = "Giudizio"
    elif re.search(r'imputaz(\.|(ione))', file, re.IGNORECASE):
        type_ = "Imputazione"
    elif re.search(r'regolamento', file, re.IGNORECASE):
        type_ = "Regolamento"
    elif re.search(r'dich(\.|iarazione)', file, re.IGNORECASE):
        type_ = "Dichiarazione"
    elif re.search(r'proc(\.|edimento)', file, re.IGNORECASE):
        type_ = "Procedimento"
    elif re.search(r'bozza', file, re.IGNORECASE):
        type_ = "Bozza"
    elif re.search(r'(verb(\.|ale))|(vrb\.)', file, re.IGNORECASE):
        type_ = "Verbale"
    elif re.search(r'indagin', file, re.IGNORECASE):
        type_ = "Indagine"
    elif re.search(r'denuncia', file, re.IGNORECASE):
        type_ = "Denuncia"
    elif re.search(r'perizia', file, re.IGNORECASE):
        type_ = "Perizia"
    elif re.search(r'ordinanza', file, re.IGNORECASE):
        type_ = "Ordinanza"
    elif re.search(r'appunti', file, re.IGNORECASE):
        type_ = "Appunti"
    elif re.search(r'procur(a|e)', file, re.IGNORECASE):
        type_ = "Procura"
    elif re.search(r'quietanza', file, re.IGNORECASE):
        type_ = "Quietanza"
    elif re.search(r'relata(\s|_)di(\s|_)notifica', file, re.IGNORECASE):
        type_ = "Relata di notifica"
    elif re.search(r'revoca', file, re.IGNORECASE):
        type_ = "Revoca"
    elif re.search(r'diffida', file, re.IGNORECASE):
        type_ = "Diffida"
    elif re.search(r'risarcimento', file, re.IGNORECASE):
        type_ = "Risarcimento"
    elif re.search(r'riscontro', file, re.IGNORECASE):
        type_ = "Riscontro"
    elif re.search(r'precisazioni', file, re.IGNORECASE):
        type_ = "Precisazioni"
    elif re.search(r'pignoramento', file, re.IGNORECASE):
        type_ = "Pignoramento"
    elif re.search(r'contratto', file, re.IGNORECASE):
        type_ = "Contratto"
    elif re.search(r'rich(\.|iesta)', file, re.IGNORECASE):
        type_ = "Richiesta"
    elif re.search(r'ricorso', file, re.IGNORECASE):
        type_ = "Ricorso"
    elif re.search(r'des(\.|igna(zione)?)(\.|\s|_)?sost', file, re.IGNORECASE):
        type_ = "Des. Sost."
    elif re.search(r'concl(\.|usion)', file, re.IGNORECASE):
        type_ = "Conclusione"
    elif re.search(r'nomina', file, re.IGNORECASE):
        type_ = "Nomina"
    elif re.search(r'(?<![a-z])all(\.|egato)', file, re.IGNORECASE):
        type_ = "Allegato"
    elif re.search(r'(?<![a-z])cit(\.|azion)', file, re.IGNORECASE):
        type_ = "Citazione"
    elif re.search(r'stenotipia', file, re.IGNORECASE):
        type_ = "Stenotipia"
    elif re.search(r'autorizzazione', file, re.IGNORECASE):
        type_ = "Autorizzazione"
    elif re.search(r'capitolato', file, re.IGNORECASE):
        type_ = "Capitolato"
    elif re.search(r'(?<![a-z])prev(entivo)?', file, re.IGNORECASE):
        type_ = "Preventivo"
    elif re.search(r'querel', file, re.IGNORECASE):
        type_ = "Querela"
    elif re.search(r'fatt(\.|ura)', file, re.IGNORECASE):
        type_ = "Fattura"
    elif re.search(r'proroga', file, re.IGNORECASE):
        type_ = "Proroga"
    elif len(file) < 4:
        raise IOError(f"Expected filenames longer then 4 char")
    else:
        type_ = "Altro"
    return type_


"""
TODO: essere sicuri di coprire ogni tipo, altrimenti crerare una funzione
      che controlla se la stringa è da scartare o meno
"""
def categorize_idproc(proc_id):
    """Trova il tipo dell ID_PROC

    Args:
        proc_id ([str]): [Id del processo]

    Returns:
        [str]: [rg type, "NaN" se non e' nell'elenco]
    """
    if re.search(r'(r\.?\s?g\.?\s?(p\.?\s?)?n\.?\s?(r\.?)?)', proc_id, re.IGNORECASE):
        type_ = "RGNR"
    elif re.search('procedimento\spenale', proc_id, re.IGNORECASE):
        type_ = "PENAL PROC"
    elif re.search('(g\.?\s?i\.?\s?p\.?)', proc_id, re.IGNORECASE):
        type_ = "RG-GIP"
    elif re.search('(g\.?\s?u\.?\s?p\.?)', proc_id, re.IGNORECASE):
        type_ = "RG-GUP"
    elif re.search('app', proc_id, re.IGNORECASE):
        type_ = "RG-APP"
    elif re.search('(d\.?\s?i\.?\s?b\.?)', proc_id, re.IGNORECASE):
        type_ = "RG-DIB"
    elif re.search('(((reg\.?\s?)|(r\.?\s?g))\.?\s?(gen)?\.?\s?(sent))', proc_id, re.IGNORECASE):
        type_ = "REG.SENT."
    elif re.search('p\.?m', proc_id, re.IGNORECASE):
        type_ = "RG-PM"
    elif re.search('(r\.?\s?g)', proc_id, re.IGNORECASE):
        type_ = "RG"
    else:
        type_ = 'NaN'
    return type_


def categorize_law(law):
    """Trova il tipo delle entità riferite a leggi o articoli


    Args:
        law ([str]): [articolo o legge]

    Returns:
        [str]: [law type, NaN se non e' nell'elenco]
    """
    if re.search('(c\.?p(?!(\.?(p|c))))|(cod(\.|ice)?(\s)?pen(\.|ale)?)', law, re.IGNORECASE):
        type_ = ('C.P.')
    elif re.search('(c\.?c)|(cod(\.|ice)?(\s)?civ(\.|ile)?)', law, re.IGNORECASE):
        type_ = 'C.C.'
    elif re.search('(c\.?p\.?p)|(proc(\.|edura)?(\s)?pen(\.|ale)?)', law, re.IGNORECASE):
        type_ = 'C.P.P.'
    elif re.search('(c\.?p\.?c)|(proc(\.|edura)?(\s)?civ(\.|ile)?)', law, re.IGNORECASE):
        type_ = 'C.P.C.'
    elif re.search('(c\.?d\.?s)|(cod(\.|ice)?(\s)della(\s)strada)', law, re.IGNORECASE):
        type_ = 'C.D.S.'
    elif re.search('(c\.?n)|(cod(\.|ice)?(\s)nav(\.|ale))', law, re.IGNORECASE):
        type_ = 'C.N.'
    elif re.search('(d\.p\.r)|(pres(/.|idente)?\sdella\srepubblica)', law, re.IGNORECASE):
        type_ = 'D.P.R.'
    elif re.search('(d\.p\.c\.m)|(pres(/.|idente)?\sdel\scons(/.|iglio)?)', law, re.IGNORECASE):
        type_ = 'D.P.C.M.'
    elif re.search('(d\.l\.vo)|(d\.?l\.?g\.?s)|(decr(\.|eto)?(\s)?legislativo)', law, re.IGNORECASE):
        type_ = 'DLGS'
    elif re.search('(d\.l(g)?\.)|(decr(\.|eto)?(\s|\-)?legge)', law, re.IGNORECASE):
        type_ = 'D.L.'
    elif re.search('(d\.?m)|(decr(\.|eto)?(\s)?min(\.|isteriale)?)', law, re.IGNORECASE):
        type_ = 'D.M.'
    elif re.search('(?<!decreto)(\slegge\s)', law, re.IGNORECASE):
        type_ = 'LEGGE'
    elif re.search('corte\scostituzionale', law, re.IGNORECASE):
        type_ = 'CORTE COSTITUZIONALE'
    elif re.search('(\scost\.?)|(costituzione)', law, re.IGNORECASE):
        type_ = 'COSTITUZIONE'
    elif re.search('cass\.?(azione)?\s', law, re.IGNORECASE):
        type_ = 'CASSAZIONE'
    elif re.search('\ssentenza\s', law, re.IGNORECASE):
        type_ = 'SENTENZA'
    elif re.search('T\.P', law, re.IGNORECASE):
        type_ = 'T.P.'
    elif re.search('(r\.d\.)|(regio\sdecreto)', law, re.IGNORECASE):
        type_ = 'REGIO DECRETO'
    elif re.search('(l\.f\.)|(legge\sfall(\.|imentare)?)', law, re.IGNORECASE):
        type_ = 'LEGGE FALLIMENTARE'
    elif re.search('(d\.p\.g\.r)|(giunta\sreg(\.|ionale)?)', law, re.IGNORECASE):
        type_ = 'D.P.G.R.'
    elif re.search('(l\.R\.)|(legge\sreg(\.|ionale)?)', law, re.IGNORECASE):
        type_ = 'LEGGE REGIONALE'
    elif re.search('cod(\.|ice)\s?deontologico', law, re.IGNORECASE):
        type_ = 'CODICE DEONTOLOGICO'
    elif re.search('(t\.u\.)|(testo\sunico)', law, re.IGNORECASE):
        type_ = 'TESTO UNICO'
    elif re.search('((o\.)|(ord(\.|inamento)?))\s?((p\.)|(pen(\.|itenziario)?))', law, re.IGNORECASE):
        type_ = 'ORDINAMENTO PENITENZIARIO'
    else:
        type_ = 'NaN'
    return type_