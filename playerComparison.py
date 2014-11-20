#!/usr/bin/python
from __future__ import division
import json #or cjson
import re
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
        	sumOfSquares = stats['success']**2
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
            score_list.append((score, user_id))

        score_list.sort(reverse=True)

        return [item[1] for item in score_list[:k]]

    def average(self, player_profiles):
    	agg_player = {}
    	hero_total = {}

        for user_id, hero_profile in player_profiles.iteritems():
            for hero, stats in hero_profile.iteritems():
                agg_player[hero] = agg_player.get(hero, {})
                agg_player[hero]['kda'] = stats['kda']
                agg_player[hero]['success'] = stats['success']
                agg_player[hero]['win_perc'] = stats['win_perc']
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
    userProfile = {}
    playerProfiles = {}
    heroesDict = {}
    nearestPlayerProfiles = {}

    for line in open('iggyzizzleProfile.json'):
        profile = re.split(r'\t+', line)
        userProfile = json.loads(profile[1])
    for line in open('crawler/playerProfiles.json'):
        profile = re.split(r'\t+', line)
        profile[0] = profile[0].strip('"')
        playerProfiles[profile[0]] = json.loads(profile[1])
    
    hero_file = open('heroes.json')
    heroes_list = json.load(hero_file)
    for item in heroes_list['heroes']:
        heroesDict[item['id']] = item['localized_name']

    comparer = PlayerComparison()
    scores = comparer.cosine(userProfile, playerProfiles)
    # neighbors is a list of user_ids
    neighbors = comparer.getNearestNeighbors(scores, 3)

    # get hero profiles for nearest neighbors
    for neighbor in neighbors:
        if neighbor in playerProfiles:
            nearestPlayerProfiles[neighbor] = playerProfiles[neighbor]

    agg_player = comparer.average(nearestPlayerProfiles)
    unplayed_heroes = comparer.returnUnplayedHeroes(userProfile, agg_player)

    # print top unplayed heroes
    unplayed_heroes.sort(reverse = True)
    print "\n\n=======================TOP 5 UNPLAYED HEROES======================="
    for item in unplayed_heroes[:5]:
        for hero_id, stats in item[1].iteritems():
            print heroesDict[int(hero_id)]
            print "Predicted win percentage: " + str(int(round(stats['win_perc'] * 100, 0))) + '%'
            print "Predicted Kill/Death/Assist ratio: " + str(round(stats['kda'], 2)) + '\n'
