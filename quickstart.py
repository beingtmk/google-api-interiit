#!/usr/bin/env python

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    results = service.files().list(
        q="name='Photos'" ,pageSize=10, fields="nextPageToken, files(id, name)").execute()


    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

    folder_id = items[0]['id']
    print("'%s' in parents" %(folder_id))

    # Call the Drive v3 API
    results = service.files().list(
        q="'%s' in parents" %(folder_id) ,pageSize=10, fields="nextPageToken, files(id, name)").execute()


    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

    f = open("output.html", "w")
    f.write('<html><body>')

    for item in items:
        str = "http://drive.google.com/uc?export=view&id="+item['id']
        str1 = '<img src="' + str + '" style="width: 500px; max-width: 100%; height: auto">'
        f.write(str1)
        print(str1)

    f.write('</html></body>')
    f.close()

if __name__ == '__main__':
    main()
