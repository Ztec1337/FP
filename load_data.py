# loading the drive folder and listing all files for everyone to use
url = 'https://drive.google.com/drive/folders/1WFesrSSvO_BYY19TZUjjUrFvlecxRLsW?usp=sharing'
folder_id = url.split('/')[-1].split('?')[0]
from google.colab import auth
auth.authenticate_user() 
def folder_list(folder_id):
    from googleapiclient.discovery import build
    gdrive = build('drive', 'v3').files()
    res = gdrive.list(q="'%s' in parents" % folder_id).execute()
    return [[f['id'],f['name']] for f in res['files']]
itemsinfolder = folder_list(folder_id)
itemsinfolder
# downloading and initializing all important files as variables
downloadlink = 'https://drive.google.com/uc?id='
import requests
import io

from google.colab import auth
auth.authenticate_user() 
def downloadfolder(url):
    folder_id = url.split('/')[-1].split('?')[0]



print('Adding new variables: ')
for item in itemsinfolder:
    if item[1].split('.')[-1] != 'txt':
        id = item[0]
        link = downloadlink+id
        response = requests.get(link)
        response.raise_for_status()
        temp = np.load(io.BytesIO(response.content),allow_pickle=True)
        vars()[item[1].split('.')[0]] = temp
        print(item,'name:',item[1].split('.')[0])
        print(link)
