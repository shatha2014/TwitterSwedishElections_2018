# coding=utf-8
# Retreive congiguration info
import ConfigParser

# Communication with mongo
from pymongo import MongoClient

# Reading the config file
config = ConfigParser.RawConfigParser()
config.read('popularityEstimateConf.cfg')

# Reading database settings
client = MongoClient()
db = client[config.get('mongodb', 'db')]
collection = config.get('mongodb', 'collection')
statistics_collection = config.get('mongodb', 'stats_collection')
electionresult_collection = config.get('mongodb', 'election_collection')

# Reading parties
partyNames = config.get('parties', 'names').split(',')

MAX_LEN = 150000

#get total election realted tweets.
def gather_total_election_tweets():
    amount = db[collection].find({
        '$and': [
            {"entities.hashtags.text": {'$in': ["svpol", "val2018","val18","dinröst","tv4val","Val2018"]}},
            {"entities.user_mentions.screen_name": {
                '$in': partyNames}}
        ]
    }).count()
    db[electionresult_collection].update({'party': 'total'}, {'party': 'total', 'amount': amount}, upsert=True)

#get amount of tweets for all parties
def party_results():
    for party in partyNames:
        amount = db.sverige.find({
            '$and': [
                {"entities.hashtags.text": {'$in': ["svpol", "val2018","val18","dinröst","tv4val","Val2018"]}},
                {"entities.user_mentions.screen_name": {'$in': [party]}}
            ]
        }).count()
        db[electionresult_collection].update({'party': party}, {'party': party, 'amount': amount}, upsert=True)


if __name__ == '__main__':
    gather_total_election_tweets()
    party_results()
