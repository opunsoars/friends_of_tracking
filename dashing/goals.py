import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from helper import *
import cloudpickle
from params import MATCH, LIV_GOALS, SCORER
from tqdm.auto import tqdm

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# LOAD DASH DATA FOR MATCH [0,1,2,3,4,5]
match_dict = {}
for m in tqdm(range(1)):
    with open('../datahub/lastrow/figs/{}.pkl'.format(LIV_GOALS[m]['PLAY']), 'rb') as handle:
        dash_dict = cloudpickle.load(handle)
        handle.close()
    match_dict[LIV_GOALS[m]['PLAY']] = dash_dict
    del dash_dict


# if SCORER:
#     hmap = dash_dict['hmap']['white_scorer']
# else:
#     hmap = dash_dict['hmap']['white']
# bar = dash_dict['bar']
# print(len(hmap['frames']))
# print('MATCH: {} || PLAY: {} || {} frames'.format(MATCH,
#                                                   LIV_GOALS[MATCH]['PLAY'],
#                                                   LIV_GOALS[MATCH]['END']+1
#                                                   ))


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
            className='row',
            children=[
                # html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                html.H4(children="Liverpool Goals Visual Analytics - GOALVID19"),
                html.P(
                    children=[
                        "† As a part of David Sumpter's #FriendsOfTracking #FoT course challenge,",
                        # html.Br(),
                        "19 Liverpool goals have been crunched and analysed here using tracking data ",
                        # html.Br(),
                        "from LastRow and pitch control models by Will Spearman (code adapted from Laurie Shaw)"
                    ]
                )
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    className="six columns",
                    children=[
                        html.Div(className='row',
                                 children=[
                                     html.P(
                                         className='three columns',
                                         id="heatmap-selector",
                                         children="Select goal:",
                                          style={
                                                 'text-align': 'center'
                                             }
                                     ),
                                     dcc.Dropdown(
                                         className='three columns',
                                         id="chart-dropdown",
                                         value="Bayern 0 - [1] Liverpool",
                                         options=[
                                             {"label": goal['PLAY'],
                                              "value":goal['PLAY']} for goal in LIV_GOALS
                                         ],
                                         #  style={
                                         #      'width': '60%',
                                         #      'display': 'inline-block',
                                         #  }
                                     ),
                                     dcc.RadioItems(
                                         className='three columns',
                                         id='scorer-radio-selector',
                                         options=[{'label': 'All Players', 'value': 'False'},
                                                  {'label': 'Goalscorer', 'value': 'True'}],
                                         value='False',
                                         labelStyle={
                                             'display': 'inline-block'}
                                     ),
                                     html.P(
                                         className='three columns',
                                         id="heatmap-text",
                                         children="Press play to view the goal",
                                     ),
                                 ]),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                # html.H6(children="{}".format(
                                #     LIV_GOALS[MATCH]['PLAY'])),

                                dcc.Graph(
                                    id='pitch-control-heatmap',
                                    #   className="six columns",
                                    # figure=match_dict["Bayern 0 - [1] Liverpool"]["hmap"]["white"]
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
                            # figure=match_dict["Bayern 0 - [1] Liverpool"]["bar"][0]
                            #   className="six columns",
                            style={
                                # 'display': 'inline-block',
                                'text-align': 'right',
                                'margin-left': 50
                            }

                        ),
                        dcc.Slider(
                            id='frame-slider',
                            # min=0,  # list(bar.keys())[0],
                            # max=200,  # list(bar.keys())[-1],
                            # value=0,  # ist(bar.keys())[0],
                            # marks={str(frame_id): str(frame_id)
                            #        for frame_id in list(match_dict["Bayern 0 - [1] Liverpool"]["bar"].keys())[::20]},
                            updatemode='drag',
                            step=1,
                            # style={
                            #     # 'margin-top': 20,
                            #     # 'margin': 50
                            # }
                        ),
                        html.H4(
                            id='show-selected-frame-container',
                            style={
                                # 'margin-top': 20,
                                'margin-left': 50
                            }
                        ),
                        html.H6(
                            "How to Use",
                            style={
                                # 'margin-top': 20,
                                'margin-left': 50
                            }
                        ),
                        html.P(
                            children=[
                                "‣ Select a goal from the dropdown and wait for it to load. Press play to view the video.",html.Br(),
                                "‣ Use the slider to examine frame by frame. Drag the slider slowly and the frame in video would change sluggishly. But you can view the pitch control changing as well.",html.Br(),
                                "‣ In the barchart, each player's velocity is visible with maximum speed too.It is possible to notice how Liverpool players (especially goal scorers) are quicker to accelerate and hit top speed around the time of anticipated assist pass. This is a key quality of their attack.",html.Br(),
                                '‣ Choose Goal Scorer radio button to update the map with only his pitch control',html.Br(),
                                "‣ You can drag and zoom on any map and double click to zoom out"
                            ],
                            style={
                                # 'margin-top': 20,
                                'margin-left': 50,
                                'font-size':13,
                            }
                        ),
                        html.A(
                            id='footer',
                            href='https://twitter.com/opunsoars',
                            children=[
                                'Author: @opunsoars | Vinay Warrier'
                            ],
                            style={
                                'margin-left': 600,
                                'font-size':15,
                            }

                        )
                    ],
                ),
            ],
        ),

    ],
)


# callbacks

# print the selected frame
@app.callback(Output('show-selected-frame-container', 'children'),
              [Input('frame-slider', 'value')])
def display_value(value):
    return 'Frame: {}'.format(value)

# update slider based on selected play


@app.callback(
    [Output('frame-slider', 'min'),
     Output('frame-slider', 'max'),
     Output('frame-slider', 'value'),
     Output('frame-slider', 'marks')],
    [Input('chart-dropdown', 'value')])
def set_slider_marks(play):
    bar = match_dict[play]['bar']
    min_ = list(bar.keys())[0]
    max_ = list(bar.keys())[-1]
    value = list(bar.keys())[0]
    marks = {str(frame_id): str(frame_id)
             for frame_id in list(bar.keys())[::20]}
    return min_, max_, value, marks

# update heatmap based on play, scorer, & slider


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
    # print(ctx.triggered)

    if ctx.triggered[0]['prop_id'] == 'chart-dropdown.value':
        # LOAD DASH DATA FOR MATCH
        dash_dict = match_dict[play]
        hmap1 = dash_dict['hmap']['white']
        return hmap1

    elif ctx.triggered[0]['prop_id'] == 'scorer-radio-selector.value':
        # LOAD DASH DATA FOR MATCH
        dash_dict = match_dict[play]
        if scorer == 'True':
            hmap2 = dash_dict['hmap']['white_scorer']
        else:
            hmap2 = dash_dict['hmap']['white']

        return hmap2

    elif ctx.triggered[0]['prop_id'] == 'frame-slider.value':
        update = {
            "data": [],
            "layout": {},
        }

        dash_dict = match_dict[play]
        if scorer == 'True':
            hmap3 = dash_dict['hmap']['white_scorer']
        else:
            hmap3 = dash_dict['hmap']['white']

        update['layout'] = hmap3['layout']
        update['data'] = hmap3['frames'][frame_value]['data']
        # update['data'] = generate_data_for_frame(frame_num=frame_value)

        return update

    else:
        # need to ensure all paths have return value
        return dash.no_update, dash.no_update

# update speed bar based no play and slider


@app.callback(
    Output('home-player-speed-bar', 'figure'),
    [Input('chart-dropdown', 'value'),
     Input('frame-slider', 'value')])
def update_graph(play, frame_value):
    update = {
        "data": [],
        "layout": {},
    }
    update = match_dict[play]["bar"][frame_value]

    # update['layout'] = bar[frame_value]['layout']
    # # update['data'] = fig_dict['frames'][frame_value]['data']
    # update['data'] = generate_bar_data_for_frame(frame_num=frame_value)

    return update


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
