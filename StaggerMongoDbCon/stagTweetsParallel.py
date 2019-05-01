#Code adapted original created by filippiazikou
#Found at https://github.com/filippiazikou/Tweetopolitics/blob/master/TextAnalysis/stagTweetsParallel.py

###
#
# KTH - Royal Institute of Technology
# Read Tweets from Mongo Database and extract statistics about users and tags
# Filippia Zikou
#
###

# Retreive congiguration info
import ConfigParser

# Communication with mongo
from pymongo import MongoClient

# Retrieve content from ur
from bs4 import BeautifulSoup, Comment, NavigableString
import urllib2

# Threads
import threading

# Communication with Java server
import javaSocketCommunication

# Reading the config file
config = ConfigParser.RawConfigParser()
config.read('read.cfg')

# Reading database settings
client = MongoClient()
db = client[config.get('mongodb', 'db')]
collection = config.get('mongodb', 'collection')

# Specify the maximum length to send through socket
MAX_LEN = 16384
MIN_LEN = 24

# Specify the num of cursors to be processed in parallel_scan
CURSORS_NUM = 4


# Remove part of html content that are not visible
def visible(element):
    try:
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif isinstance(element, Comment):
            return False
        return True
    except:
        print "error"


def stag_tweet(doc, client_socket):
    # Get attributes needed from tweet
    tweetid = doc['_id']
    text = doc['text'].encode('utf8')
    urls = doc['entities']['urls']

    # Send text to java server and get back stagged text and entities
    javaSocketCommunication.mysend(client_socket, text + "\n")
    reply = javaSocketCommunication.myreceive(client_socket)
    flag = True
    for entity in reply.split("~"):
        split = entity.rstrip('\n')
        # Insert the tagged text
        if flag == True:
            db[collection].update({"_id": tweetid}, {'$push': {'stagged_text': split}})
            flag = False
        # Insert the entities
        else:
            db[collection].update({"_id": tweetid},
                                  {"$push": {"enitites": {"name": split.split(",")[0], "type": split.split(",")[1]}}})


def process_cursor(cursor):
    # Create connection
    client_socket = javaSocketCommunication.init_client_communication()
    threadid = str(threading.current_thread())
    javaSocketCommunication.mysend(client_socket, "1\n")
    javaSocketCommunication.myreceive(client_socket)

    # Analyze the chunk
    for document in cursor:
        if ('stagged_text' not in document):
            stag_tweet(document, client_socket)

    print "Sending end of file"
    javaSocketCommunication.mysend(client_socket, "EOF\n")
    #javaSocketCommunication.myreceive(client_socket)
    # Terminate Connection
    #javaSocketCommunication.terminate_client_communication(client_socket)


def read_tweets():
    # Get up to 4 cursors.
    cursors = db[collection].parallel_scan(CURSORS_NUM)
    print len(cursors)
    threads = [
        threading.Thread(target=process_cursor, args=(cursor,)) for cursor in cursors
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    read_tweets()
