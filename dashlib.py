from flask import Flask, redirect
import dash
from dash.dependencies import Input, Output, State
from tinydb import TinyDB, Query
import pandas as pd
import socket

DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
DB_PATH = "./tiny.sqlite"


db = TinyDB(DB_PATH, default_table='users')
table_users = db.table("users")
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

def get_users_from_db(name_regex = None):
    raw_obj = None
    if name_regex is None:
        raw_obj = table_users.all()
    else:
        User = Query()
        raw_obj = table_users.search(User.name == name_regex)
    all_users_df = pd.DataFrame(raw_obj)
    best_users_df = None
    all_users_sorted_df = None
    if all_users_df.empty:
        all_users_sorted_df = pd.DataFrame(columns=['name', 'score', 'time'])
        best_users_df = pd.DataFrame(columns=['name', 'score', 'time'])
    else:
        all_users_sorted_df = all_users_df.sort_values(by="time", ascending=False)
        best_users_df = all_users_df.nlargest(10, "score")
    return {"all": all_users_sorted_df, "best": best_users_df}