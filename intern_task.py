from http import client
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from tweepy import OAuthHandler
import pandas as pd
import time
import tweepy
import json
from oauth2client.service_account import ServiceAccountCredentials

credential_url = "https://gist.githubusercontent.com/vrushangdev/e26987231a1e8517b6b7f3487f74d6d0/raw/9339c09c2298a3b91fc743c67ee880ce79e1c5e7/gsheet_creds.json"
response = requests.get(credential_url)
try:
  cred_file = open('file.json','w')
  cred_file.write(response.text)
  cred_file.close()
except Exception as e:
  print(e)
finally:
  cred_file.close()
gc = gspread.service_account(filename='/Users/poonamdhankher/Downloads/test/amazon_web_scrapping/twitter scrapping/file.json')
gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1slvCX233_Qwqw1JPENxSL7qZzMLFwUmPbvFC6p7YJ_Q")
work_sheet = gsheet.worksheets()[0]
twitter_links = work_sheet.col_values(5)
tweet_data=[]



def scrape_tweet_data(link):
  consumer_key = "XcrRUHT0KE7m6U2IGTQ0JQSbt"
  consumer_secret = "BcIfwBG9k72r8fJJgjLgE6iqQ4vSxoGOH2snEM1xLuU8xVKYOX"
  access_token = "2726708538-nKLmdxmPDSEPhUQr3JYq6lFPCa5dEuyHUy2g875"
  access_token_secret = "0nJvpnHrYxUl0e4SrGD1eF0pd53xD5VBK126ysrYumzEG"
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)
  dict={}
  
  # link= "https://twitter.com/psalmcrypt/status/1442536560667332608?s=19"
  links= link.split("/")
  if (len(links) < 5):
    return
  id = links[5]
  id_link= id.split("?")
  promoter_id= id_link[0]
  # print(promoter_id)
  try:
    promoter_tweet_status = api.get_status(promoter_id)
  except:
    print("Issue found with promoter tweet")
    return
  promoter_id_number= promoter_tweet_status.id_str
  # print(promoter_tweet_status.id_str)
  promoter_name= promoter_tweet_status.user.screen_name
  # print(promoter_tweet_status.user.screen_name)
  promoter= "https://twitter.com/"+ promoter_name
  print("Promoter:" + promoter)
  promoter_tweet= promoter+ "/status/"+ str(promoter_id_number)
  print("Promoter Tweet:" + promoter_tweet)
  promoter_likes= promoter_tweet_status.favorite_count
  print("Promoter Tweet Likes: " + str(promoter_tweet_status.favorite_count))
  promoter_detail= promoter_tweet_status.text
  print("Promoter Tweet content: " + promoter_tweet_status.text)
  
  
  

# Influencer details
  influencer_tweet_id = promoter_tweet_status.in_reply_to_status_id
  print(influencer_tweet_id)
  try:
    influencer_tweet_status = api.get_status(influencer_tweet_id)
  except:
    print("Issue found with influencer tweet")
    return

  influencer_name= influencer_tweet_status.user.screen_name
# print(influencer_tweet_status.user.screen_name)
  influencer = "https://twitter.com/"+ influencer_name
  print("Influencer:" + influencer)
  influencer_tweet= influencer+ "/status/"+ str(influencer_tweet_id)
  print("Influencer:" + influencer_tweet)
  influencer_likes= influencer_tweet_status.favorite_count
  print("Influencer Tweet Likes: " + str(influencer_tweet_status.favorite_count))
  influencer_detail= influencer_tweet_status.text
  print("Influencer Tweet content: " + influencer_tweet_status.text)
  
  dict["Promoter"]= promoter
  dict["Promoter Tweet"]= promoter_tweet
  dict["Promoter Likes"]= promoter_likes
  dict["Promoter Detail"]= promoter_detail
  dict["Influencer"]= influencer
  dict["Influencer Tweet"]= influencer_tweet
  dict["Influencer Likes"]= influencer_likes
  dict["Influencer Detail"]= influencer_detail
  tweet_data.append(dict)





# scrape_tweet_data("https://twitter.com/psalmcrypt/status/1442536560667332608?s=19")
# ------------

for tweets in twitter_links:
  scrape_tweet_data(tweets)

  jsonstr= json.dumps(tweet_data)
  with open('/Users/poonamdhankher/Downloads/test/amazon_web_scrapping/twitter scrapping/data.json', 'w') as f:
      print(jsonstr, file=f)





