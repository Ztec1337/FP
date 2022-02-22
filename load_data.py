import numpy as np
import pandas as pd
import requests
import io
import sys

from google.colab import auth
auth.authenticate_user() 

def downloadfolder(url):
    folder_id = url.split('/')[-1].split('?')[0]
    from googleapiclient.discovery import build
    gdrive = build('drive', 'v3').files()
    res = gdrive.list(q="'%s' in parents" % folder_id).execute()
    itemlist =  [[f['id'],f['name']] for f in res['files']]
    print('Adding new variables: ')
    downloadlink = 'https://drive.google.com/uc?id='
    for item in itemlist:
        link = downloadlink+item[0]
        response = requests.get(link)
        response.raise_for_status()
        format = item[1].split('.')[-1]
        
        if format == 'npy':
            temp = np.load(io.BytesIO(response.content),allow_pickle=True)
            vars(sys.modules[__name__])[item[1].split('.')[0]] = temp
        if format == 'csv':
            temp = pd.read_csv(link)
            vars(sys.modules[__name__])[item[1].split('.')[0]] = temp

        print(item,'name:',item[1].split('.')[0])
        print(link)
         
