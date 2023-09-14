import os
import subprocess 

def load_haystack_reindexer():
    path = os.getcwd()
    process = subprocess.Popen(['./manage.py rebuild_index --noinput'], shell=True,cwd=path) 
    stdout,stderr = process.communicate()
    return process.poll()


    
