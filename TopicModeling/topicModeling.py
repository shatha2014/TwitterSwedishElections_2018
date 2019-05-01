# Retreive congiguration info
import ConfigParser

# Communication with mongo
from pymongo import MongoClient

# Reading the config file
config = ConfigParser.RawConfigParser()
config.read('confTopic.cfg')

# Reading database settings
client = MongoClient()
db = client[config.get('mongodb', 'db')]
collection = config.get('mongodb', 'collection')
statistics_collection = config.get('mongodb', 'stats_collection')
user_collection = config.get('mongodb', 'user_collection')

# Reading parties
partyNames = config.get('parties', 'names').split(',')

MAX_LEN = 150000


# Get tweets from party users and save in a party specific collection
def gather_party_tweets():
    for party in partyNames:
        list = db[user_collection].distinct("userList", {"_id": party})
        pipeline = [
            {"$match": {"user.screen_name": {"$in": list}}},
            {"$group": {
                "_id": party, "textList": {"$push": '$stagged_text'}}},
            {"$out": party + "_tweets_2"}
        ]
        db[collection].aggregate(pipeline=pipeline)


if __name__ == '__main__':
    gather_party_tweets()
