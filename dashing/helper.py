import sys
sys.path.insert(
    0, '/media/csivsw/crossOS/playground/friends_of_tracking/src/friends_of_tracking/LaurieOnTracking')
from params import *
import Metrica_Viz as mviz
import Metrica_Velocities as mvel
import Metrica_IO as mio
from tqdm.auto import tqdm
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import cloudpickle
from time import time
from functools import wraps
from collections import namedtuple
import pickle


def timing(f):
    # https://stackoverflow.com/a/27737385/4232601
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r took: %2.4f sec' %
              (f.__name__, te-ts))
        return result
    return wrap


@timing
def populate_tracking_dataframes():
    tracking_home = mio.tracking_data(DATA_DIR, MATCH_ID, 'Home')
    tracking_away = mio.tracking_data(DATA_DIR, MATCH_ID, 'Away')
    events = mio.read_event_data(DATA_DIR, MATCH_ID)

    tracking_home = mio.to_metric_coordinates(tracking_home)
    tracking_away = mio.to_metric_coordinates(tracking_away)
    events = mio.to_metric_coordinates(events)

    tracking_home = mvel.calc_player_velocities(tracking_home, smoothing=True)
    tracking_away = mvel.calc_player_velocities(tracking_away, smoothing=True)

    return mio.to_single_playing_direction(tracking_home, tracking_away, events)


@timing
def populate_LIV_tracking_dataframes():
    # for a single match
    data_attack = pd.read_csv(GOALVID19_ATT, index_col=[0, 1])
    data_defence = pd.read_csv(GOALVID19_DEF, index_col=[0, 1])

    for play, score in list(zip(data_attack.index.get_level_values(0).unique(), SCORES)):
        data_attack.loc[play, 'score'] = score
        data_defence.loc[play, 'score'] = score

    tracking_home = data_attack.loc[LIV_GOALS[MATCH]['PLAY']]
    tracking_away = data_defence.loc[LIV_GOALS[MATCH]['PLAY']]

    tracking_home.columns = tracking_home.columns.str.replace('attack', 'Home')
    tracking_away.columns = tracking_away.columns.str.replace(
        'defense', 'Away')
    events = pd.DataFrame()
    return tracking_home, tracking_away, events


@timing
def generate_pitch_layout(tracking_frames=None, field_dimen=FIELD_DIM):
    # decide what color we want the field to be. Default is green, but can also choose white
    #     if field_color=='green':
    #         ax.set_facecolor('mediumseagreen')
    #         lc = 'whitesmoke' # line color
    #         pc = 'w' # 'spot' colors
    #     elif field_color=='white':
    #         lc = 'k'
    #         pc = 'k'
    # ALL DIMENSIONS IN m
    border_dimen = (3, 3)  # include a border arround of the field of width 3m
    meters_per_yard = 0.9144  # unit conversion from yards to meters
    half_pitch_length = field_dimen[0]/2.  # length of half pitch
    half_pitch_width = field_dimen[1]/2.  # width of half pitch
    signs = [-1, 1]
    # Soccer field dimensions typically defined in yards, so we need to convert to meters
    goal_line_width = 8*meters_per_yard
    box_width = 20*meters_per_yard
    box_length = 6*meters_per_yard
    area_width = 44*meters_per_yard
    area_length = 18*meters_per_yard
    penalty_spot = 12*meters_per_yard
    corner_radius = 1*meters_per_yard
    D_length = 8*meters_per_yard
    D_radius = 10*meters_per_yard
    D_pos = 12*meters_per_yard
    centre_circle_radius = 10*meters_per_yard

    point = namedtuple('point', ['x', 'y'])
    centre = point(0., 0.)

    shapes = []

    mid_circle = dict(type="circle", x0=centre.x - centre_circle_radius, y0=centre.y - centre_circle_radius,
                      x1=centre.x + centre_circle_radius, y1=centre.y + centre_circle_radius, line_color=FIELD_MARKINGS_COLOR, layer="below")
    mid_line = dict(type="line",
                    x0=centre.x, y0=centre.y - half_pitch_width,
                    x1=centre.x, y1=centre.y + half_pitch_width, line_color=FIELD_MARKINGS_COLOR, layer="below")
    mid_point = dict(type="circle",
                     x0=centre.x-0.4, y0=centre.y-0.4,
                     x1=centre.x+0.4, y1=centre.y+0.4, line_color=FIELD_MARKINGS_COLOR, fillcolor=FIELD_MARKINGS_COLOR, layer="below")
    shapes.extend([mid_circle, mid_line, mid_point])

    for s in signs:

        # plot pitch boundary
        boundary1 = dict(type="line",
                         x0=-half_pitch_length, y0=s*half_pitch_width,
                         x1=half_pitch_length, y1=s*half_pitch_width, line_color=FIELD_MARKINGS_COLOR, layer="below")

        boundary2 = dict(type="line",
                         x0=s*half_pitch_length, y0=-half_pitch_width,
                         x1=s*half_pitch_length, y1=half_pitch_width, line_color=FIELD_MARKINGS_COLOR, layer="below")

        circle = dict(type="circle",
                           x0=s*(centre.x+half_pitch_length-penalty_spot) - centre_circle_radius, y0=centre.y - centre_circle_radius,
                           x1=s*(centre.x+half_pitch_length-penalty_spot) + centre_circle_radius, y1=centre.y + centre_circle_radius, line_color=FIELD_MARKINGS_COLOR, layer="below")

        patch = dict(type="rect",
                     x0=s*half_pitch_length, y0=-area_width/2. - 1,
                     x1=s*(half_pitch_length - area_length), y1=area_width/2. + 1, line=dict(color=FIELD_COLOR, width=0), fillcolor=FIELD_COLOR, layer="below")

        box = dict(type="rect",
                   x0=s*half_pitch_length, y0=-area_width/2.,
                   x1=s*(half_pitch_length - area_length), y1=area_width/2., line=dict(color=FIELD_MARKINGS_COLOR, width=2), layer="below")
        D = dict(type="rect",
                 x0=s*half_pitch_length, y0=-box_width/2.,
                 x1=s*(half_pitch_length - box_length), y1=box_width/2., line=dict(color=FIELD_MARKINGS_COLOR, width=2), layer="below")
        pen = dict(type="circle",
                   x0=s*(half_pitch_length - penalty_spot)-0.4, y0=-0.4,
                   x1=s*(half_pitch_length - penalty_spot)+0.4, y1=0.4, line_color=FIELD_MARKINGS_COLOR, fillcolor=FIELD_MARKINGS_COLOR, layer="below")

        top_post = dict(type="rect",
                        x0=s*half_pitch_length, y0=goal_line_width/2. - 0.5,
                        x1=s*(half_pitch_length-0.5), y1=goal_line_width/2.+0.5, line=dict(color=FIELD_MARKINGS_COLOR, width=0), fillcolor=FIELD_MARKINGS_COLOR, layer="below")

        bottom_post = dict(type="rect",
                           x0=s*half_pitch_length, y0=-goal_line_width/2. - 0.5,
                           x1=s*(half_pitch_length-0.5), y1=-goal_line_width/2.+0.5, line=dict(color=FIELD_MARKINGS_COLOR, width=0), fillcolor=FIELD_MARKINGS_COLOR, layer="below")

        shapes.extend([boundary1, boundary2, circle, patch,
                       box, D, pen, top_post, bottom_post])
    if tracking_frames:
        print(len(tracking_frames), '<------here')
        sliders_dict = {
            "active": 0,
            #     "yanchor": "top",
            #     "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Frame:",
                "visible": True,
                "xanchor": "right"
            },
            #     "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            #     "len": 0.9,
            #     "x": 0.1,
            #     "y": 0,
            "steps": []
        }

        for frame_num in tracking_frames:
            slider_step = {"args": [
                [frame_num],
                {"frame": {"duration": 300, "redraw": False},
                 "mode": "immediate",
                 "transition": {"duration": 0, "easing": "linear"}
                 }
            ],
                "label": frame_num,
                "method": "animate"
            }
            sliders_dict["steps"].append(slider_step)

    updatemenus = {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 0, "redraw": False},
                                "fromcurrent": True,
                                "mode": "immediate",
                                "transition": {"duration": 0,
                                               "easing": "linear"
                                               }}],
                "label": ">",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "||",
                "method": "animate"
            }
        ],
        "direction": "left",
        # "pad": {"r": 40, "t": 50},
        "showactive": False,
        "type": "buttons",
        "xanchor": "right",
        "yanchor": "top",
        "x": 0.1,
        "y": 0.02,
    }

    # set axis limits
    xmax = field_dimen[0]/2. + border_dimen[0]
    ymax = field_dimen[1]/2. + border_dimen[1]

    layout = go.Layout(
        # title='Goal: {}'.format(LIV_GOALS[MATCH]['PLAY']),
        hovermode='closest',
        autosize=False,
        width=FIELD_WIDTH,
        height=FIELD_HEIGHT,
        plot_bgcolor=FIELD_COLOR,
        xaxis=go.layout.XAxis(
            range=[-xmax, xmax],
            showgrid=False, zeroline=False,
            showticklabels=False,
            visible=False
        ),
        yaxis=go.layout.YAxis(
            range=[-ymax, ymax],
            showgrid=False, zeroline=False,
            showticklabels=False,
            visible=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        legend = dict(x=0.2, y=0.03, orientation="h")
    )

    layout["shapes"] = shapes
    if tracking_frames:
        layout["sliders"] = [sliders_dict]
    layout["updatemenus"] = [updatemenus]

    return layout


def positions(tracking_data):
    position_traces = []
    for i, side in enumerate(['Home', 'Away']):
        team_data = tracking_data[i]
        player_nums = list(set(item for subitem in team_data.keys() for item in subitem.split('_')
                               if item.isdigit()))
        xlocs = [team_data['{}_{}_{}'.format(
            side, num, 'x')] for num in player_nums]
        ylocs = [team_data['{}_{}_{}'.format(
            side, num, 'y')] for num in player_nums]
        traces = go.Scatter(x=xlocs, y=ylocs, text=player_nums,
                            **player_marker_args[side], name=side)
        position_traces.append(traces)

    return position_traces


def velocities(tracking_data):
    velocity_quivers = []
    for i, side in enumerate(['Home', 'Away']):
        team_data = tracking_data[i]
        player_nums = list(set(item for subitem in team_data.keys() for item in subitem.split('_')
                               if item.isdigit()))
        xlocs = [team_data['{}_{}_{}'.format(
            side, num, 'x')] for num in player_nums]
        ylocs = [team_data['{}_{}_{}'.format(
            side, num, 'y')] for num in player_nums]
        xvels = [team_data['{}_{}_{}'.format(
            side, num, 'vx')] for num in player_nums]
        yvels = [team_data['{}_{}_{}'.format(
            side, num, 'vy')] for num in player_nums]
        trace = ff.create_quiver(x=xlocs, y=ylocs, u=xvels, v=yvels,
                                 scale=.5, line_color=player_marker_args[side]['marker_color'], name=side+'_vel')
        velocity_quivers.append(trace.data[0])

    return velocity_quivers


def plot_ball(tracking_data):
    team_data = tracking_data[0]
    trace = go.Scatter(x=[team_data['ball_x']], y=[team_data['ball_y']],
                       marker_size=10, marker_opacity=0.8, marker_color='white', marker_line_width=2, marker_line_color="green",
                       name='ball'
                       )
    return [trace]


# tracking_home, tracking_away, events = populate_LIV_tracking_dataframes()
# with open("../datahub/lastrow/{}_pc_dict.pkl".format(LIV_GOALS[MATCH]['PLAY']), "rb") as handle:
#     pitch_control_dict = pickle.load(handle)
#     handle.close()


def team_pitch_control(pitch_control_dict, frame_num, player_num=None):
    # frame_num = str(frame_num)
    # print (frame_num, type(pitch_control_dict))
    if player_num:
        surface = pitch_control_dict[frame_num]['PPCFa_pax'][str(player_num)]
    else:
        surface = pitch_control_dict[frame_num]['PPCFa']
    trace = go.Heatmap(
        z=surface,
        x=pitch_control_dict.get(frame_num)['xgrid'],
        y=pitch_control_dict.get(frame_num)['ygrid'],
        colorscale='RdBu_r', opacity=0.8,
        zsmooth='best', zmin=0., zmax=1.,
        # showlegend=False,
        colorbar={'len': 0.3, 'thickness':10, 'x':0.9},
        showscale=False

    )
    # trace = go.Surface(
    # z=surface,
    # colorscale='RdBu_r', opacity=0.8,
    # cmin=0, cmax=1
    # )
    return [trace]


def generate_data_for_frame(tracking_home, tracking_away, pitch_control_dict,frame_num, show_velocities=True, player_num=None):
    hometeam = tracking_home.loc[frame_num]
    awayteam = tracking_away.loc[frame_num]
    tracking_data = (hometeam, awayteam)
    traces = []

    traces.extend(team_pitch_control(pitch_control_dict, frame_num, player_num=player_num))
    if show_velocities:
        traces.extend(velocities(tracking_data))

    traces.extend(positions(tracking_data))

    if hometeam['ball_x']:
        traces.extend(plot_ball(tracking_data))

    data = traces

    return data


@timing
def generate_plotly_frames_for_event(tracking_home, tracking_away, pitch_control_dict, tracking_frames, player_num=None):
    frames = []
    for frame_num in tqdm(tracking_frames):  # [::25]:
        # frame_num = str(frame_num)
        frame = {"data": [],
                 #  'traces': [0],
                 "name": frame_num}
        frame["data"].extend(generate_data_for_frame(tracking_home, tracking_away, pitch_control_dict, 
            frame_num=frame_num, player_num=player_num))
        # print (len(frame['data']))
        frames.append(frame)

    return frames


def generate_bar_data_for_frame(tracking_home, tracking_away, pitch_control_dict, frame_num):
    def get_pc(pid):
        pcs = pitch_control_dict[frame_num]['PPCFa_pax']
        if pid in pcs.keys():
            return pitch_control_dict[frame_num]['PPCFa_pax'][pid].mean()
        else:
            return 0
    hometeam = tracking_home
    awayteam = tracking_away
    # pick only the columns representing players whose data is available for this match
    homeplayers = [c[:-1] for c in hometeam[[c for c in hometeam.columns if c.startswith(
        'Home') & c.endswith('_x')]].dropna(1).columns]
    awayplayers = [c[:-1] for c in awayteam[[c for c in awayteam.columns if c.startswith(
        'Away') & c.endswith('_x')]].dropna(1).columns]

    for p in homeplayers:
        hometeam[p+'_speed_max'] = hometeam[p+'speed'].cummax()
    for p in awayplayers:
        awayteam[p+'_speed_max'] = awayteam[p+'speed'].cummax()

    hometeam = hometeam.loc[frame_num]
    velocity_indices = [c for c in hometeam.index if c.endswith('speed')]
    max_velocity_indices = [
        c for c in hometeam.index if c.endswith('speed_max')]
    homespeeds = hometeam[velocity_indices].dropna().reset_index()
    homespeeds = pd.concat([hometeam[velocity_indices].dropna(
    ).reset_index(), hometeam[max_velocity_indices].reset_index()], axis=1)
    homespeeds['player'] = homespeeds.iloc[:, 0].apply(
        lambda x: 'HP{}'.format(x.split('_')[1]))
    homespeeds['side'] = 'Home'
    homespeeds['color'] = '#c8102E'
    homespeeds = homespeeds.iloc[:, [4, 1, 3, 5, 6]]
    homespeeds.columns = ['player', 'speed', 'speed_max', 'side', 'color']
    homespeeds['PC'] = homespeeds['player'].apply(
        lambda x: -10*pitch_control_dict[frame_num]['PPCFa_pax'][x[2:]].mean())

    awayteam = awayteam.loc[frame_num]
    velocity_indices = [c for c in awayteam.index if c.endswith('speed')]
    max_velocity_indices = [
        c for c in awayteam.index if c.endswith('speed_max')]
    awayspeeds = awayteam[velocity_indices].dropna().reset_index()
    awayspeeds = pd.concat([awayteam[velocity_indices].dropna(
    ).reset_index(), awayteam[max_velocity_indices].reset_index()], axis=1)
    awayspeeds['player'] = awayspeeds.iloc[:, 0].apply(
        lambda x: 'AP{}'.format(x.split('_')[1]))
    awayspeeds['side'] = 'Away'
    awayspeeds['color'] = '#2196f3'
    awayspeeds = awayspeeds.iloc[:, [4, 1, 3, 5, 6]]
    awayspeeds.columns = ['player', 'speed', 'speed_max', 'side', 'color']
    awayspeeds['PC'] = 0

    speeds = homespeeds.append(awayspeeds)
    # print (speeds)
    trace0 = go.Bar(x=speeds.player, y=speeds.speed,
                    marker_color=speeds.color, name='speeds')
    trace1 = go.Bar(x=speeds.player, y=speeds.PC,
                    marker_color='indianred', name='pitch-control x 10')
    trace2 = go.Bar(x=speeds.player, y=[0.2 for s in speeds.player], base=speeds.speed_max,
                    marker_color="#4caf50", marker_line_width=1, marker_line_color='#212121', name='speed_max')
    data = [trace0, trace1, trace2]

    return data


def generate_bar_layout():
    layout = go.Layout(title='Player velocities for Liverpool & opposition',
                       xaxis_tickfont_size=14,
                       yaxis=dict(
                           title='Pitch Control <--|--> Speed (m/s)',
                           titlefont_size=16,
                           tickfont_size=14,
                       ),
                       legend=dict(
                           x=1,
                           y=1.0,
                           bgcolor='rgba(255, 255, 255, 0)',
                           bordercolor='rgba(255, 255, 255, 0)'
                       ),
                       autosize=True,
                       width=800,
                       height=400,
                       #    margin=dict(
                       #        l=100,
                       #        r=100,
                       #        b=100,
                       #        t=100,
                       #        pad=4
                       #    ),
                       barmode='overlay',
                       #     bargap=0.15, # gap between bars of adjacent location coordinates.
                       #     bargroupgap=0.1 # gap between bars of the same location coordinate.
                       )
    return layout


@timing
def plot_pitch_slider(event_start_frame=LIV_GOALS[MATCH]['START'],
                      event_end_frame=LIV_GOALS[MATCH]['END'],
                      field_dimen=(106.0, 68.0), data=None, frame=None):
    tracking_frames = range(event_start_frame, event_end_frame+1)
    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }
    fig_dict['layout'] = generate_pitch_layout(
        tracking_frames)
    fig_dict['data'] = generate_data_for_frame(frame_num=event_start_frame)
    fig_dict['frames'] = generate_plotly_frames_for_event(tracking_frames)

    # fig = go.Figure(fig_dict)

    # fig.show()

    # https://anvil.works/forum/t/serialization-of-graph-objects/4134/2
    with open('../datahub/lastrow/{}_fig_dict_white.pickle'.format(LIV_GOALS[MATCH]['PLAY']), 'wb') as handle:
        cloudpickle.dump(fig_dict, handle,
                         protocol=cloudpickle.DEFAULT_PROTOCOL)
        handle.close()
    # return fig_dict

def load_data():
    # goals_dict = {}
    # fig_dicts = {}
    # for goal in tqdm(LIV_GOALS):
    play = LIV_GOALS[MATCH]['PLAY']
    
    tracking_home, tracking_away, events = populate_LIV_tracking_dataframes()
    with open("../datahub/lastrow/{}_pc_dict.pkl".format(play), "rb") as handle:
        pitch_control_dict = pickle.load(handle)
        handle.close()
    
    # goals_dict[play] = tracking_home, tracking_away, events, pitch_control_dict

    # with open('../datahub/lastrow/{}_fig_dict_green.pickle'.format(play), 'rb') as handle:
    #     fig_dicts[play]['green']  = cloudpickle.load(handle)
    #     handle.close()

    # with open('../datahub/lastrow/{}_fig_dict_white.pickle'.format(play), 'rb') as handle:
    #     fig_dicts[play]['white'] = cloudpickle.load(handle)
    #     handle.close()

    # with open('../datahub/lastrow/{}_fig_dict_white_scorer.pickle'.format(play), 'rb') as handle:
    #     fig_dicts[play]['scorer'] = cloudpickle.load(handle)
    #     handle.close()

    return tracking_home, tracking_away, events, pitch_control_dict
        
        
        
