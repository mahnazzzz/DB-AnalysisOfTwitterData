import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.social_net

def get_all():
    for tweet in db.tweets.find():
        print(tweet)

def get_user_amount():
    return (len(db.tweets.distinct('user')))

print('How many Twitter users are in the database?')
print(get_user_amount() , 'Users are in there')

