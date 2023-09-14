from django import forms
        
#Define the class of a form
class MultiscopeForm(forms.Form):
    INPUT_SELECTION = (
        ('PERSON', 'PERSON'),
        ('FILENAME','FILENAME'),
        ('LOCATION', 'LOCATION')
    )

    FILE_TYPE = (
        ('None','None'),
        ('Altro', 'Altro'),
        ('Accertamento', 'ACCERTAMENTO'),
        ('Allegato', 'ALLEGATO'),
        ('Appello', 'APPELLO'),
        ('Appunti', 'APPUNTI'),
        ('Atto', 'ATTO'),
        ('Autorizzazione', 'AUTORIZZAZIONE'),
        ('Bozza', 'BOZZA'),
        ('Capitolato', 'CAPITOLATO'),
        ('Citazione', 'CITAZIONE'),
        ('Conclusione', 'CONCLUSIONE'),
        ('Consulenza', 'CONSULENZA'),
        ('Contratto', 'CONTRATTO'),
        ('Dichiarazione', 'DICHIARAZIONE'),
        ('Decreto', 'DECRETO'),
        ('Delega', 'DELEGA'),
        ('Denuncia', 'DENUNCIA'),
        ('Des. Sost.', 'DES. SOST.'),
        ('Diffida', 'DIFFIDA'),
        ('Fattura', 'FATTURA'),
        ('Giudizio', 'GIUDIZIO'),
        ('Indagine', 'INDAGINE'),
        ('Informativa', 'INFORMATIVA'),
        ('Interrogatorio', 'INTERROGATORIO'),
        ('Imputazione', 'IMPUTAZIONE'),
        ('Istanza', 'ISTANZA'),
        ('Legge', 'LEGGE'),
        ('Lettera', 'LETTERA'),
        ('Memoria', 'MEMORIA'),
        ('Nomina', 'NOMINA'),
        ('Nota', 'NOTA'),
        ('Opposizione', 'OPPOSIZIONE'),
        ('Ordinanza', 'ORDINANZA'),
        ('Parcella', 'PARCELLA'),
        ('Parere', 'PARERE'),
        ('Perizia', 'PERIZIA'),
        ('Pignoramento', 'PIGNORAMENTO'),
        ('Precisazioni', 'PRECISAZIONI'),
        ('Preventivo', 'PREVENTIVO'),
        ('Procedimento', 'PROCEDIMENTO'),
        ('Procura', 'PROCURA'),
        ('Proroga', 'PROROGA'),
        ('Querela', 'QUERELA'),
        ('Quietanza', 'QUIETANZA'),
        ('Regolamento', 'REGOLAMENTO'),
        ('Relata di notifica', 'RELATA DI NOTIFICA'),
        ('Relazione', 'RELAZIONE'),
        ('Revoca', 'REVOCA'),
        ('Richiesta', 'RICHIESTA'),
        ('Ricorso', 'RICORSO'),
        ('Rinuncia', 'RINUNCIA'),
        ('Risarcimento', 'RISARCIMENTO'),
        ('Riscontro', 'RISCONTRO'),
        ('Sentenza', 'SENTENZA'),
        ('Sollecito', 'SOLLECITO'),
        ('Stenotipia', 'STENOTIPIA'),
        ('Udienza', 'UDIENZA'),
        ('Verbale', 'VERBALE')        
    )

    DEEP_LEVEL = (
        ('1', 'LEVEL ONE'),
        ('2', 'LEVEL TWO'),
        ('3', 'LEVEL TREE')
    )

    input_query     = forms.CharField(max_length = 20, required=True)
    input_selection = forms.ChoiceField(choices = INPUT_SELECTION, required=True)
    file_type       = forms.ChoiceField(choices = FILE_TYPE, required=False)
    input_deep      = forms.ChoiceField(choices = DEEP_LEVEL, required=True)

    #this function will be used for validation
    
    def clean(self):
        # data from the form is fetched using super function
        super(MultiscopeForm, self).clean()
        input_query = self.cleaned_data.get('input_query','')
        input_selection = self.cleaned_data.get('input_selection','')
        file_type = self.cleaned_data.get('file_type', '')
        input_deep = self.cleaned_data.get('input_deep','')


        # conditions to be met 
        if len(input_query) >= 20:
            self._errors['input_query'] = self.error_class([
                'Minimum 30 characters required'])
      
        #print(self.cleaned_data)
        # return any errors if found
        return self.cleaned_data




class ProcIdForm(forms.Form):
    
    INPUT_SELECTION = (
        ('RGNR', 'RGNR'),
        ('RG','RG'),
        ('RG-GIP', 'RG-GIP'),
        ('RG-PM', 'RG-PM'),
        ('RG-GUP', 'RG-GUP'),
        ('RG-DIB', 'RG-DIB'),
        ('RG-APP', 'RG-APP'),
        ('REG.SENT.', 'REG.SENT.'),
        )
    
    DEEP_LEVEL = (
        ('1', 'LEVEL ONE'),
        ('2', 'LEVEL TWO'),
        ('3', 'LEVEL TREE')
    )

   
    code_input = forms.IntegerField(required=True)
    date_input = forms.IntegerField(required=True)
    mode_input = forms.IntegerField(required=False) 

    input_selection = forms.ChoiceField(choices = INPUT_SELECTION, required=True)
    input_deep = forms.ChoiceField(choices = DEEP_LEVEL, required=True)

    #this function will be used for validation
    
    def clean(self):
        # data from the form is fetched using super function
        super(ProcIdForm, self).clean()
        code_input = self.cleaned_data.get('code_input')
        date_input = self.cleaned_data.get('date_input')
        mode_input = self.cleaned_data.get('mode_input')
        input_selection = self.cleaned_data.get('input_selection','')
        input_deep = self.cleaned_data.get('input_deep','')

        # conditions to be met 

        #print(self.cleaned_data)
        # return any errors if found
        return self.cleaned_data

class DecrIdForm(forms.Form):

    INPUT_SELECTION = (
        ('DLGS', 'DLGS'),
        ('D.P.R.', 'D.P.R.'),
        ('LEGGE', 'LEGGE'),
        ('D.L.', 'D.L.'),
        ('D.M', 'D.M.'),
    
    )
    
    DEEP_LEVEL = (
        ('1', 'LEVEL ONE'),
        ('2', 'LEVEL TWO'),
        ('3', 'LEVEL TREE')
    )

    NUM_OPT = (
        ('None',None),
        ('BIS', 'BIS'),
        ('TER','TER'),
        ('QUATER','QUATER'),
        ('QUINQUIES','QUINQUIES'),
        ('SEXIES','SEXIES'),
        ('SEPTIES','SEPTIES'),
        ('OCTIES','OCTIES'),
        ('NOVIES','NOVIES'),
        ('DECIES','DECIES'),
        ('DECIES','DECIES'),
        ('UNDECIES','UNDECIES'),
        ('DUODECIES','DUODECIES')
    )
    
    decrid_art = forms.IntegerField(required=False)
    decrid_opt = forms.ChoiceField(choices=NUM_OPT, required=True)
    decrid_comma = forms.IntegerField(required=False)
    decrid_lett = forms.CharField(required=False) 
    decrid_num  = forms.IntegerField(required=False)
    decrid_year = forms.IntegerField(required=False)
    input_selection = forms.ChoiceField(choices = INPUT_SELECTION, required=True)
    input_deep = forms.ChoiceField(choices = DEEP_LEVEL, required=True)

    def clean(self):
        super(DecrIdForm, self).clean()
        decrid_art = self.cleaned_data.get('decrid_art')
        decrid_opt = self.cleaned_data.get('decrid_opt')
        decrid_comma = self.cleaned_data.get('decrid_comma')
        decrid_lett = self.cleaned_data.get('decrid_lett')
        decrid_num = self.cleaned_data.get('decrid_num')
        decrid_year = self.cleaned_data.get('decrid_year')
        input_selection = self.cleaned_data.get('input_selection','')
        input_deep = self.cleaned_data.get('input_deep','')


        #add conditions to be met
        return self.cleaned_data


        
        
class ArtIdForm(forms.Form):

    INPUT_SELECTION = (
        ('C.C.', 'C.C.'),
        ('C.P.C.','C.P.C.'),
        ('C.P.', 'C.P.'),
        ('C.P.P.', 'C.P.P.'),
        ('C.A.', 'C.A.'),
        ('C.P.A.', 'C.P.A.'),
        ('C.D.S.', 'C.D.S.'),
        ('COSTITUZIONE', 'COSTITUZIONE'),
        ('CORTE COSTITUZIONALE', 'CORTE COSTITUZIONALE'),
        ('REGIO DECRETO', 'REGIO DECRETO'),
        ('LEGGE REGIONALE', 'LEGGE REGIONALE'),
        ('TESTO UNICO', 'TESTO UNICO'),
        )
    
    DEEP_LEVEL = (
        ('1', 'LEVEL ONE'),
        ('2', 'LEVEL TWO'),
        ('3', 'LEVEL TREE')
    )

    NUM_OPT = (
        ('None',None),
        ('BIS', 'BIS'),
        ('TER','TER'),
        ('QUATER','QUATER'),
        ('QUINQUIES','QUINQUIES'),
        ('SEXIES','SEXIES'),
        ('SEPTIES','SEPTIES'),
        ('OCTIES','OCTIES'),
        ('NOVIES','NOVIES'),
        ('DECIES','DECIES'),
        ('DECIES','DECIES'),
        ('UNDECIES','UNDECIES'),
        ('DUODECIES','DUODECIES')
    )
    

    art_num = forms.IntegerField(required=True)
    art_opt = forms.ChoiceField(choices=NUM_OPT, required=True)
    art_comma = forms.IntegerField(required=False)
    art_lett = forms.CharField(required=False)
    input_selection = forms.ChoiceField(choices = INPUT_SELECTION, required=True)
    input_deep = forms.ChoiceField(choices = DEEP_LEVEL, required=True)

    def clean(self):
        super(ArtIdForm, self).clean()
        art_num = self.cleaned_data.get('art_num')
        art_opt = self.cleaned_data.get('art_opt')
        art_comma = self.cleaned_data.get('art_comma')
        art_lett = self.cleaned_data.get('art_lett')
        input_selection = self.cleaned_data.get('input_selection','')
        input_deep = self.cleaned_data.get('input_deep','')


        #add conditions to be met
        return self.cleaned_data


class CassIdForm(forms.Form):

    SEZ = (
        ('NoSez', 'NoSez'),
        ('SEZ. UN.', 'SEZ. UN.'),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
        ('VI', 'VI'),
        ('VII', 'VII'),
        
    )
    
    DEEP_LEVEL = (
        ('1', 'LEVEL ONE'),
        ('2', 'LEVEL TWO'),
        ('3', 'LEVEL TREE')
    )

    TYPE = (
        ('GEN.','GEN.'),
        ('PEN.', 'PEN.'),
        ('CIV.','CIV'),
    )
    

    cass_num = forms.IntegerField(required=True)
    cass_year = forms.IntegerField(required=False)
    cass_sez = forms.ChoiceField(choices=SEZ, required=True)
    cass_type = forms.ChoiceField(choices = TYPE, required=True)
    input_deep = forms.ChoiceField(choices = DEEP_LEVEL, required=True)

    def clean(self):
        super(CassIdForm, self).clean()
        cass_num = self.cleaned_data.get('cass_num')
        cass_year = self.cleaned_data.get('cass_year')
        cass_sez = self.cleaned_data.get('cass_sez')
        cass_type = self.cleaned_data.get('cass_type')
        input_deep = self.cleaned_data.get('input_deep','')


        #add conditions to be met
        return self.cleaned_data
    
