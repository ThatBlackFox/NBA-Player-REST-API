from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3
import collections
import subprocess

app = FastAPI()

conn = sqlite3.connect('data.db')
cor = conn.cursor()

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html",'r') as f: 
        html = f.read()
    return HTMLResponse(content=html, status_code=200)

@app.get("/players/")
async def data(lastnameletter:str=None,limit:int=50,page:int=0,start_year:int=None,end_year:int=None,pos:str=None,height:str=None,weight:int=None,college:str=None):
    params = locals()
    for arg in list(params):
        print(arg)
        if arg == 'limit' or arg=='page':
            params.pop(arg)
        elif not params[arg]:
            params.pop(arg)
    to_execute = "SELECT * FROM players WHERE "
    for arg in params:
        if not 'year' in arg:
            to_execute = to_execute+f"{arg}='{params[arg]}' AND "
        else:
            to_execute = to_execute+f"{arg}={params[arg]} AND "
    cor.execute(to_execute[:-4])
    raw_data = cor.fetchall()
    data = []
    s=page*limit
    if raw_data:
        if page*limit+limit>len(raw_data):
            limit=len(raw_data)
        for i in range(s,limit,1):
            d = collections.OrderedDict()
            d["url"] = raw_data[i][0]
            d["lastnameletter"] = raw_data[i][1]
            d["name"] = raw_data[i][2]
            d["start_year"] = raw_data[i][3]
            d["end_year"] = raw_data[i][4]
            d["position"] = raw_data[i][5]
            d["height"] = raw_data[i][6]
            d["weight"] = raw_data[i][7]
            d["dob"] = raw_data[i][8]
            d["college"] = raw_data[i][9]
            data.append(d)
        return data
    else:
        return raw_data

if __name__ == "__main__":
    subprocess.run(["python", "-m", "uvicorn", "main:app", "--reload"])