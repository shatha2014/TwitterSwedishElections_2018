# Communication with mongo
import collections

from pymongo import MongoClient

# Retreive congiguration info
import configparser


import matplotlib.pyplot as plt
import re
from collections import Counter

config = configparser.RawConfigParser()
config.read('exploration.cfg')

# Reading database settings
client = MongoClient()
db = client[config.get('mongodb', 'db')]
collection = config.get('mongodb', 'collection')

tweetsDay = collections.OrderedDict()
lastMonthTweets = collections.OrderedDict()


#Get the Tweets up to the election and plot
def tweet_stats():
    i = 0
    getTweetLastMonth = True
    for doc in db[collection].find():
        dataeCreated = doc.get("created_at")[:-9]
        if(dataeCreated == "2018-10-01" ):
            print(i)
            break
        if tweetsDay.get(dataeCreated) is None:
            tweetsDay[dataeCreated] = 1
        else:
            newsum = tweetsDay.get(dataeCreated) + 1
            tweetsDay[dataeCreated] = newsum
        if doc.get("created_at")[:-9] == "2018-08-01" and getTweetLastMonth:
            print(i)
            print(doc.get("stagged_text"))
            getTweetLastMonth = False
        i = i + 1

    plt.switch_backend('Agg')
    names = list(tweetsDay.keys())
    values = list(tweetsDay.values())
    print(len(names))
    print(names[len(names)-1])
    #remove names to see the graph
    plt.plot(names, values)
    ax = plt.gca()
    #xticks = ax.axes.xaxis.get_major_ticks()
    i = 0
    #plt.setp(ax.get_xticklabels(), visible=False)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Tweets', fontsize=16)
    i = 0

    ax.set_xticks(["2018-02-04", "2018-04-09", "2018-05-24", "2018-07-08", "2018-09-09"])
    ax.set_xticklabels(["2018-02-04", "2018-04-09", "2018-05-24", "2018-07-08", "2018-09-09"])

    plt.savefig('bar.png')

#Get the tweets the last month up to the elections
def tweets_last_month():
    data = []
    i = 123
    counter = 0
    countLastMonth = 0
    with open("test.txt", encoding="utf-8") as fp:
        line = fp.readline()
        while line:
            i = i + 1
            if i<counter:
                data.append(line)
                countLastMonth =+ 1
            line = fp.readline()

    print(countLastMonth)
    with open("lastmonth.txt", encoding="utf-8") as fp:
        for d in data:
            fp.write(d+'\n')

def most_common_word():
    words = re.findall(r'\w+', open('NoStopTweets.txt',encoding="utf-8").read().lower())
    print(Counter(words).most_common(15))

if __name__ == '__main__':
    #tweet_stats()
    #tweets_last_month()
    most_common_word()
