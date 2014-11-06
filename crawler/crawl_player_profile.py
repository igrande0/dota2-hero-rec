""" Crawl a user's matches and compile data
"""

import json
import requests

class UserCrawler(object):
    def __init__(self, user_id):
        self.history_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/'
        self.details_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'
        self.history_params = dict(key='CCAFC265C13500E30C9E8BC6E04EEE9C', account_id=user_id)
        self.details_params = dict(key='CCAFC265C13500E30C9E8BC6E04EEE9C')

    def updateUser(self, user_id):
        self.history_params['account_id'] = user_id

    def getMatches(self):
        resp = requests.get(url=self.history_url, params=self.history_params)
        return json.loads(resp.text)

    def getMatchDetails(self):
        pass

if __name__ == '__main__':
    # 39127319 = user iggyzizzle (Isaac)
    crawler = UserCrawler('39127319')
    print crawler.getMatches()
