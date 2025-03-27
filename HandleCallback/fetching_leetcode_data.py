import requests 
import json
import datetime


def header(reponse):
     value=json.loads(reponse)
     header={
        "Content-Type":"application/json",
        "x-csrftoken":value["csrf_token"],
        "cookie":f"csrftoken={value["csrf_token"]};LEETCODE_SESSION={value["cookies"]}",
        "Referer": "https://leetcode.com/",
        "Origin": "https://leetcode.com"
        
                
    }
     return header
def fetch_data(headers,url,type="get",query=None,payload=None):
    endpoint=""
    if type=='get':
         endpoint=requests.get(url,headers=headers)
         if endpoint.status_code==200:
             return endpoint.json()
         else:
             print(endpoint.status_code,endpoint.text)
    else:
        endpoint=requests.post(url,json=payload,headers=headers)
        if endpoint.status_code==200:
            return endpoint.json()
        else:
            print(endpoint.status_code,endpoint.text)
            
    return False
def time_difference(timestamp):
    convert=datetime.datetime.fromtimestamp(timestamp=int(timestamp))
    current=datetime.datetime.now().minute
    print(convert.minute,current)

def adding_zero(value,needed):
    change=str(value)
    if len(change) < needed:
        return "0" * (needed - len(change)) + change