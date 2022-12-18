import scrapy
from bs4 import BeautifulSoup
import json
import re

class ExampleSpider(scrapy.Spider):
    name = 'tutorial'

    search_term = ''
  
    player_id=''

    player_dict = {}

    headers_search = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-encoding': 'gzip, deflate, br',
      'accept-language': 'es-ES,es;q=0.9',
      'cache-control': 'no-cache',
      'pragma': 'no-cache',
      'referer': 'https://www.transfermarkt.com/',
      'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
  
    headers_player = {
      'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-encoding': 'gzip, deflate, br',
      'accept-language': 'es-ES,es;q=0.9',
      'cache-control': 'no-cache',
      'referer': 'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=',
      'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    headers_performance = {
      "accept" : "*/*",
      "accept-encoding" : "gzip, deflate, br",
      "accept-language" : "es-ES,es;q=0.9",
      "cache-control" : "no-cache",
      "pragma" : "no-cache",
      #"referer" : player_url,
      "sec-ch-ua" : 'Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      "sec-ch-ua-mobile" :  "?0",
      "sec-ch-ua-platform" : "Windows",
      "sec-fetch-dest" : "empty",
      "sec-fetch-mode" : "cors",
      "sec-fetch-site" : "same-origin",
      "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }

    def __init__(self, search_ter, player_dic, *a, **kw):
      super(ExampleSpider, self).__init__(*a, **kw)
      self.search_term = search_ter
      
      self.player_dict = player_dic
      
  
    if __name__ == '__main__':
      pass
    
      

    def clean_datum(self, datum):
      datum = re.sub("\n", "", datum)
      datum = re.sub("^[\s]+", "", datum)
      datum = re.sub("[\s]+$", "", datum)
      datum = re.sub("[\s]{2,}", " ", datum)
      return datum

    #@wait_for(timeout=5.0)
    def start_requests(self):
      
      self.urls = [f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={self.search_term}']
      for urlll in self.urls:
        yield scrapy.Request(urlll, headers = self.headers_search)
  
    def parse(self, response):
      #self.headers_player['referer'] = self.urls[0]
      soup = BeautifulSoup(response.text, 'lxml')
      
      data_cell = soup.find('td', class_ = 'hauptlink')
      url_player = data_cell.find('a').get('href')
      
      url_parts = url_player.split("/")
      
      if url_parts[2] == "profil":
        self.player_id = url_parts[4]
        player_url = f'https://www.transfermarkt.com{url_player}'
        self.headers_player['referer'] = response.url
        
        yield scrapy.Request(player_url, callback=self.parse_personal, headers=self.headers_player)
      else:
        self.player_dict['player_name'] = 'Name Error'
      

    def parse_personal(self, response):
      soup = BeautifulSoup(response.text, 'lxml')
      personal_info = soup.find_all("meta", attrs={"name": "keywords"})
      
      contento = personal_info[0]
      content = contento['content']
      
      contents = content.split(',')
      personal_info = soup.find_all('span', class_='info-table__content info-table__content--bold')
      personal_infoo = soup.find_all("meta", attrs={"name": "description"})
      contentoo = personal_infoo[0]
      contentt = contentoo['content']
      contentt = re.sub("➤", ",", contentt)
      contentss = contentt.split(',')
      self.player_dict['player_name'] = self.clean_datum(contents[0])
      self.player_dict['player_age'] = self.clean_datum(contentss[1])
      self.player_dict['player_nation'] = self.clean_datum(contents[3])
      self.player_dict['player_position'] = self.clean_datum(contentss[5])
      self.player_dict['player_club'] = self.clean_datum(contentss[3])
      contentss[6] = re.sub("Market value:", "", contentss[6])
      self.player_dict['player_marketvalue'] = self.clean_datum(contentss[6])
      
      stats_url = f'https://www.transfermarkt.com/ceapi/player/{self.player_id}/performance'
      self.headers_performance['referer'] = response.url
      yield scrapy.Request(stats_url, callback = self.parse_stats, headers=self.headers_performance)

      
    def parse_stats(self, response):
      data = json.loads(response.body)
      
      for stats in data:
        
        
        description_competition = self.clean_datum(stats["competitionDescription"])
        
        if description_competition == "Serie A" or description_competition == "LaLiga" or description_competition == "Premier League" or description_competition == "Bundesliga" or description_competition == "Liga Portugal" or description_competition == "Ligue 1" or description_competition == "Eredivisie" or description_competition == "Bundesliga" or description_competition == "Premiership":
          self.player_dict['player_league_matches'] = self.player_dict['player_league_matches'] + int(stats["gamesPlayed"])
          self.player_dict['player_league_goals'] = self.player_dict['player_league_goals'] + int(stats["goalsScored"])
          self.player_dict['player_league_assists'] = self.player_dict['player_league_assists'] + int(stats["assists"])

        elif description_competition == "Champions League":
          self.player_dict['player_champions_matches'] =  int(stats["gamesPlayed"])
          self.player_dict['player_champions_goals'] = int(stats["goalsScored"])
          self.player_dict['player_champions_assists'] = int(stats["assists"])

        else:
          self.player_dict['player_other_matches'] = self.player_dict['player_other_matches'] + int(stats["gamesPlayed"])
          self.player_dict['player_other_goals'] = self.player_dict['player_other_goals'] + int(stats["goalsScored"])
          self.player_dict['player_other_assists'] = self.player_dict['player_other_assists'] + int(stats["assists"])
          
      
