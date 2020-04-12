This dataset describes all the matches made available. Each match is a document consisting of the following fields:

- **competitionId**: the identifier of the competition to which the match belongs to. It is a integer and refers to the field "wyId" of the competition document;
- **date and dateutc**: the former specifies date and time when the match starts in explicit format (e.g., May 20, 2018 at 8:45:00 PM GMT+2), the latter contains the same information but in the compact format YYYY-MM-DD hh:mm:ss;
- **duration**: the duration of the match. It can be "Regular" (matches of regular duration of 90 minutes + stoppage time), "ExtraTime" (matches with supplementary times, as it may happen for matches in continental or international competitions), or "Penalities" (matches which end at penalty kicks, as it may happen for continental or international competitions);
- **gameweek**: the week of the league, starting from the beginning of the league;
- **label**: contains the name of the two clubs and the result of the match (e.g., "Lazio - Internazionale, 2 - 3");
- **roundID**: indicates the match-day of the competition to which the match belongs to. During a competition for soccer clubs, each of the participating clubs plays against each of the other clubs twice, once at home and once away. The matches are organized in match-days: all the matches in match-day i are played before the matches in match-day i + 1, even tough some matches can be anticipated or postponed to facilitate players and clubs participating in Continental or Intercontinental competitions. During a competition for national teams, the "roundID" indicates the stage of the competition (eliminatory round, round of 16, quarter finals, semifinals, final);
- **seasonId**: indicates the season of the match;
- **status**: it can be "Played" (the match has officially finished), "Cancelled" (the match has been canceled for some reason), "Postponed" (the match has been postponed and no new date and time is available yet) or "Suspended" (the match has been suspended and no new date and time is available yet);
- **venue**: the stadium where the match was held (e.g., "Stadio Olimpico");
- **winner**: the identifier of the team which won the game, or 0 if the match ended with a draw;
- **wyId**: the identifier of the match, assigned by Wyscout;
- **teamsData**: it contains several subfields describing information about each team that is playing that match: such as lineup, bench composition, list of substitutions, coach and scores:
- **hasFormation**: it has value 0 if no formation (lineups and benches) is present, and 1 otherwise;
- **score**: the number of goals scored by the team during the match (not counting penalties);
- **scoreET**: the number of goals scored by the team during the match, including the extra time (not counting penalties);
- **scoreHT**: the number of goals scored by the team during the first half of the match;
- **scoreP**: the total number of goals scored by the team after the penalties;
- **side**: the team side in the match (it can be "home" or "away");
- **teamId**: the identifier of the team;
- **coachId**: the identifier of the team's coach;
- **bench**: the list of the team's players that started the match in the bench and some basic statistics about their performance during the match (goals, own goals, cards);
- **lineup**: the list of the team's players in the starting lineup and some basic statistics about their performance during the match (goals, own goals, cards);
- **substitutions**: the list of team's substitutions during the match, describing the players involved and the minute of the substitution.

[Source](https://figshare.com/articles/Matches/7770422)