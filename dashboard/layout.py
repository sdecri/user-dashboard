import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dashlib import *

def serve_layout():
    users = get_users_from_db()
    all_users_df = users["all"]
    best_users_df = users["best"]


    return html.Div([

        html.H1('Scoreboard')
        # , dcc.Dropdown(
        #     id='my-dropdown',
        #     options=[
        #         {'label': 'Today', 'value': 'Today'},
        #         {'label': 'Best', 'value': 'Best'},
        #         {'label': 'Last', 'value': 'Last'}
        #     ],
        #     value='Today'
        # )
        , dcc.Loading(id="loading-1", children=[
            html.Button(
                ['Refresh'], id='btn_refresh', n_clicks_timestamp=0
            )
            , html.H2('Top 10')
            , dash_table.DataTable(
                id='table_best_users'
                , columns=[{"name": j, "id": j} for j in best_users_df]
                , data=best_users_df.to_dict('records')
                , style_table={'overflowX': 'scroll'}
            )
            , html.H2('All Game Records')
            , html.Button(
                ['Save'], id='btn_save', n_clicks_timestamp=0
            )
            , dash_table.DataTable(
                id='table_all_users'
                , sort_action="native"
                , sort_mode="single"
                , sort_by={"time": "desc"}
                , columns=[{"name": j, "id": j, "editable": True if j == "name" else False} for j in all_users_df]
                , data=all_users_df.to_dict('records')
                , row_deletable=True
                , filter_action='native'
                , style_table={'overflowX': 'scroll'}
            )
        ], type="default")
    ], style={'width': '500'})

layout = serve_layout()