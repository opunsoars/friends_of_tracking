
DATA_DIR = '../datahub/metrica_sports/sample-data/data'
MATCH_ID = 2

GOALVID19_ATT = '../src/friends_of_tracking/Last-Row/datasets/positional_data/GOALVID19_tracking_attack.csv'
GOALVID19_DEF = '../src/friends_of_tracking/Last-Row/datasets/positional_data/GOALVID19_tracking_defence.csv'

'''
pd.DataFrame([[play, 
               data_attack.loc[play,'score'][0],
               data_attack.loc[play].index[0], 
               data_attack.loc[play].index[-1]] for play in data_attack.index.get_level_values(0).unique()], columns=['PLAY','SCORE','START','END']).to_dict(orient='records')
'''
MATCH = 2
SCORER=False
LIV_GOALS = [{'PLAY': 'Bayern 0 - [1] Liverpool',
              'SCORE': 'BAY 0 [1] LIV',
              'START': 0,
              'END': 164},
             {'PLAY': 'Bournemouth 0 - 3 Liverpool',
              'SCORE': 'BOU 0 [3] LIV',
              'START': 0,
              'END': 170},
             {'PLAY': 'Fulham 0 - [1] Liverpool',
              'SCORE': 'FUL 0 [1] LIV',
              'START': 0,
              'END': 182},
             {'PLAY': 'Genk 0 - [3] Liverpool',
              'SCORE': 'GNK 0 [3] LIV',
              'START': 0,
              'END': 182},
             {'PLAY': 'Leicester 0 - [3] Liverpool',
              'SCORE': 'LEI 0 [3] LIV',
              'START': 0,
              'END': 124},
             {'PLAY': 'Liverpool [1] - 0 Everton',
              'SCORE': 'LIV [1] 0 EVE',
              'START': 0,
              'END': 198},
             {'PLAY': 'Liverpool [1] - 0 Watford',
              'SCORE': 'LIV [1] 0 WAT',
              'START': 0,
              'END': 224},
             {'PLAY': 'Liverpool [1] - 0 Wolves',
              'SCORE': 'LIV [1] 0 WLV',
              'START': 0,
              'END': 156},
             {'PLAY': 'Liverpool [2] - 0 Everton',
              'SCORE': 'LIV [2] 0 EVE',
              'START': 0,
              'END': 286},
             {'PLAY': 'Liverpool [2] - 0 Man City',
              'SCORE': 'LIV [2] 0 MCI',
              'START': 0,
              'END': 166},
             {'PLAY': 'Liverpool [2] - 0 Porto',
              'SCORE': 'LIV [2] 0 POR',
              'START': 0,
              'END': 194},
             {'PLAY': 'Liverpool [2] - 0 Salzburg',
              'SCORE': 'LIV [2] 0 RBS',
              'START': 0,
              'END': 190},
             {'PLAY': 'Liverpool [2] - 1 Chelsea',
              'SCORE': 'LIV [2] 1 CHE',
              'START': 0,
              'END': 194},
             {'PLAY': 'Liverpool [2] - 1 Newcastle',
              'SCORE': 'LIV [2] 1 NEW',
              'START': 0,
              'END': 148},
             {'PLAY': 'Liverpool [3] - 0 Bournemouth',
              'SCORE': 'LIV [3] 0 BOU',
              'START': 0,
              'END': 154},
             {'PLAY': 'Liverpool [3] - 0 Norwich',
              'SCORE': 'LIV [3] 0 NOR',
              'START': 0,
              'END': 148},
             {'PLAY': 'Liverpool [4] - 0 Barcelona',
              'SCORE': 'LIV [4] 0 FCB',
              'START': 0,
              'END': 138},
             {'PLAY': 'Porto 0 - [2] Liverpool',
              'SCORE': 'POR 0 [2] LIV',
              'START': 0,
              'END': 256},
             {'PLAY': 'Southampton 1 - [2] Liverpool',
              'SCORE': 'SOU 1 [2] LIV',
              'START': 0,
              'END': 256}]

# PITCH VIZ PARAMS
FIELD_WIDTH=1000
FIELD_HEIGHT=700
FIELD_DIM = (106.0, 68.0)

# FIELD_COLOR = 'mediumseagreen'
# FIELD_MARKINGS_COLOR = 'White'

FIELD_COLOR = 'White'
FIELD_MARKINGS_COLOR = 'black'


PLAYERMARKERSIZE = 20
player_marker_args = {'Home': dict(mode='markers+text',
                                   marker_size=PLAYERMARKERSIZE,
                                   marker_line_color="white",
                                   marker_color="red",
                                   marker_line_width=2,
                                   textfont=dict(
                                        size=11,
                                        color="white"
                                   )),
                      'Away': dict(mode='markers+text',
                                   marker_size=PLAYERMARKERSIZE,
                                   marker_line_color="white",
                                   marker_color="#0570b0",
                                   marker_line_width=2,
                                   textfont=dict(
                                        size=11,
                                        color="white"
                                   ))}

event_player_marker_args = {'Home': dict(mode='lines+markers+text',
                                         marker_size=PLAYERMARKERSIZE,
                                         marker_line_color="white",
                                         marker_color="red",
                                         marker_line_width=2,
                                         line_color="red",
                                         textfont=dict(
                                             size=11,
                                             color="white"
                                         )),
                            'Away': dict(mode='lines+markers+text',
                                         marker_size=PLAYERMARKERSIZE,
                                         marker_line_color="white",
                                         marker_color="#0570b0",
                                         marker_line_width=2,
                                         line_color="#0570b0",
                                         textfont=dict(
                                             size=11,
                                             color="white"
                                         ))}

SCORES = ['BAY 0 [1] LIV',
          'BOU 0 [3] LIV',
          'FUL 0 [1] LIV',
          'GNK 0 [3] LIV',
          'LEI 0 [3] LIV',
          'LIV [1] 0 EVE',
          'LIV [1] 0 WAT',
          'LIV [1] 0 WLV',
          'LIV [2] 0 EVE',
          'LIV [2] 0 MCI',
          'LIV [2] 0 POR',
          'LIV [2] 0 RBS',
          'LIV [2] 1 CHE',
          'LIV [2] 1 NEW',
          'LIV [3] 0 BOU',
          'LIV [3] 0 NOR',
          'LIV [4] 0 FCB',
          'POR 0 [2] LIV',
          'SOU 1 [2] LIV']
