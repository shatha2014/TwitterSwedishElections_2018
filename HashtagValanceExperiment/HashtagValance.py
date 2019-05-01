# Retreive congiguration info
import ConfigParser

# Communication with mongo
from pymongo import MongoClient

# Reading the config file
config = ConfigParser.RawConfigParser()
config.read('valance.cfg')

# Reading database settings
client = MongoClient()
db = client[config.get('mongodb', 'db')]
indiv_hashtag_party_count = config.get('mongodb', 'indiv_hashtag_party_count')

all_hashtag_party_count = config.get('mongodb', 'all_hashtag_party_count')

total_indiv_hashtags_count = config.get('mongodb', 'total_indiv_hashtags_count')

all_hashtag_count = config.get('mongodb', 'all_hashtag_count')

# Reading parties
partynames = config.get('parties', 'names').split(',')

# Specify the maximum length to send through socket
MAX_LEN = 150000

# Collect number of hashtags that each party used.

dictionary = dict()
hashtagDict = dict()


# For each hashtag have a number for how times it was used
def get_valance():
    for party in partynames:
        for item in db[party + "_valance_collection"].find():
            t = 0.0
            for np in partynames:
                h = db[np + "_valance_collection"].find_one({"_id": item.get("_id")})
                if h is not None:
                    t = + h.get("valance")
            if t!=0:
                value = item.get("valance") / float(t)
                db[party + "_valance_collection"].update({'_id': item.get("hashtag")}, {'$set': {'valance': value}})

# Collect number of hashtags that were used for all parties.
# For each hashtag give a number for how many times it was used for each party.
def party_hashtags_collection():
    # save all total hashtag count for each party in dictonary
    for doc in db[all_hashtag_party_count].find():
        party = doc.get("_id")
        dictionary[party.get("id")] = doc.get("total_tags")
    print dictionary
    for doc in db[total_indiv_hashtags_count].find():
        hashtagDict[doc.get("_id")] = doc.get("count")
    print "Dictionary created"
    print dictionary.get("moderaterna")
    print hashtagDict.get("svpol")

    total = 0
    # Get the total amount of hashtags used by all parties.
    for tag in db[all_hashtag_count].find():
        total = tag.get("total")

    for party in db[indiv_hashtag_party_count].find({}):
        for item in party.get("term_tf"):
            h = item.get("hsum") / float(dictionary.get(party.get("_id")))
            db[party.get("_id") + "_valance_collection"].insert({'_id': item.get("hashtag"), "valance": h})

    print "First collection done now get tail and real valance value"


if __name__ == '__main__':
    party_hashtags_collection()
    get_valance()
