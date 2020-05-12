from helper import *
import cloudpickle
from params import LIV_GOALS, MATCH

# generate for 1P or allP and save in ../datahub/lastrow
# generate green for allP and white for 1P / allP

# MATCH = 0
PLAYER = LIV_GOALS[MATCH]['PLAYER']# GOALSCORER #None
PLAY = LIV_GOALS[MATCH]['PLAY']
event_start_frame = LIV_GOALS[MATCH]['START']
event_end_frame = LIV_GOALS[MATCH]['END']
print(MATCH, PLAY)

# load data pkl for the match
tracking_home, tracking_away, events, pitch_control_dict = load_data()
tracking_frames = range(event_start_frame, event_end_frame+1)


fname = '../datahub/lastrow/figs/{}.pkl'.format(PLAY)

hmap_dict = {'white': {"data": [],
                       "layout": {},
                       "frames": []},
             'white_scorer': {"data": [],
                              "layout": {},
                              "frames": []}}  # no green
bar_dict = {frame_num: {'data': [], 'layout': {}}
            for frame_num in tracking_frames}


hmap_dict['white']['layout'] = generate_pitch_layout()
hmap_dict['white']['data'] = generate_data_for_frame(
    tracking_home, tracking_away, pitch_control_dict, frame_num=event_start_frame)
hmap_dict['white']['frames'] = generate_plotly_frames_for_event(
    tracking_home, tracking_away, pitch_control_dict, tracking_frames)

hmap_dict['white_scorer']['layout'] = hmap_dict['white']['layout']
hmap_dict['white_scorer']['data'] = generate_data_for_frame(
    tracking_home, tracking_away, pitch_control_dict, frame_num=event_start_frame, player_num=PLAYER)
hmap_dict['white_scorer']['frames'] = generate_plotly_frames_for_event(
    tracking_home, tracking_away, pitch_control_dict, tracking_frames, player_num=PLAYER)

for frame_num in tqdm(tracking_frames):
    bar_dict[frame_num]['data'] = generate_bar_data_for_frame(
        tracking_home, tracking_away, pitch_control_dict, frame_num)
    bar_dict[frame_num]['layout'] = generate_bar_layout()


dash_dict = {'hmap': hmap_dict,
             'bar': bar_dict}


with open(fname, 'wb') as handle:
    cloudpickle.dump(dash_dict, handle,
                     protocol=cloudpickle.DEFAULT_PROTOCOL)
    handle.close()


# # make figure
# fig_dict = {
#     "data": [],
#     "layout": {},
#     "frames": []
# }
# fig_dict['layout'] = generate_pitch_layout()
# if PLAYER:
#     fig_dict['data'] = generate_data_for_frame(
#         frame_num=event_start_frame, player_num=PLAYER)
#     fig_dict['frames'] = generate_plotly_frames_for_event(
#         tracking_frames, player_num=PLAYER)
#     fname = '../datahub/lastrow/{}_fig_dict_white_scorer.pickle'.format(
#         LIV_GOALS[MATCH]['PLAY'])
# else:
#     fig_dict['data'] = generate_data_for_frame(frame_num=event_start_frame)
#     fig_dict['frames'] = generate_plotly_frames_for_event(tracking_frames)
#     fname = '../datahub/lastrow/{}_fig_dict_white.pickle'.format(
#         LIV_GOALS[MATCH]['PLAY'])

# with open(fname, 'wb') as handle:
#     cloudpickle.dump(fig_dict, handle,
#                      protocol=cloudpickle.DEFAULT_PROTOCOL)
#     handle.close()
