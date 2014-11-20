#!/usr/bin/python
from __future__ import division
import json #or cjson
import re
from stemming.porter2 import stem
from operator import itemgetter
from math import log
from collections import defaultdict
from math import sqrt

class PlayerComparison (Hw1):
   
    def cosine(self, user_profile, player_profiles):
    # returns {"user_id:", similarity score} 
        norm_user_scores = {}
        player_scores = {}

        # normalize the user's scores
        sumOfSquares = float(0)
        for hero, stats in user_profile.itemgetter():
        	norm_user_scores[hero] = stats['success']
        	sumOfSquares = stats['success']**2
        for hero, stats in user_profile.itemgetter():
        	norm_user_scores[hero] /= sqrt(sumOfSquares)

        # calculate the scores
        for user_id, hero_stats in player_profiles:
        	sumOfSquares = float(0)
        	score = float(0)

        	for hero_id, stats in hero_stats.itemgetter():
        		if hero_id in norm_user_scores:
        			score += norm_user_scores[hero_id]*stats['success']
        		sumofSquares += stats['success']**2

        	score /= sqrt(sumOfSquares)
        	player_scores[user_id] = score

        return player_scores

    def getNearestNeighbors(self, scores, k):
    	# conver to a list, sort, then give back as a dict
    	pass

    def average(self, player_profiles):
    	agg_player = {}
    	hero_total = {}

    	for user_id, hero_profile in player_profiles:
    		for hero, stats in hero_profile:
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

		for hero, stats in user_profile:
			if hero in agg_player:
				del agg_player[hero]

		for hero, stats in agg_player:
			unplayed_heroes.append(stats['success'], {hero: stats})

		return unplayed_heroes

if __name__ == '__main__':
	userProfile = {}
	playerProfiles = {}

    comparer = PlayerComparison()
    scores = comparer.cosine(userProfile, playerProfiles)
    neighbors = comparer.getNearestNeighbors(scores, 10)
    agg_player = comparer.average(neighbors)
    unlayed_heroes = comparer.returnUnplayedHeroes(userProfile, agg_player)

    # nice printing for submission

