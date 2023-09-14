class Filename: #file
    def __init__(self, name, type_):
        self.name  = name    #nome del documento
        self.type_ = type_   #tipo di documento (ordinanza, sentenza,ecc)
    def export(self):
        return (
            {
                "name" : self.name,
                "type" : self.type_
            })
    #def print_class(self):
    #    print(f'name: {self.name}, type_: {self.type_}')

class Articolo: #Articoli del codice
    def __init__(self, type_, num, num_no_attr, attr, comma, lett, raw_s):
        self.type_  = type_    #tipologia di articolo (cp, cpp, cc...)
        self.num    = num     #codice dell'articolo
        self.num_no_attr = num_no_attr
        self.attr   = attr
        self.comma  = comma    #comma
        self.lett   = lett     #lettera del comma
        self.raw_s  = raw_s    #stringa grezza del dataset
    def export(self):
        return (
            {
                "type" : self.type_,
                "num" : self.num,
                "num_no_attr" : self.num_no_attr,
                "attr" : self.attr,
                "comma" : self.comma,
                "lett" : self.lett
            })
    #def print_class(self):
    #    print(f'type: {self.type_}, num: {self.num}, comma: {self.comma}, lett: {self.lett}, raw_string: {self.raw_s}')

class Cassazione: #Sentenze della cassazione
    def __init__(self, type_, sez, year, date, num, raw_s):
        self.type_     = type_    #tipo di cassazione (penale, civile...)
        self.sez       = sez      #sezione
        self.year      = year
        self.date      = date     #data della sentenza
        self.num       = num      #numero della sentenza
        self.raw_s     = raw_s

    def export(self):
        return (
            {
                "type" : self.type_,
                "sez" : self.sez,
                "year" : self.year,
                "date" : self.date,
                "num" : self.num
            })
    #def print_class(self):
    #    print(f'type: {self.type_}, sez: {self.sez}, year: {self.year} date: {self.date}, num: {self.num}, raw_string: {self.raw_s}')

class Decreto: # Decreti legge, legislativi, ministeriali, ecc...
    def __init__(self, type_, art, num, art_no_attr, attr, year, date, comma, lett, raw_s):
        self.type_     = type_      #tipo di decreto(DPR, DLGS...)
        self.art       = art        #articolo del decreto
        self.num       = num        #numero del decreto
        self.art_no_attr = art_no_attr  # senza bis, ter, ecc
        self.attr      = attr,      #bis,ter, ecc
        self.year      = year       #anno
        self.date      = date       #data completa(qualora riportata)
        self.comma     = comma
        self.lett      = lett
        self.raw_s     = raw_s

    def export(self):
        return (
            {
                "type" : self.type_,
                "art" : self.art,
                "num" : self.num,
                "art_no_attr" : self.art_no_attr,
                "attr" : self.attr,
                "year" : self.year,
                "comma" : self.comma,
                "lett" : self.lett,
                "date" : self.date
            })
    #def print_class(self):
    #    print(f'type: {self.type_}, art: {self.art}, num: {self.num}, year: {self.year}, date: {self.date}, comma: {self.comma}, lett: {self.lett}, raw_string: {self.raw_s}')

class Id_proc:
    def __init__(self, code, type_, mod, date, raw_s):
        self.code   = code
        self.type_  = type_   #tipo (rgnr, rg GIP,..)
        self.mod    = mod     #eventuale mod associato all'rg
        self.date   = date
        self.raw_s  = raw_s
    def export(self):
        return (
            {
                "code" : self.code,
                "type" : self.type_,
                "mod" : self.mod,
                "date" : self.date
            })
    #def print_class(self):
    #    print(f'code: {self.code}, type: {self.type_}, date: {self.date}, mod: {self.mod}, raw_string: {self.raw_s}')

class Person:
    def __init__(self, name, raw_s):
        self.name  = name    #nome
        self.raw_s = raw_s
    def export(self):
        return ({"name" : self.name})
    #def print_class(self):
    #    print(f'name: {self.name}, raw_string: {self.raw_s}')

class Location:
    def __init__(self, name, raw_s):
        self.name  = name    #nome
        self.raw_s = raw_s
    def export(self):
        return ({"name" : self.name})
    #def print_class(self):
    #    print(f'name: {self.name}, raw_string: {self.raw_s}')

class Organization:
    def __init__(self, name, raw_s):
        self.name  = name    #nome
        self.raw_s = raw_s
    def export(self):
        return ({"name" : self.name})
    #def print_class(self):
    #    print(f'name: {self.name}, raw_string: {self.raw_s}')
