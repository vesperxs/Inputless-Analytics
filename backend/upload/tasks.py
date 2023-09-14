from celery.decorators import task
from .parser import ParseData
from .offsets import Paragraph, Case
from .entity_extractor import build_dataframe
from .DB_operations import create_graph, initialize_db
from .processing_func import process_all
import time
from celery_progress.backend import ProgressRecorder
import os
from .models import DocumentDataStore
from .models import ChartInfo, ChartFolderQuotas, ChartsNLP
from django.db import connection
from customers.models import Client
from .stats_extraction import extract_for_stats
import json



@task(name='init_extraction_task', bind=True)
def init_extraction_task(self, path):
    #print(connection.schema_name)

    progress_recorder = ProgressRecorder(self)
    result = 0
    db, coll_dict = initialize_db(connection.schema_name)
    
    for i in range(1):
        time.sleep(0.2)
        Case: Paragraph = ParseData(path).filter_by_types()
        
        if Case:
            ret = build_dataframe(Case)
            #print(ret)
            #save extracted_text into db for future indexing
            to_save = DocumentDataStore(title=Case.case_id,
                                        extracted_text=Case.extracted_text)

            to_save.save()
            process_all(db, coll_dict, ret)
        result += i
        progress_recorder.set_progress(i + 1,1)
    #create_graph(db)
    return result


@task(name='init_analyze_task', bind=True)
def init_analyze_task(self):

    db, _ = initialize_db(connection.schema_name) 
    #print(db)
    create_graph(db)
    tot_d = extract_for_stats(db)

    save_chart_nlp = ChartsNLP(nlp_data=tot_d)
    save_chart_nlp.save()
    pass

@task(name='init_save_chart_data', bind=True)
def init_save_chart_data(self, n_file_uploaded):
    file_uploaded = []
    file_uploaded.append(n_file_uploaded)
    #print(file_uploaded)
    save_chart_data = ChartInfo(numbers_of_file_uploaded = n_file_uploaded)
    save_chart_data.save()

@task(name='init_calculate_folder_quotas', bind=True)
def init_calculate_folder_quotas(self, folder_path):
    
    folder_list = folder_path.split('/')[:-1]
    folder_path = "/".join(folder_list)
    size = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    # display size
    #print("Folder size: " + str(size))
    final_size = ChartFolderQuotas(folder_size=str(size))
    final_size.save()
    

    

    
