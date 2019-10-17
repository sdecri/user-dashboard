from dashlib import *


# db.purge_table("users")
# from datetime import datetime,timedelta
# nUsers = 100000
# data = [{"name": "foo_" + str(i), "score": i
#             , "time":(datetime.now() - timedelta(seconds=i)).strftime(DATETIME_FORMAT)} for i in range(0, nUsers)]
# db.insert_multiple(data)





def register_callbacks(dashapp):

    def create_obj_to_update_users_tables(users):

        all_users_df = users["all"]
        best_users_df = users["best"]
        return [all_users_df.to_dict('records'), best_users_df.to_dict('records')]

    # @dashapp.callback(
    #     Output('user-search', 'value')
    #     ,[Input('user-search', 'persistence')])
    # def search_box_clear(n_clicks_ts_search_clear):
    #     if n_clicks_ts_search_clear > 0:
    #         return ''
    #     dash.exceptions.PreventUpdate()




    @dashapp.callback(
        [Output('table_all_users', 'data'), Output('table_best_users', 'data')]
        ,[
            Input('btn_refresh', 'n_clicks_timestamp')
            , Input('btn_save', 'n_clicks_timestamp')
        ], [State('table_all_users', 'data')])
    def display(n_clicks_ts_refresh, n_clicks_ts_save, current_table_data):

        btn_state = [int(n_clicks_ts_refresh), int(n_clicks_ts_save)]
        msg = ""
        output = []
        name_regex = None
        if all(v == 0 for v in btn_state):
            # it will be fired on th page load.
            print "I was fired on page load"
            dash.exceptions.PreventUpdate()
        else:
            max_index = btn_state.index(max(i for i in btn_state if i is not None))

            if max_index == 0:
                msg = "Refresh was clicked"

            elif max_index == 1:
                db.purge_table("users")
                table_users.insert_multiple(current_table_data)
                msg = "Save was clicked"

            else:
                msg = 'None of the buttons have been clicked yet'

        output = create_obj_to_update_users_tables(get_users_from_db(name_regex))

        print msg


        return output[0], output[1]
