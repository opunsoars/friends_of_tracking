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
def generate_pitch_layout(tracking_frames=None, field_dimen=(106.0, 68.0), field_color='green', linewidth=2, markersize=20):
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
                      x1=centre.x + centre_circle_radius, y1=centre.y + centre_circle_radius, line_color="White", layer="below")
    mid_line = dict(type="line",
                    x0=centre.x, y0=centre.y - half_pitch_width,
                    x1=centre.x, y1=centre.y + half_pitch_width, line_color="White", layer="below")
    mid_point = dict(type="circle",
                     x0=centre.x-0.4, y0=centre.y-0.4,
                     x1=centre.x+0.4, y1=centre.y+0.4, line_color="White", fillcolor='white', layer="below")
    shapes.extend([mid_circle, mid_line, mid_point])

    for s in signs:

        # plot pitch boundary
        boundary1 = dict(type="line",
                         x0=-half_pitch_length, y0=s*half_pitch_width,
                         x1=half_pitch_length, y1=s*half_pitch_width, line_color="White", layer="below")

        boundary2 = dict(type="line",
                         x0=s*half_pitch_length, y0=-half_pitch_width,
                         x1=s*half_pitch_length, y1=half_pitch_width, line_color="White", layer="below")

        circle = dict(type="circle",
                           x0=s*(centre.x+half_pitch_length-penalty_spot) - centre_circle_radius, y0=centre.y - centre_circle_radius,
                           x1=s*(centre.x+half_pitch_length-penalty_spot) + centre_circle_radius, y1=centre.y + centre_circle_radius, line_color="White", layer="below")

        patch = dict(type="rect",
                     x0=s*half_pitch_length, y0=-area_width/2. - 1,
                     x1=s*(half_pitch_length - area_length), y1=area_width/2. + 1, line=dict(color="mediumseagreen", width=0), fillcolor="mediumseagreen", layer="below")

        box = dict(type="rect",
                   x0=s*half_pitch_length, y0=-area_width/2.,
                   x1=s*(half_pitch_length - area_length), y1=area_width/2., line=dict(color="white", width=2), layer="below")
        D = dict(type="rect",
                 x0=s*half_pitch_length, y0=-box_width/2.,
                 x1=s*(half_pitch_length - box_length), y1=box_width/2., line=dict(color="white", width=2), layer="below")
        pen = dict(type="circle",
                   x0=s*(half_pitch_length - penalty_spot)-0.4, y0=-0.4,
                   x1=s*(half_pitch_length - penalty_spot)+0.4, y1=0.4, line_color="White", fillcolor='white', layer="below")

        top_post = dict(type="rect",
                        x0=s*half_pitch_length, y0=goal_line_width/2. - 0.5,
                        x1=s*(half_pitch_length-0.5), y1=goal_line_width/2.+0.5, line=dict(color="white", width=0), fillcolor="white", layer="below")

        bottom_post = dict(type="rect",
                           x0=s*half_pitch_length, y0=-goal_line_width/2. - 0.5,
                           x1=s*(half_pitch_length-0.5), y1=-goal_line_width/2.+0.5, line=dict(color="white", width=0), fillcolor="white", layer="below")

        shapes.extend([boundary1, boundary2, circle, patch,
                       box, D, pen, top_post, bottom_post])

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
            {"frame": {"duration": 0, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 0}
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
                                "fromcurrent": True, "transition": {"duration": 0,
                                                                    "easing": "quadratic-in-out"}}],
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
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0.1,
        "yanchor": "top"
    }

    # set axis limits
    xmax = field_dimen[0]/2. + border_dimen[0]
    ymax = field_dimen[1]/2. + border_dimen[1]

    layout = go.Layout(
        title='Goal: {}'.format(LIV_GOALS[MATCH]['PLAY']),
        hovermode='closest',
        autosize=False,
        width=1000,
        height=800,
        plot_bgcolor='mediumseagreen',
        xaxis=go.layout.XAxis(range=[-xmax, xmax],
                              showgrid=False, zeroline=False,
                              showticklabels=False
                              ),
        yaxis=go.layout.YAxis(range=[-ymax, ymax],
                              showgrid=False, zeroline=False,
                              showticklabels=False,
                              scaleanchor="x",
                              scaleratio=1,
                              ))

    layout["shapes"] = shapes
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
                       marker_size=10, marker_opacity=0.8, marker_color='#262e39', name='ball'
                       )
    return [trace]


tracking_home, tracking_away, events = populate_LIV_tracking_dataframes()


def generate_data_for_frame(frame_num, show_velocities=True):
    hometeam = tracking_home.loc[frame_num]
    awayteam = tracking_away.loc[frame_num]
    tracking_data = (hometeam, awayteam)
    traces = []

    if show_velocities:
        traces.extend(velocities(tracking_data))

    traces.extend(positions(tracking_data))

    if hometeam['ball_x']:
        traces.extend(plot_ball(tracking_data))

    data = traces

    return data


@timing
def generate_plotly_frames_for_event(tracking_frames):
    frames = []
    for frame_num in tqdm(tracking_frames):  # [::25]:
        frame = {"data": [], "name": str(frame_num)}
        frame["data"].extend(generate_data_for_frame(frame_num=frame_num))
        # print (len(frame['data']))
        frames.append(frame)

    return frames


@timing
def plot_pitch_slider(event_start_frame=LIV_GOALS[MATCH]['START'],
                      event_end_frame=LIV_GOALS[MATCH]['END'],
                      field_dimen=(106.0, 68.0), field_color='green',
                      linewidth=2, markersize=20, data=None, frame=None):
    tracking_frames = range(event_start_frame, event_end_frame+1)
    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }
    fig_dict['layout'] = generate_pitch_layout(
        tracking_frames, field_dimen=field_dimen, field_color=field_color, linewidth=linewidth, markersize=markersize)
    fig_dict['data'] = generate_data_for_frame(frame_num=event_start_frame)
    fig_dict['frames'] = generate_plotly_frames_for_event(tracking_frames)

    # with open('../output/fig_dict.json','w') as fp:
    #     json.dump(fig_dict, fp)
    # print ('dumped')
    # fig = go.Figure(fig_dict)

    # fig.show()

    # https://anvil.works/forum/t/serialization-of-graph-objects/4134/2
    with open('../output/fig_dict_{}.pickle'.format(LIV_GOALS[MATCH]['PLAY']), 'wb') as handle:
        cloudpickle.dump(fig_dict, handle,
                         protocol=cloudpickle.DEFAULT_PROTOCOL)
        handle.close()
    # return fig_dict
