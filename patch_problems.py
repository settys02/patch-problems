import asyncio
import requests
import pandas as pd
import numpy as np
from io import StringIO
import json
import time
from headers import headers
import copy
import httpx


def build_id_map(headers, eid = 'paraSamplesGrid:c635f3a1-4d58-4753-a815-0491d44a5e4f'):
    url = 'https://devstaging.snbstg5bup.perkinelmercloud.com/api/rest/v1.0/sampleSummary/'
    eid = eid.replace(':', '%3A')
    url = url + eid + '/samples?page%5Boffset%5D=0&page%5Blimit%5D=5000'
    response = requests.get(url, headers=headers)
    d = json.loads(response.content.decode('utf-8'))
    id_map = {entity['attributes']['name'][:-4]: entity['attributes']['eid'] for entity in d['data']}
    return id_map


def build_col_map(headers, eid = 'sample:dd8fee9c-8c83-4b66-9fea-fafcb64c53df'):
    url = "https://devstaging.snbstg5bup.perkinelmercloud.com/api/rest/v1.0/samples/"
    eid = eid.replace(':', '%3A')
    url = url + eid + '/properties?' + '?value=display'
    response = requests.get(url, headers=headers)
    d = json.loads(response.content.decode('utf-8'))
    col_map = {i['attributes']['name']: i['attributes']['id'] for i in d['data'] if 'name' in i['attributes'].keys()}
    return col_map

def build_subrequest(data, key_map, id_map, col_map, out = {"id": "empty", "type": "samplesTableRow", "attributes" : {"columns": {}}}):
    if not data:
        return dict(out)
    if 'linkedEntityType' in data[0].keys():
        out['id'] = id_map[data[0]['display']]
        return build_subrequest(data[1:], key_map, id_map, col_map, out)
    else:
        out['attributes']['columns'][col_map[key_map[str(data[0]['key'])]]] = {"content": {"value": data[0]['value']}}
        return build_subrequest(data[1:], key_map, id_map, col_map, out)

def build_request(headers, id_map, col_map, eid = 'paragrid:29c22d49-ebb0-4493-b4c0-5e4810820506'):
    url = 'https://devstaging.snbstg5bup.perkinelmercloud.com/api/rest/v1.0/subexpSummary/'
    eid = eid.replace(':', '%3A')
    url = url + eid + str('/rows')
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    key_map = {item['key']: item['title'] for item in data['included'][0]['attributes']['cols']}
    return [copy.deepcopy(dict(build_subrequest(sample['attributes']['columns'], key_map, id_map, col_map))) 
            for sample in data['data']]


id_map = build_id_map(headers)
col_map = build_col_map(headers)
req = build_request(headers, id_map, col_map)

if __name__ == "__main__":  

    #samples 2,6,11,13,30,34,35,47,57,64 consistently return error 428 precondition required

    url = 'https://devstaging.snbstg5bup.perkinelmercloud.com/api/rest/v1.0/samplesTables/paraSamplesGrid%3A116bef06-e216-4a8e-a03b-b85f3519315f/rows?force=true'

    print('---------------------------------------------------------------------------------')
    print('Patching 92 samples in paraSamplesGrid:116bef06-e216-4a8e-a03b-b85f3519315f in Notebook 0800162 using samples bulk update patch endpoint:')
    print('')
    for i in range(0,92):
        response = httpx.patch(url, headers=headers, json={"data": [req[i]]}, timeout=None)
        if str(response) == '<Response [428 Precondition Required]>':
            out = 'Sample #' + str(i) + ' (' + str(req[i]['id']) + ')' + ':' + str(response)
            print(out)
    
    print('')
    print('---------------------------------------------------------------------------------')
    print('')
    response = httpx.patch(url, headers = headers, json={"data": req[65:92]}, timeout=None)
    print('Response for patching samples 65 to 92: ')
    print(response)
    print('')
    response = httpx.patch(url, headers = headers, json={"data": req[64:92]}, timeout=None)   
    print('response for patching samples 64 to 92: ')
    print(response)