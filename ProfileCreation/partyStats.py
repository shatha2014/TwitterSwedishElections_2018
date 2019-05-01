import ConfigParser

# Communication with mongo
from pymongo import MongoClient
from bson.code import Code

# Reading the config file
config = ConfigParser.RawConfigParser()
config.read('read.cfg')

# Reading database settings
client = MongoClient()
db = client[config.get('mongodb', 'db')]
collection = config.get('mongodb', 'collection')
statistics_collection = config.get('mongodb', 'stats_collection')

# Reading parties
partyNames = config.get('parties', 'names').split(',')

#Get stats for the db number of users and and total party users.
def get_stats():
    print("Total users: " + str(db[statistics_collection].find().count()))
    print("Not in party users: " + str(db[statistics_collection].find({"party": "none"}).count()))
    for party in partyNames:
        print(party + " has total: " + str(db[statistics_collection].find({"party": party}).count()))

#get number of mentions for each party
def gather_party_mentions():
    pipeline = [
        {"$group": {
            "_id": "$party",
            "sum": {"$sum": "$value.mentions"}
        }}
    ]
    for doc in db[statistics_collection].aggregate(pipeline=pipeline):
       print(str(doc.get("_id")) +" number of mentions: "+ str(doc.get("sum")))

#get number of posts for each party
def gather_party_posts():
    pipeline = [
        {"$group": {
            "_id": "$party",
            "sum": {"$sum": "$value.posts"}
        }}
    ]
    for doc in db[statistics_collection].aggregate(pipeline=pipeline):
       print(str(doc.get("_id")) +" number of posts: "+ str(doc.get("sum")))



if __name__ == '__main__':
    get_stats()
    gather_party_posts()
    gather_party_mentions()
