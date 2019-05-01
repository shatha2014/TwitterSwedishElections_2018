import ConfigParser

# Communication with mongo
from pymongo import MongoClient
import codecs

config = ConfigParser.RawConfigParser()
config.read('doc2vec.cfg')

# Reading database settings
client = MongoClient()
db = client[config.get('mongodb', 'db')]
users_tweets = config.get('mongodb', 'user_collection')


#Concat the collced tweets from the same user
def collect_tweets():
    fp = codecs.open('concatTweets.txt','w', encoding='utf-8')
    for doc in db[users_tweets].find():
        s=""
        listTweets = doc.get('tweets')
        for tweet in listTweets:
            s = s +' '+tweet[0]
        fp.write(s+'\n')
    fp.close()
if __name__ == '__main__':
    collect_tweets()