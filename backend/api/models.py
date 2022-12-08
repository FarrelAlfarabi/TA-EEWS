from django.db import models
from .firebase_config import *

def get_GMJI_data_firebase(name):
    lst = []
    store = []
    for data in database.child('mseed_data/'+name).child('traces').get().val():
        store.append(data)
         
    for datas in store:
        if datas['station'] == "GMJI":
            lst.append(datas)
    return lst

def get_JAGI_data_firebase(name):
    lst = []
    store = []
    for data in database.child('mseed_data/'+name).child('traces').get().val():
        store.append(data)     
           
    for datas in store:
        if datas['station'] == "JAGI":
            lst.append(datas)
    return lst

def get_PWJI_data_firebase(name):
    lst = []
    store = []
    for data in database.child('mseed_data/'+name).child('traces').get().val():
        store.append(data)
        
    for datas in store:
        if datas['station'] == "PWJI":
            lst.append(datas)
    return lst
