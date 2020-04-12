If you use these data cite the following papers:

- Pappalardo et al., (2019) **A public data set of spatio-temporal match events in soccer competitions**, Nature Scientific Data 6:236, https://www.nature.com/articles/s41597-019-0247-7

- Pappalardo et al. (2019) **PlayeRank: Data-driven Performance Evaluation and Player Ranking in Soccer via a Machine Learning Approach.** ACM Transactions on Intellingent Systems and Technologies (TIST) 10, 5, Article 59 (September 2019), 27 pages. DOI: https://doi.org/10.1145/3343172


The PlayeRank score of the players in the matches they played. The PlayeRank score indicate, in a range from 0 to 1, how good was that player in that match (0 unforgettably bad, 1 amazing). The score have been computed using the PlayeRank framework, if you use these data please cite the following paper: https://arxiv.org/abs/1802.04987.

Each document in the json file has the following fields:

- **goalScored**: the number of goals scored by the player in the match
- **playerankScore**: the PlayeRank score of the player in the match
- **matchId**: the identifier of the match
- **playerId**: the identifier of the player
- **roleCluster**: the role of player in the match, as computed by the PlayeRank framework
- **minutesPlayed**: the minutes played by the player in the match

[Source](https://figshare.com/articles/PlayeRanks/9361148)