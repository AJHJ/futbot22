from keep_alive import keep_alive
from tutorial.tutorial.spiders.example import ExampleSpider
import os
import praw
import re
import time
import scrapydo
scrapydo.setup()

reddit = praw.Reddit(client_id=os.getenv('client_id'),
                     client_secret=os.getenv('client_secret'),
                     username=os.getenv('username'),
                     password=os.getenv('password'),
                     user_agent="<ReplyCommentBot1.0>")


class RedditBot:

  player1 = ''
  player2 = ''
  
  player1_stats = {
      'player_name':'',
      'player_age':'',
      'player_nation':'',
      'player_position':'',
      'player_marketvalue':'',
      'player_club':'',
      'player_league_matches':0,
      'player_league_goals':0,
      'player_league_assists':0,
      'player_champions_matches':0,
      'player_champions_goals':0,
      'player_champions_assists':0,
      'player_other_matches':0,
      'player_other_goals':0,
      'player_other_assists':0
    }
  player2_stats = {
      'player_name':'',
      'player_age':'',
      'player_nation':'',
      'player_position':'',
      'player_marketvalue':'',
      'player_club':'',
      'player_league_matches':0,
      'player_league_goals':0,
      'player_league_assists':0,
      'player_champions_matches':0,
      'player_champions_goals':0,
      'player_champions_assists':0,
      'player_other_matches':0,
      'player_other_goals':0,
      'player_other_assists':0
    }

  def empty_dictionaries(self, dictionary):
    dictionary = {
      'player_name':'',
      'player_age':'',
      'player_nation':'',
      'player_position':'',
      'player_marketvalue':'',
      'player_club':'',
      'player_league_matches':0,
      'player_league_goals':0,
      'player_league_assists':0,
      'player_champions_matches':0,
      'player_champions_goals':0,
      'player_champions_assists':0,
      'player_other_matches':0,
      'player_other_goals':0,
      'player_other_assists':0
    }
    return dictionary


  def clean_string(self, raw_string):
    cleaned_string = raw_string.lower()
    cleaned_string = re.sub(r'[^A-Za-z -]+', '', cleaned_string)
    return cleaned_string
  
  def run_spider_one(self):
    scrapydo.run_spider(ExampleSpider, search_ter=self.player1, player_dic=self.player1_stats)
    
  def run_spider_two(self):
    scrapydo.run_spider(ExampleSpider, search_ter=self.player2, player_dic=self.player2_stats)
  
  def find_match(self, comment):
    comment_str = self.clean_string(comment.body)
    words = comment_str.split()
    comment_str = ''
    self.player1 = ''
    self.player2 = ''
    if words[0] == "-stats":
      for i, word in enumerate(words):
        #We are checking if this comment is a comparison (-v)
        if word == "-v":
          #Here we get the complete player1 name
          for x in range(1, i):
            if self.player1 != '':
              self.player1 = self.player1 + '+' + words[x]
            else:
              self.player1 = words[x]
          #Here we get the complete player2 name
          for x in range(i+1, len(words)):
            if self.player2 != '':
              self.player2 = self.player2 + '+' + words[x]
            else:
              self.player2 = words[x]

          #If there is 2 names available then search the names and post
      if self.player1 != '' and self.player2 != '':
        
        #This code allows to run 2 scrapers 1 by 1
        self.run_spider_one()
        self.run_spider_two()
        comment_str = f'Stats from current season taken from transfermarkt.com \n\nPlayer name: {self.player1_stats["player_name"]} | {self.player2_stats["player_name"]} \n\nAge: {self.player1_stats["player_age"]} | {self.player2_stats["player_age"]} \n\nCountry: {self.player1_stats["player_nation"]} | {self.player2_stats["player_nation"]} \n\nPosition: {self.player1_stats["player_position"]} | {self.player2_stats["player_position"]} \n\nMarket Value: {self.player1_stats["player_marketvalue"]} | {self.player2_stats["player_marketvalue"]} \n\nClub: {self.player1_stats["player_club"]} | {self.player2_stats["player_club"]} \n\nLeague matches: {self.player1_stats["player_league_matches"]} | {self.player2_stats["player_league_matches"]} \n\nLeague goals: {self.player1_stats["player_league_goals"]} | {self.player2_stats["player_league_goals"]} \n\nLeague assists: {self.player1_stats["player_league_assists"]} | {self.player2_stats["player_league_assists"]} \n\nChampions L. matches: {self.player1_stats["player_champions_matches"]} | {self.player2_stats["player_champions_matches"]} \n\nChampions L. goals: {self.player1_stats["player_champions_goals"]} | {self.player2_stats["player_champions_goals"]} \n\nChampions L. assists: {self.player1_stats["player_champions_assists"]} | {self.player2_stats["player_champions_assists"]} \n\nOther matches: {self.player1_stats["player_other_matches"]} | {self.player2_stats["player_other_matches"]} \n\nOther goals: {self.player1_stats["player_other_goals"]} | {self.player2_stats["player_other_goals"]} \n\nOther assists: {self.player1_stats["player_other_assists"]} | {self.player2_stats["player_other_assists"]}'
        self.player1_stats = self.empty_dictionaries(self.player1_stats)
        self.player2_stats = self.empty_dictionaries(self.player2_stats)
        

      #If no comment was generated yet then probably the comment is one player stats
      if comment_str == '':
        self.player1 = ''
        for word in words:
          if word != '-stats':
            if self.player1 != '':
              self.player1 = f'{self.player1}+{word}'
            else:
              self.player1 = word
        #If player1 name was found then search and comment
        if self.player1 != '':
          self.run_spider_one()
          comment_str = f'Stats from current season taken from transfermarkt.com \n\nPlayer name: {self.player1_stats["player_name"]} \n\nAge: {self.player1_stats["player_age"]} \n\nCountry: {self.player1_stats["player_nation"]} \n\nPosition: {self.player1_stats["player_position"]} \n\nMarket Value: {self.player1_stats["player_marketvalue"]} \n\nClub: {self.player1_stats["player_club"]} \n\nLeague matches: {self.player1_stats["player_league_matches"]} \n\nLeague goals: {self.player1_stats["player_league_goals"]} \n\nLeague assists: {self.player1_stats["player_league_assists"]} \n\nChampions L. matches: {self.player1_stats["player_champions_matches"]} \n\nChampions L. goals: {self.player1_stats["player_champions_goals"]} \n\nChampions L. assists: {self.player1_stats["player_champions_assists"]} \n\nOther matches: {self.player1_stats["player_other_matches"]} \n\nOther goals: {self.player1_stats["player_other_goals"]} \n\nOther assists: {self.player1_stats["player_other_assists"]}'
    self.make_reply(comment, comment_str)

  def make_reply(self, comment, comment_str):
    try:
      comment.reply(comment_str)
      time.sleep(15)
    except Exception as e:
      print(e)


if __name__ == '__main__':
  keep_alive()
  subreddit = reddit.subreddit("test")
  bot = RedditBot()
  for comment in subreddit.stream.comments(skip_existing=True):
    bot.find_match(comment)
