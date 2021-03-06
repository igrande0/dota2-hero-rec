#usr/bin/env python

""" Create a player profile for every
    given user ID in the input file.
"""

from __future__ import division
import sys
import json
import requests
from mrjob.job import MRJob
from math import sqrt
from time import sleep
from random import randint

STEAM_KEYS = ["CCAFC265C13500E30C9E8BC6E04EEE9C",
              "495726C265823513DE44E1A10C1D061E",
              "E9C49E6B7C47C4EDC79035934218E485",
              "16A5E8AE2F16B01E6D10FD205EC44D66",
              "54821F4A31BFCDA4D1D9339B91378FD1",
              "70E60BD29BA287460C4DA514D264E384",
              "90E84D0E6A277AA99A4A73DE03E443DB",
              "6E43467AE9F14E0037C9102F6B25C3CF",
              "48344009AA3726BD418876A49E3A3398"]

def success_rating(won, lost):
# a success rating that considers win/loss ratio along with # of games return
# normalized between 0 and 100%
    return (((won + 1.9208) / (won + lost) \
            - 1.96 * sqrt(((won * lost) / (won + lost)) + 0.9604) \
            / (won + lost)) / (1 + 3.8416 / (won + lost)))*100

def get_key():
    return STEAM_KEYS[randint(0, len(STEAM_KEYS)-1)]


class ProfileCreator(MRJob):

    def mapper_get_matches(self, _, user_id):
    # for each user, yeild all matches: (user_id, match_id)
        history_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/'
        history_params = dict(key=get_key(), min_players=10, account_id=int(user_id)+76561197960265728)

        current_match = 1
        last_match_id = 0

        while(True):
            # get the next 100 matches
            resp = requests.get(url=history_url, params=history_params)
            match_history = {}
            bad_count = 0

            while(True):
                try:
                    match_history = json.loads(resp.text)
                    if(len(match_history) == 0):
                        history_params['key'] = get_key()
                        details_resp = requests.get(url=details_url, params=details_params)
                        continue
                    break
                except ValueError:
                    print >> sys.stderr, "Caught match history ValueError - invalid JSON:"
                    print >> sys.stderr, resp.text
                    history_params['key'] = get_key()
                    resp = requests.get(url=history_url, params=history_params)
                    bad_count += 1
                    # lots of errors returned, so wait 10 seconds
                    if(bad_count > 5):
                        sleep(10)
                        bad_count = 0

            # user's profile is private
            if match_history['result']['status'] == 15:
                return

            for match in match_history['result']['matches']:
                # the last match of the previous page is the first match of the current page
                if 'start_at_match_id' in history_params and \
                   history_params['start_at_match_id'] == match['match_id']:
                    continue

                # for getting the next page of matches
                current_match +=1
                history_params['start_at_match_id'] = match['match_id']

                yield user_id, match['match_id']

            if(match_history['result']['results_remaining'] == 0):
                break

    def mapper_get_match_details(self, user_id, match_id):
    # for each match, yeild hero details:
    # (user_id, {"hero_name:" {"matches": ,"won": , "kills":, "deaths": , "assists": }})
        details_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'
        details_params = dict(key=get_key(), account_id=int(user_id)+76561197960265728, match_id=match_id)

        details_resp = requests.get(url=details_url, params=details_params)
        match_details = {}
        bad_count = 0

        while(True):
            try:
                match_details = json.loads(details_resp.text)
                if(len(match_details) == 0):
                    details_params['key'] = get_key()
                    details_resp = requests.get(url=details_url, params=details_params)
                    continue
                break
            except ValueError:
                print >> sys.stderr, "Caught match details ValueError - invalid JSON:"
                print >> sys.stderr, details_resp.text
                details_params['key'] = get_key()
                details_resp = requests.get(url=details_url, params=details_params)
                bad_count += 1
                # lots of errors returned, so wait 10 seconds
                if(bad_count > 5):
                    sleep(10)
                    bad_count = 0

        heroes = {}

        radiant_win = match_details['result']['radiant_win']
        for player in match_details['result']['players']:
            if player['account_id'] == int(user_id):
                if player['leaver_status'] != 0:
                    break

                hero_id = player['hero_id']
                heroes[hero_id] = heroes.get(hero_id, {})
                if (radiant_win == True and player['player_slot'] < 5) or \
                   (radiant_win == False and player['player_slot'] > 5):
                    heroes[hero_id]['won'] = 1
                else:
                    heroes[hero_id]['won'] = 0
                heroes[hero_id]['matches'] = 1
                heroes[hero_id]['kills'] = player['kills']
                heroes[hero_id]['deaths'] = player['deaths']
                heroes[hero_id]['assists'] = player['assists']

        yield user_id, heroes
        

    def reducer_compile_hero_stats(self, user_id, heroes):
    # for each user_id, compile details. yeild:
    # (user_id, {"hero_name:" {"matches": ,"won": , "kills":, "deaths": , "assists": }},
    #           {"hero_name:" {"matches": ,"won": , "kills":, "deaths": , "assists": }}, 
    #           ...)
        all_heroes = {}

        for hero_item in heroes:
            for hero_id, stats in hero_item.iteritems():
                all_heroes[hero_id] = all_heroes.get(hero_id, {})
                all_heroes[hero_id]['matches'] = all_heroes[hero_id].get('matches', 0) + stats['matches']
                all_heroes[hero_id]['won'] = all_heroes[hero_id].get('won', 0) + stats['won']
                all_heroes[hero_id]['kills'] = all_heroes[hero_id].get('kills', 0) + stats['kills']
                all_heroes[hero_id]['deaths'] = all_heroes[hero_id].get('deaths', 0) + stats['deaths']
                all_heroes[hero_id]['assists'] = all_heroes[hero_id].get('assists', 0) + stats['assists']

        yield user_id, all_heroes

        
    def reducer_normalize_hero_stats(self, user_id, heroes):
    # for each user_id, normalize details. yeild:
    # (user_id, {"hero_name:" {"matches": ,"won": , "win_perc": , "kda":, "success": }},
    #           {"hero_name:" {"matches": ,"won": , "win_perc": , "kda":, "success": }}, 
    #           ...)
        norm_heroes = {}

        for hero_item in heroes:
            for hero_id, stats in hero_item.iteritems():
                norm_heroes[hero_id] = norm_heroes.get(hero_id, {})
                norm_heroes[hero_id]['matches'] = stats['matches']
                norm_heroes[hero_id]['won'] = stats['won']
                norm_heroes[hero_id]['win_perc'] = stats['won'] / stats['matches']
                if stats['deaths'] != 0:
                    norm_heroes[hero_id]['kda'] = (stats['kills'] + stats['assists']) / stats['deaths']
                else:
                    norm_heroes[hero_id]['kda'] = (stats['kills'] + stats['assists'])
                norm_heroes[hero_id]['success'] = success_rating(stats['won'], stats['matches'] - stats['won'])
        
        yield user_id, norm_heroes

    def steps(self):
        return [
            self.mr(mapper=self.mapper_get_matches),
            self.mr(mapper=self.mapper_get_match_details,
                    reducer=self.reducer_compile_hero_stats),
            self.mr(reducer=self.reducer_normalize_hero_stats)
        ]
        


if __name__ == "__main__":
    ProfileCreator().run()
