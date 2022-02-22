import numpy as np
import requests
import io

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
        if item[1].split('.')[-1] == 'npy':
            link = downloadlink+item[0]
            response = requests.get(link)
            response.raise_for_status()
            temp = np.load(io.BytesIO(response.content),allow_pickle=True)
            vars()[item[1].split('.')[0]] = temp
            print(item,'name:',item[1].split('.')[0])
            print(link)
