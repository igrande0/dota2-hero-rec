#!/usr/bin/python
from __future__ import division
import json #or cjson
import re
import time
from math import sqrt

class PlayerComparison():
   
    def cosine(self, user_profile, player_profiles):
    # returns {"user_id:", similarity score} 
        norm_user_scores = {}
        player_scores = {}

        # normalize the user's scores
        sumOfSquares = float(0)
        for hero, stats in user_profile.iteritems():
        	norm_user_scores[hero] = stats['success']
        	sumOfSquares += stats['success']**2
        for hero, stats in user_profile.iteritems():
        	norm_user_scores[hero] /= sqrt(sumOfSquares)

        # calculate the scores
        for user_id, hero_stats in player_profiles.iteritems():
        	sumOfSquares = float(0)
        	score = float(0)

        	for hero_id, stats in hero_stats.iteritems():
        		if hero_id in norm_user_scores:
        			score += norm_user_scores[hero_id]*stats['success']
        		sumOfSquares += stats['success']**2

        	score /= sqrt(sumOfSquares)
        	player_scores[user_id] = score

        return player_scores

    def getNearestNeighbors(self, scores, k):
    # returns a list of user_ids
    	score_list = []

        for user_id, score in scores.iteritems():
            if score != 1:
                score_list.append((score, user_id))

        score_list.sort(reverse=True)

        return [item[1] for item in score_list[:k]]

    def average(self, player_profiles):
    	agg_player = {}
    	hero_total = {}

        for user_id, hero_profile in player_profiles.iteritems():
            for hero, stats in hero_profile.iteritems():
                if stats['matches'] < 10:
                    continue
                agg_player[hero] = agg_player.get(hero, {})
                agg_player[hero]['kda'] = agg_player[hero].get('kda', 0) + stats['kda']
                agg_player[hero]['success'] = agg_player[hero].get('success', 0) + stats['success']
                agg_player[hero]['win_perc'] = agg_player[hero].get('win_perc', 0) + stats['win_perc']
                hero_total[hero] = hero_total.get(hero, 0) + 1

    	for hero in agg_player.keys():
            agg_player[hero]['kda'] /= hero_total[hero]
            agg_player[hero]['success'] /= hero_total[hero]
            agg_player[hero]['win_perc'] /= hero_total[hero]

        return agg_player

    def returnUnplayedHeroes(self, user_profile, agg_player):
    # returns {'hero_id': {hero stats}}
    	unplayed_heroes = []

    	for hero, stats in user_profile.iteritems():
    		if hero in agg_player:
    			del agg_player[hero]

    	for hero, stats in agg_player.iteritems():
    		unplayed_heroes.append((stats['success'], {hero: stats}))

    	return unplayed_heroes

if __name__ == '__main__':
    startTime = time.time()
    userProfile = {}
    playerProfiles = {}
    heroesDict = {}
    heroesFormattedDict = {}
    nearestPlayerProfiles = {}

    for line in open('iggyzizzleProfile.json'):
        profile = re.split(r'\t+', line)
        userProfile = json.loads(profile[1])
    for line in open('crawler/playerProfiles1.json'):
        profile = re.split(r'\t+', line)
        profile[0] = profile[0].strip('"')
        playerProfiles[profile[0]] = json.loads(profile[1])
    for line in open('crawler/playerProfiles2.json'):
        profile = re.split(r'\t+', line)
        profile[0] = profile[0].strip('"')
        playerProfiles[profile[0]] = json.loads(profile[1])
    
    hero_file = open('heroes.json')
    heroes_list = json.load(hero_file)
    for item in heroes_list['heroes']:
        heroesDict[item['id']] = item['localized_name']
        heroesFormattedDict[item['id']] = re.sub('npc_dota_hero_', '', item['name'])

    comparer = PlayerComparison()
    scores = comparer.cosine(userProfile, playerProfiles)
    # neighbors is a list of user_ids
    neighbors = comparer.getNearestNeighbors(scores, 500)

    # get hero profiles for nearest neighbors
    for neighbor in neighbors:
        if neighbor in playerProfiles:
            nearestPlayerProfiles[neighbor] = playerProfiles[neighbor]

    agg_player = comparer.average(nearestPlayerProfiles)
    unplayed_heroes = comparer.returnUnplayedHeroes(userProfile, agg_player)

    # print top unplayed heroes
    output = []
    unplayed_heroes.sort(reverse = True)
    #print "\n\n=======================TOP 5 UNPLAYED HEROES======================="
    for item in unplayed_heroes[:5]:
        for hero_id, stats in item[1].iteritems():
            dictionary = dict()
            dictionary['formatted_name'] = heroesFormattedDict[int(hero_id)]
            dictionary['hero_name'] = heroesDict[int(hero_id)]
            dictionary['hero_link'] = re.sub(' ', '_', heroesDict[int(hero_id)])
            dictionary['hero_id'] = hero_id
            dictionary['win_perc'] = int(round(stats['win_perc'] * 100, 0))
            dictionary['kda'] = round(stats['kda'], 2)
            output.append(dictionary)
            #print dictionary['hero_name']
            #print "Predicted win percentage: " + str(dictionary['win_perc']) + '%'
            #print "Predicted Kill/Death/Assist ratio: " + str(dictionary['kda']) + '\n'
    
    print json.dumps(output, separators=(',',':'))

    #print("execution time: %f seconds" % (time.time()-startTime))
