import pymongo
from bson.son import SON
from bson.regex import Regex
import re

from pymongo import MongoClient

client = MongoClient()
db = client.social_net

def get_all():
    for tweet in db.tweets.find():
        print(tweet)

def get_total_user_amount():
    return (len(db.tweets.distinct('_TheSpecialOne_'))) #gets the length of the distinct users

def get_user_most_linked():
    pipeline = [
        {'$match':{'text':{'$regex':"@\w+"}}}, 
        {'$addFields': {"mentions":1}},
        {'$group':{"_id":"$user", "mentions":{'$sum':1}}},
        {'$sort':{"mentions":-1}},
        {'$limit':10}]
    tweets = db.tweets.aggregate(pipeline)
    return(list(tweets))



def print_list(list):
    for el in list:
        print(el)



print('How many Twitter users are in the database?')
print(get_total_user_amount() , 'Twitter users')


print('Which Twitter users link the most to other Twitter users? (Provide the top ten.)')
print_list(get_user_most_linked())

