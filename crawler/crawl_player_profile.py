""" Crawl a user's matches and compile data
"""

from __future__ import division

import sys

import json
import requests
from time import sleep

STEAM_KEY = 'CCAFC265C13500E30C9E8BC6E04EEE9C'

class UserCrawler():
    def __init__(self):
        self.history_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/'
        self.details_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'
        self.history_params = dict(key=STEAM_KEY, min_players=10)
        self.details_params = dict(key=STEAM_KEY)

    def getPlayerProfile(self, user_id):
        # to store the player's stats for each match
        player_profile = {}
        # add the offset to conver to 64 bit ID
        self.history_params['account_id'] = user_id + 76561197960265728
        current_match = 1

        last_match_id = 0
        while(True):
            # get the next 100 matches
            resp = requests.get(url=self.history_url, params=self.history_params)
            match_history = json.loads(resp.text)
            #sleep(1)

            # get relevant details for each match
            for match in match_history['result']['matches']:
                if 'start_at_match_id' in self.history_params and \
                   self.history_params['start_at_match_id'] == match['match_id']:
                    continue
                print >> sys.stderr, current_match
                current_match +=1
                # get match details
                self.details_params['match_id'] = match['match_id']
                self.history_params['start_at_match_id'] = match['match_id']
                details_resp = requests.get(url=self.details_url, params=self.details_params)
                match_details = json.loads(details_resp.text)
                #sleep(1)

                # save relevant match details
                relev_details = {}
                radiant_win = match_details['result']['radiant_win']
                for player in match_details['result']['players']:
                    if player['account_id'] == user_id + 76561197960265728:
                        hero_id = player['hero_id']

                        # initialize if necessary
                        if hero_id not in player_profile:
                            player_profile[hero_id] = {}
                            player_profile[hero_id]['win_perc'] = 0
                            player_profile[hero_id]['matches'] = 0
                            player_profile[hero_id]['kills'] = 0
                            player_profile[hero_id]['deaths'] = 0
                            player_profile[hero_id]['assists'] = 0

                        # save details
                        if (radiant_win == True and player['player_slot'] < 5) or \
                           (radiant_win == False and player['player_slot'] > 5):
                            player_profile[hero_id]['win_perc'] += 1
                        player_profile[hero_id]['matches'] += 1
                        player_profile[hero_id]['kills'] += player['kills']
                        player_profile[hero_id]['deaths'] += player['deaths']
                        player_profile[hero_id]['assists'] += player['assists']

            print >> sys.stderr, match_history['result']['results_remaining']
            if(match_history['result']['results_remaining'] == 0):
                break

        # average all hero stats
        for hero in player_profile:
            hero['win_perc'] /= hero['matches']
            hero['kills'] /= hero['matches']
            hero['deaths'] /= hero['matches']
            hero['assists'] /= hero['matches']

        return player_profile

if __name__ == '__main__':
    # 183104694 = user CADILLACLACLACLACO (Alan)
    crawler = UserCrawler()
    print crawler.getPlayerProfile(183104694)
