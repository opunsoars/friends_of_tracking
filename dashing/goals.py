import dash
import dash_core_components as dcc
import dash_html_components as html
from helper import plot_pitch_slider
import cloudpickle
from params import LIV_GOALS

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# tracking_home, tracking_away, events = populate_tracking_dataframes()
# 52696 - 53075
# fig_dict = plot_pitch_slider(
#     # event_start_frame=52696,
#     # event_end_frame=53075,
#     # tracking_home=tracking_home,
#     # tracking_away=tracking_away
# )

MATCH = 0
print('MATCH: {}\nPLAY: {}\n{} frames'.format(MATCH,
                                              LIV_GOALS[MATCH]['PLAY'],
                                              LIV_GOALS[MATCH]['END']+1
                                              ))
with open('../output/fig_dict_{}.pickle'.format(LIV_GOALS[MATCH]['PLAY']), 'rb') as handle:
    fig_dict = cloudpickle.load(handle)
    handle.close()


app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig_dict
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
