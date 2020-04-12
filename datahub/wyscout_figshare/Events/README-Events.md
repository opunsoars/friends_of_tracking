Further details on this file are in the following paper: https://www.nature.com/articles/s41597-019-0247-7. Please cite it if you use the data for your research or analyses.

This dataset describes all the events that occur during each match. Each event refers to a ball touch and contains the following information:

- **eventId**: the identifier of the event's type. Each eventId is associated with an event name (see next point);
- **eventName**: tteamIdhe name of the event's type. There are seven types of events: pass, foul, shot, duel, free kick, offside and touch;
- **subEventId**: the identifier of the subevent's type. Each subEventId is associated with a subevent name (see next point);
- **subEventName**: the name of the subevent's type. Each event type is associated with a different set of subevent types;
- **tags**: a list of event tags, each one describes additional information about the event (e.g., accurate). Each event type is associated with a different set of tags;
- **eventSec**: the time when the event occurs (in seconds since the beginning of the current half of the match);
- **id**: a unique identifier of the event;
- **matchId**: the identifier of the match the event refers to. The identifier refers to the field "wyId" in the match dataset;
- **matchPeriod**: the period of the match. It can be "1H" (first half of the match), "2H" (second half of the match), "E1" (first extra time), "E2" (second extra time) or "P" (penalties time);
- **playerId**: the identifier of the player who generated the event. The identifier refers to the field "wyId" in a player dataset;
- **positions**: the origin and destination positions associated with the event. Each position is a pair of coordinates (x, y). The x and y coordinates are always in the range [0, 100] and indicate the percentage of the field from the perspective of the attacking team. In particular, the value of the x coordinate indicates the event's nearness (in percentage) to the opponent's goal, while the value of the y coordinates indicates the event's nearness (in percentage) to the right side of the field;
- **teamId**: the identifier of the player's team. The identifier refers to the field "wyId" in the team dataset.

[Source](https://figshare.com/articles/Events/7770599)