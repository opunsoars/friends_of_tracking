import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from helper import *
import cloudpickle
from params import MATCH, LIV_GOALS, SCORER

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# LOAD DASH DATA FOR MATCH
with open('../datahub/lastrow/figs/{}.pkl'.format(LIV_GOALS[MATCH]['PLAY']), 'rb') as handle:
    dash_dict = cloudpickle.load(handle)
    handle.close()

if SCORER:
    hmap = dash_dict['hmap']['white_scorer']
else:
    hmap = dash_dict['hmap']['white']
bar = dash_dict['bar']
print(len(hmap['frames']))
print('MATCH: {} || PLAY: {} || {} frames'.format(MATCH,
                                                  LIV_GOALS[MATCH]['PLAY'],
                                                  LIV_GOALS[MATCH]['END']+1
                                                  ))


# tracking_home, tracking_away, events = populate_LIV_tracking_dataframes()
# 52696 - 53075
# fig_dict = plot_pitch_slider(
#     # event_start_frame=52696,
#     # event_end_frame=53075,
#     # tracking_home=tracking_home,
#     # tracking_away=tracking_away
# )
# fname = '../datahub/lastrow/{}_fig_dict_white_scorer.pickle'.format(LIV_GOALS[MATCH]['PLAY'])
# fname = '../datahub/lastrow/{}_fig_dict_white.pickle'.format(
#     LIV_GOALS[MATCH]['PLAY'])
# # fname = '../datahub/lastrow/{}_fig_dict_green.pickle'.format(LIV_GOALS[MATCH]['PLAY'])


# with open(fname, 'rb') as handle:
#     fig_dict = cloudpickle.load(handle)
#     handle.close()
# tracking_frames = range(LIV_GOALS[MATCH]['START'],
#                         LIV_GOALS[MATCH]['END']+1)
# layout = generate_pitch_layout()
# # layout["paper_bgcolor"] = "#1f2630"
# speedbar_layout = generate_bar_layout()


app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                html.H4(children="Liverpool Goals Visual Analytics - GOALVID19"),
                html.P(
                    id="description",
                    children="† As a part of David Sumpter's #FriendsOfTracking #FoT course challenge, \
                    19 Liverpool goals have been shown here by using tracking data from LastRow and pitch \
                    control models by Will Spearman (code adapted from Laurie Shaw)",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    className="six columns",
                    children=[
                        html.P(id="heatmap-selector", children="Select goal:"),
                        dcc.Dropdown(
                            id="chart-dropdown",
                            value="Bayern 0 - [1] Liverpool",
                            options=[
                                {"label": goal['PLAY'],
                                 "value":goal['PLAY']} for goal in LIV_GOALS
                            ],
                        ),
                        dcc.RadioItems(
                            id='scorer-radio-selector',
                            options=[{'label': 'All Players', 'value': 'False'},
                                     {'label': 'Goalscorer', 'value': 'True'}],
                            value='False',
                            labelStyle={'display': 'inline-block'}
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                # html.H6(children="{}".format(
                                #     LIV_GOALS[MATCH]['PLAY'])),
                                html.P(
                                    id="heatmap-text",
                                    children="Press play to view the goal",
                                ),
                                dcc.Graph(
                                    id='pitch-control-heatmap',
                                    #   className="six columns",
                                    figure=hmap
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="right-column",
                    className="six columns",
                    children=[
                        # html.P(
                        #     id="chart-selector",
                        #        children="Select chart:"
                        # ),
                        dcc.Graph(
                            id='home-player-speed-bar',
                            figure=bar[0]
                            #   className="six columns",
                            # figure={
                            #     'data': generate_bar_data_for_frame(0),
                            #     'layout': speedbar_layout
                            # }
                        ),
                        dcc.Slider(
                            id='frame-slider',
                            min=list(bar.keys())[0],
                            max=list(bar.keys())[-1],
                            value=list(bar.keys())[0],
                            marks={str(frame_id): str(frame_id)
                                   for frame_id in list(bar.keys())[::20]},
                            updatemode='drag',
                            step=1
                        ),
                        html.H4(
                            id='show-selected-frame-container',
                            style={
                                'margin-top': 20,
                                'margin-left': 50
                            }
                        )
                    ],
                ),
            ],
        ),
    ],
)


# callbacks
@app.callback(Output('show-selected-frame-container', 'children'),
              [Input('frame-slider', 'value')])
def display_value(value):
    return 'Frame: {}'.format(value)


# @app.callback(
#     Output('pitch-control-heatmap', 'figure'),
#     [Input('chart-dropdown', 'value')])
# def load_match_plot(play):
#     # LOAD DASH DATA FOR MATCH
#     with open('../datahub/lastrow/figs/{}.pkl'.format(play), 'rb') as handle:
#         dash_dict = cloudpickle.load(handle)
#         handle.close()
#     hmap = dash_dict['hmap']['white']
#     return hmap

# @app.callback(
#     Output('pitch-control-heatmap', 'figure'),
#     [Input('scorer-radio-selector', 'value')])
# def update_scorer(scorer):
#     if scorer == 'True':
#         hmap = dash_dict['hmap']['white_scorer']
#     else:
#         hmap = dash_dict['hmap']['white']

#     return hmap

# @app.callback(
#     Output('pitch-control-heatmap', 'figure'),
#     [Input('frame-slider', 'value')])
# def update_graph(frame_value):
#     update = {
#         "data": [],
#         "layout": {},
#     }

#     update['layout'] = hmap['layout']
#     update['data'] = hmap['frames'][frame_value]['data']
#     # update['data'] = generate_data_for_frame(frame_num=frame_value)

#     return update

@app.callback(
    Output('pitch-control-heatmap', 'figure'),
    [Input('chart-dropdown', 'value'),
     Input('scorer-radio-selector', 'value'),
     Input('frame-slider', 'value')])
def update_graph(play, scorer, frame_value):
    ctx = dash.callback_context
    if not ctx.triggered:
        # Handle initial firing on page load - do not update options
        return dash.no_update, dash.no_update
    print (ctx.triggered)

    if ctx.triggered[0]['prop_id'] == 'chart-dropdown.value':
        # LOAD DASH DATA FOR MATCH
        with open('../datahub/lastrow/figs/{}.pkl'.format(play), 'rb') as handle:
            dash_dict = cloudpickle.load(handle)
            handle.close()    
        hmap = dash_dict['hmap']['white']
        return hmap

    elif ctx.triggered[0]['prop_id'] == 'scorer-radio-selector.value':
        # LOAD DASH DATA FOR MATCH
        with open('../datahub/lastrow/figs/{}.pkl'.format(play), 'rb') as handle:
            dash_dict = cloudpickle.load(handle)
            handle.close() 
        if scorer == 'True':
            hmap = dash_dict['hmap']['white_scorer']
        else:
            hmap = dash_dict['hmap']['white']

        return hmap

    elif ctx.triggered[0]['prop_id'] == 'frame-slider.value':
        update = {
            "data": [],
            "layout": {},
        }

        update['layout'] = hmap['layout']
        update['data'] = hmap['frames'][frame_value]['data']
        # update['data'] = generate_data_for_frame(frame_num=frame_value)

        return update
    
    else:
        # need to ensure all paths have return value
        return dash.no_update, dash.no_update


@app.callback(
    Output('home-player-speed-bar', 'figure'),
    [Input('frame-slider', 'value')])
def update_graph(frame_value):
    update = {
        "data": [],
        "layout": {},
    }
    update = bar[frame_value]

    # update['layout'] = bar[frame_value]['layout']
    # # update['data'] = fig_dict['frames'][frame_value]['data']
    # update['data'] = generate_bar_data_for_frame(frame_num=frame_value)

    return update


if __name__ == '__main__':
    app.run_server(debug=True)
