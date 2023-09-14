from django.shortcuts import render
from django.views.generic import TemplateView
from .tasks import multiscope_query, articles_query, rgnr_query, decr_query, cass_query, blacklist
#from .query_dispatcher import multiscope_query, articles_query, rgnr_query, decr_query, cass_query, blacklist
from .query_operations import jsonize_data, create_table

from django.contrib.auth.decorators import login_required
from .forms import MultiscopeForm, ProcIdForm, DecrIdForm, ArtIdForm, CassIdForm
import csv
import logging
logger = logging.getLogger(__name__)


@login_required
def multiscope_views(request):
    
    query_dict = dict()
    res_list = list() 

    if request.method == "POST":
        details = MultiscopeForm(request.POST or None)
        
        if details.is_valid():
            
            input_query = details['input_query'].value()
            input_selection = details['input_selection'].value()
            input_file_type = details['file_type'].value()
            input_deep = details['input_deep'].value()
            
            query_dict['query'] = input_query
            query_dict['type'] = input_selection
            query_dict['file_type'] = input_file_type
            query_dict['deep'] = input_deep

            # initialize db connection
            
            if query_dict['type'] in ['PERSON','FILENAME','LOCATION']:
                
                task_result = multiscope_query.delay(query_dict)
                res_list = task_result.get() 

            if res_list:
                data = jsonize_data(res_list)
                return render(request, 'graph.html', {'data_graph':data})
            else:
                return render(request, 'error-505.html', {})
            
        else:
        
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "error-404.html", {'form':details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = MultiscopeForm(None)  
        return render(request, 'graph.html', {'form':form})


@login_required
def procid_views(request):
    
    query_dict = dict()
    res_list = list() 
    
    if request.method == "POST":
        details = ProcIdForm(request.POST or None)
        
        if details.is_valid():
            
            code_input = details['code_input'].value()
            date_input = details['date_input'].value()
            mode_input = details['mode_input'].value()
            input_selection = details['input_selection'].value()
            input_deep = details['input_deep'].value()

            query_dict['query'] = code_input
            query_dict['date'] = date_input 
            query_dict['mod']  = mode_input if len(mode_input) > 0 else None
            query_dict['type'] = input_selection
            query_dict['deep'] = input_deep 

            task_result = rgnr_query.delay(query_dict)
            res_list = task_result.get()

            if res_list:
                data = jsonize_data(res_list)
                return render(request, 'graph.html', {'data_graph':data})
            else:
                return render(request, 'error-505.html', {})

        else:
        
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "error-404.html", {'form':details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = ProcIdForm(None)  
        return render(request, 'graph.html', {'form':form})


@login_required
def decrid_views(request):
    
    query_dict = dict()
    res_list = list()
    
    if request.method == "POST":
        
        details = DecrIdForm(request.POST or None)
        #print(details)
        
        if details.is_valid():

            decrid_art = details['decrid_art'].value()
            decrid_opt = details['decrid_opt'].value()
            decrid_comma = details['decrid_comma'].value()
            decrid_lett = details['decrid_lett'].value()
            decrid_num = details['decrid_num'].value()
            decrid_year = details['decrid_year'].value()
            input_selection = details['input_selection'].value()
            input_deep = details['input_deep'].value()

            query_dict['art'] = decrid_art
            query_dict['opt'] = decrid_opt
            query_dict['comma'] = decrid_comma if len(decrid_comma) > 0 else None
            query_dict['lett']  = decrid_lett if len(decrid_lett) > 0 else None
            query_dict['num'] = decrid_num if len(decrid_num) > 0 else None
            query_dict['year'] = decrid_year if len(decrid_year) > 0 else None
            query_dict['type'] = input_selection
            query_dict['deep'] = input_deep 

            task_result = decr_query.delay(query_dict)
            res_list = task_result.get()


            if res_list:
                data = jsonize_data(res_list)
                return render(request, 'graph.html', {'data_graph':data})
            else:
                #specify the error status code 
                return render(request, 'error-505.html', {})
            
        else:
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "error-404.html", {'form':details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = DecrIdForm(None)  
        return render(request, 'graph.html', {'form':form})



@login_required
def art_views(request):
    query_dict = dict()
    res_list = list()
    
    if request.method == "POST":
        
        details = ArtIdForm(request.POST or None)
        #print(details)
        
        if details.is_valid():

            art_num = details['art_num'].value()
            art_opt = details['art_opt'].value()
            art_comma = details['art_comma'].value()
            art_lett = details['art_lett'].value()
            input_selection = details['input_selection'].value()
            input_deep = details['input_deep'].value()

            
            query_dict['art'] = art_num
            query_dict['opt'] = art_opt
            query_dict['comma'] = art_comma if len(art_comma) > 0 else None
            query_dict['lett'] = art_lett if len(art_comma) > 0 else None
            query_dict['type'] = input_selection
            query_dict['deep'] = input_deep 

            task_result = articles_query.delay(query_dict)
            res_list = task_result.get()
            
            

            if res_list:
                data = jsonize_data(res_list)
                return render(request, 'graph.html', {'data_graph':data})
            else:
                #specify the error status code 
                return render(request, 'error-505.html', {})
        else:
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "error-404.html", {'form':details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = ArtIdForm(None)  
        return render(request, 'graph.html', {'form':form})


@login_required
def cass_views(request):
    query_dict = dict()
    res_list = list()
    
    if request.method == "POST":
        details = CassIdForm(request.POST or None)
        #print(details)
        
        if details.is_valid():

            cass_num = details['cass_num'].value()
            cass_year = details['cass_year'].value()
            cass_sez = details['cass_sez'].value()
            cass_type = details['cass_type'].value()
            input_deep = details['input_deep'].value()

            query_dict['num'] = cass_num
            query_dict['year'] = cass_year
            query_dict['sez'] = cass_sez
            query_dict['type'] = cass_type
            query_dict['deep'] = input_deep 

            #print(query_dict)
            task_result = cass_query.delay(query_dict)
            res_list = task_result.get()

            if res_list:
                data = jsonize_data(res_list)
                return render(request, 'graph.html', {'data_graph':data})
            else:
                #specify the error status code 
                return render(request, 'error-505.html', {})

        else:
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "error-404.html", {'form':details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = CassIdForm(None)  
        return render(request, 'graph.html', {'form':form})


@login_required
def table_views(request):

    def id_to_label(id,data):
        res = None
        for el in data["root"]["nodes"]:
            if el['id'] == id:
                res = el["label"]
        return res

    query_dict = dict()
    res_list = list() 

    if request.method == "POST":
        input_query = request.POST.get('q')
        input_selection = request.POST.get('selection_field')

        if len(input_query) <= 30:
            query_dict['file_type'] = 'None'
            query_dict['query'] = str(input_query) 

            query_dict['deep'] = 1 

        #Assign default value if search_options is empty
        else:
            return render(request, 'error-505.html', {})


        query_dict['type'] = input_selection
        task_result = multiscope_query.delay(query_dict)
        res_list = task_result.get()

    if res_list:
        print('in table result')
        data = jsonize_data(res_list)
        d = dict()
        for k, v in data.items():
            if 'FILENAME' in k:
                label = id_to_label(k,data)
                #d[k] = dict()
                #d[k]['FILENAME']=[],
                d[k] = {
                    'FILENAME':label,
                    'PERSON':[],
                    'IDPROC':[],
                    'ARTICOLI':[],
                    'LOCATION':[]
                }
                for i in v['nodes']:
                    #if i['type'] == 'FILENAME':
                    #    d['FILENAME'].append(i['label'].replace('\n',' '))
                    if i['type'] == 'PERSON':
                        d[k]['PERSON'].append(i['label'].replace('\n',' '))

                    elif i['type'] == 'IDPROC':
                        d[k]['IDPROC'].append(i['label'].replace('\n',' '))

                    elif i['type'] == 'ARTICOLI':
                        d[k]['ARTICOLI'].append(i['label'].replace('\n',' '))

                    elif i['type'] == 'LOCATION':
                        d[k]['LOCATION'].append(i['label'].replace('\n',' '))

        return render(request, 'table.html', {'data_table':d})
    else:
        return render(request, 'error-508.html', {})

    return render(request, 'error-404.html', {})



@login_required
def filter_results(request):
    """ 
    take an input file (csv) filled with strings, then load them into arango
    """
    to_return = dict()
    if request.method == "post":
        csv_file = request.files['file_uploaded']

        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            return render(request, 'error-404.html', {})

        content_to_read = csv_file.read().decode('utf-8').split('\n')
        to_return['data'] = content_to_read

        task_result = blacklist.delay(to_return['data'])
    else:
        return render(request, 'error-404.html')

    
    return render(request, 'filters.html', {'data': to_return['data']})
        
            
