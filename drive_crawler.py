# chcp 65001
# set PYTHONIOENCODING=UTF-8
# drive_crawler.py > filename.csv 2> filename2.csv
# coding=UTF-8

import sys
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import sample_tools
from functools import reduce

# How to use the OAuth 2.0 client is described here:
# https://developers.google.com/api-client-library/python/guide/aaa_oauth

SCOPE = ('https://www.googleapis.com/auth/drive'+
        'https://www.googleapis.com/auth/drive.file'+
        'https://www.googleapis.com/auth/drive.photos.readonly'+
        'https://www.googleapis.com/auth/drive.metadata'+ 
        'https://www.googleapis.com/auth/drive.metadata.readonly'+ 
        'https://www.googleapis.com/auth/drive.readonly')

# client_secrets.json is downloaded from the API console:
# https://code.google.com/apis/console/#project:<PROJECT_ID>:access
# where <PROJECT_ID> is the ID of your project

def recorrer_directorio(service, folderFileId):
  page_token = None
  while True:
    response = service.files().list(q="'"+folderFileId+"' in parents",
                                        spaces='drive',
                                        corpora='user',
                                        fields='nextPageToken,files(id, name, mimeType, createdTime,owners)',
                                        pageToken=page_token).execute()
    for file in response.get('files', []):
      if file.get('mimeType') != 'application/vnd.google-apps.folder':
        try:
          listar_revisiones(service, file, folderFileId);
        except:
          print >> sys.stderr, file.get('id') + ';' + file.get('name')+ ';' + file.get('mimeType')+ ';' + file.get('createdTime') + ';' + reduce((lambda x,y: x+'+'+y ),map((lambda x: x.get('displayName')),file.get('owners')))
      else:
        recorrer_directorio(service, file.get('id'));

    page_token = response.get('nextPageToken', None)
    if page_token is None:
      break

def listar_revisiones(service, file, folderFileId):
  pageToken2 = None
  while True:
    response2 = service.revisions().list(fileId=file.get('id'),
                                        pageSize=1000,pageToken=pageToken2,
                                        fields='nextPageToken, revisions(id,modifiedTime,lastModifyingUser)'
                                        ).execute()
    for revision in response2.get('revisions', []):
      displayName = u' '
      emailAddr = u' '
      if revision.get('lastModifyingUser') != None:
        displayName = revision.get('lastModifyingUser').get('displayName')
        emailAddr = revision.get('lastModifyingUser').get('emailAddress')
        if displayName == None:
          displayName = u'NA'
        if emailAddr == None:
          emailAddr = u'NA'
      
      print u''.join(
          (# folderFileId,',',
          file.get('id'),';',
          file.get('name'),';',
          file.get('mimeType'),';',
          file.get('createdTime'),';',
          reduce((lambda x,y: x+'+'+y ),map((lambda x: x.get('displayName')),file.get('owners'))),';',
          revision.get('modifiedTime'),';',
          displayName
          )).encode('utf-8').strip()
    pageToken2 = response2.get('nextPageToken', None)
    if pageToken2 is None:
      break

def main(argv):
  flow = flow_from_clientsecrets('client_secrets.json',
                                scope=SCOPE,
                                redirect_uri='http://localhost')

  storage = Storage('plus.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
      run_flow(flow,storage)

  service, flags = sample_tools.init(
      argv, 'drive', 'v3', __doc__, __file__,
      scope= 'https://www.googleapis.com/auth/drive')

  try:
    folderFileId = '0B_UC-7ShbgndTzlvaS1DOWVhRnM' #flf
    # folderFileId = '0B0V-zM54DsKKSnhOTHk1RDZEX1U' #kids
    # folderFileId = '0B6E2Atn07k-5c0w4c0xNbURuaG8' #pabellon

    print "fileId;fileName;mimeType;createdTime;ownerName;modifiedTime;lastModName"

    recorrer_directorio(service, folderFileId);

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
          'the application to re-authorize')
 
if __name__ == '__main__':
  main(sys.argv)