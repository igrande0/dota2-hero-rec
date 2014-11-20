D2REC README
==============


Team Members: Patrick Knauth, Isaac Grande, Adrien Mombo-Caristan


##DEPENDENCIES:

- Three JSON files are used by playerComparison.py:
  - crawler/playerProfiles.json - Contains the JSON database of crawled player profiles
  - iggyzizzleProfile.json - Contains a single, hard-coded player profile for recommendation
  - heroes.json - List of hero names for each hero ID.


##PROGRAM EXECUTION:

- To run the demo script input following command to command-line:
	"python playerComparison.py"
- Output is a list of the top 5 unplayed heroes sorted by the user's predicted success. 



##ALGORITHM DESCRIPTION:

For the purposes of this demo release, PlayerRecommender.py finds the cosine similarity score
between a single, hard-coded, user (iggyzizzleProfile.json) and other crawled users (crawler/playerProfiles.json)
from our larger repository of collected player profiles, using a calculated success rate of each players' heroes as terms.
The success is calculated considering the winrate and number of matches played by using the lower bound of a Wilson Score
Confidence Interval for a Bernoulli parameter. The top 100 gamer profiles that are most similar to iggyzizzle are combined into an aggregate player which holds the predicted success of all of the heroes. The heroes of the aggregate player
are used to recommend unplayed heroes of the user (iggyzizzle) sorted by success. The top 5 heroes are then presented
along with their predicted win percentage and kill/death/assist ratio.

In the final implementation we plan to, depending on the input of the user, output a list of 
the best heroes not yet played by the user or a list of best heroes overall (played/non-played)
will be recommended, each with a predicted win percentage and a predicted kill/death/assist 
ratio.

Time consideration: In running the python script during testing, the program typically ran
for ~30 seconds.
