from datetime import datetime, timedelta
import random
from flask.helpers import get_root_path
from dashlib import *

def register_dashapp(my_app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
                           server=my_app,
                           url_base_pathname='/' + base_pathname + '/',
                           assets_folder=get_root_path(__name__) + '/' + base_pathname + '/assets/',
                           meta_tags=[meta_viewport])

    with my_app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)

def create_app():
    server = Flask(__name__)

    from user_dashapp.layout import layout as layout1
    from user_dashapp.callbacks import register_callbacks as register_callbacks1
    register_dashapp(server, 'Games Dashboard', 'dashboard', layout1, register_callbacks1)

    return server

app = create_app()



@app.route('/')
def index():
    local_ip = get_local_ip()
    return redirect("http://" + local_ip + ":5000/debug", code=302)


@app.route('/debug')
def debugapp():
    score = random.randint(1,10000)
    #score = 100000000
    return __name__ + '<br>' + \
           '<a href="dashboard">Dashboard</a><br>' \
           '<a href="db">get db data</a><br>' + \
           '<a href="db/user/' + str(score) + ' ">insert records with db/name/score </a>'


@app.route('/db')
def readdb():
    return 'DB DATA<br>' + str(table_users.all())

@app.route('/db/<string:name>/<int:score>')
def show_post(name, score):
    # returns the post, the post_id should be an int
    # table = db.table('table')
    # user = tinydb.Query()

    now = datetime.now().strftime(DATETIME_FORMAT)
    print(name, now, score)
    table_users.insert({'name': name, 'score': score, 'time': now})

    return str('done for {} {} {}'.format(name, now, score))

# set FLASK_ENV=development
# set FLASK_APP=app.py

# import pandas_datareader as pdr
# from dash.dependencies import Input
# from dash.dependencies import Output
