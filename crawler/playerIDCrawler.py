""" Gather all players that a user has ever played with
"""

from __future__ import division

import sys
import json
import requests
from time import sleep

STEAM_KEY = 'CCAFC265C13500E30C9E8BC6E04EEE9C'

class PlayerCrawler():
    def __init__(self):
        self.history_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/'
        self.history_params = dict(key=STEAM_KEY, min_players=10)

    # returns a set of all unique players that player "user_id" has ever played with
    def getUsers(self, user_id):
        # to store the player's stats for each match
        players = set()
        # add the offset to conver to 64 bit ID
        self.history_params['account_id'] = user_id + 76561197960265728
        self.history_params.pop('start_at_match_id', None)
        #print >> sys.stderr, self.history_params['account_id']
        current_match = 1
        last_match_id = 0

        while(True):
            # get the next 100 matches
            resp = requests.get(url=self.history_url, params=self.history_params)
            match_history = json.loads(resp.text)
            #print >> sys.stderr, match_history

            # user's profile is private
            if match_history['result']['status'] == 15:
                #print >> sys.stderr, "private user profile: " + str(user_id)
                return players

            for match in match_history['result']['matches']:
                if 'start_at_match_id' in self.history_params and \
                   self.history_params['start_at_match_id'] == match['match_id']:
                    continue

                # for getting the next page of matches
                current_match +=1
                self.history_params['start_at_match_id'] = match['match_id']

                for player in match['players']:
                    # this is the value meaning that the profile is private (and therefore is not real)
                    if player['account_id'] != 4294967295 and player['account_id'] != user_id:
                        players.add(player['account_id'])

            print >> sys.stderr, match_history['result']['results_remaining']
            if(match_history['result']['results_remaining'] == 0):
                break

        return players

if __name__ == '__main__':
    # hopefully the spread of MMR here will provide a more complete picture
    player_crawler = PlayerCrawler()
    # alan's main, mmr ~4.5k
    players = player_crawler.getUsers(149987685)
    # iggyzizzle, mmr ~3.7k
    players = players | player_crawler.getUsers(39127319)
    # travis (starix jr.), mmr ~5k
    players = players | player_crawler.getUsers(105496685)
    # TK, mmr ~3k
    players = players | player_crawler.getUsers(60010854)
    # dragonofthewest, mmr ~3k
    players = players | player_crawler.getUsers(50630885)
    # raegano, mmr ~3k?
    players = players | player_crawler.getUsers(75293220)
    # dan, mmr ~3.3k
    players = players | player_crawler.getUsers(54406907)
    # era, mmr ~5.5k+
    players = players | player_crawler.getUsers(70422290)
    # solin, mmr ~5k
    players = players | player_crawler.getUsers(14988790)
    # ben, mmr ~4.6kk
    players = players | player_crawler.getUsers(38164725)
    # acidicpain, 4k mmr?
    players = players | player_crawler.getUsers(89090493)
    # james, 4k mmr
    players = players | player_crawler.getUsers(155331471)
    # austin, 4k mmr
    players = players | player_crawler.getUsers(19745006)
    # [a]kke, 6k+ mmr
    players = players | player_crawler.getUsers(41288955)
    # qojqva, 6.5k+ mmr?
    players = players | player_crawler.getUsers(86738694)

    for player in players:
        print player
