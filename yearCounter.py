from urllib.request import Request, urlopen
import json
import time
from datetime import date
import numpy as np
import re
import random

LEN = 2024-1500
arr = np.zeros(LEN, dtype=int)
listie = [None]*LEN
for i in range(LEN):
    listie[i] = []

def getIndex(stri):
    s_index = stri.index("title=")
    e_index = stri.index("\"",s_index+7)
    return stri[s_index+7:e_index]

def doChunk(chunk, arr, S_YEAR):
    s = 1000*chunk+1
    e = 1000*chunk+1000
    URL = "https://en.wikipedia.org/wiki/Meanings_of_minor_planet_names:_"+str(s)+"-"+str(e)
    req = Request(
        url=URL,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read().decode()
    lines = webpage.split("\n")

    for i in range(len(lines)):
        shouldAddYear = -1
        if "born " in lines[i]:
            index = lines[i].index("born ")
            results = re.findall(r'\d+', lines[i][index:])
            if len(results) >= 1:
                yr = int(results[0])-S_YEAR
                if yr >= 0 and yr < len(arr):
                    shouldAddYear = yr

        elif "(" in lines[i]:
            index_s = lines[i].index("(")+1
            range_str = lines[i][index_s:]
            if "–" in range_str:
                before_dash = range_str[:range_str.index("–")]
                if before_dash.isnumeric():
                    yr = int(before_dash)-S_YEAR
                    if yr >= 0 and yr < len(arr):
                        shouldAddYear = yr

        if shouldAddYear >= 0:
            arr[shouldAddYear] += 1
            listie[shouldAddYear].append(getIndex(lines[i-2]))

    print("Finished doing chunk "+str(chunk))
    time.sleep(1)


for i in range(0,630):   #630
    doChunk(i,arr,1500)

f = open("count6.csv","w+")
for i in range(LEN):
    listier = ""
    sample = random.sample(listie[i], min(10,len(listie[i])))
    for s in sample:
        listier += ","+s
    f.write(str(arr[i])+listier+"\n")
f.flush()
f.close()
