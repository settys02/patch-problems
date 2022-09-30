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

url = 'https://devstaging.snbstg5bup.perkinelmercloud.com/api/rest/v1.0/samplesTables/paraSamplesGrid%3A116bef06-e216-4a8e-a03b-b85f3519315f/rows?force=true'

with open('payload.txt') as file:
    req = json.load(file)


 #samples 2,6,11,13,30,34,35,47,57,64 consistently return error 428 precondition required

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