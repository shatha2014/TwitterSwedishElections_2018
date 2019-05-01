# Communication with mongo
from pymongo import MongoClient

# Retreive congiguration info
import ConfigParser

# Reading the config file
config = ConfigParser.RawConfigParser()
config.read('read.cfg')

# Reading database settings
client = MongoClient()
db = client[config.get('mongodb', 'db')]
collection = config.get('mongodb', 'collection')
statistics_collection = config.get('mongodb', 'stats_collection')
id_collection = config.get('mongodb', 'id_collection')

edgelist = []
dictionary = dict()
edgedict = dict()
nodeDict = dict()
users = dict()
#Makes it so that only nodes with 5 posts or higher gets added to edgelist
for doc in db[statistics_collection].find({'value.posts': {'$gt': 5}}):
    users[doc.get('_id')] = 1

#Add new edge to the list
def append_graph(username, connections):
    gen = []
    for c in connections:
        if(users.get(c) is not None) and (edgedict.get(username+c) is None) and (edgedict.get(c+username) is None):
            edgedict[username+c] = (dictionary.get(c), dictionary.get(username))
            nodeDict[c] = 1
            nodeDict[username] = 1

    if len(edgedict.keys()) % 5000 == 0:
        if 0 != len(edgelist):
            print(edgedict.get(username+connections[0]))
        print(len(edgedict.keys()))

#Create id numbers for each user.
def create_idNum():
    i = 0
    for doc in db[statistics_collection].find():
        db[statistics_collection].update({'_id': doc.get("_id")}, {'$set': {'idNum': i}})
        dictionary[doc.get("_id")] = i
        i = i+1
    print "added idnumer"

#Create the list of edges with users having 5 or more posts
def creat_list():
    x = 0
    for doc in db[statistics_collection].find({'value.posts': {'$gt': 5}}):
        x = x + 1
        append_graph(doc.get("_id"), list(set(doc.get("value").get("friends"))))
    print "list is ready"
    # write edges to file
    with open('edgelist.txt', 'w') as f:
        for k in edgedict.values():
            line = ' '.join(str(x) for x in k)
            f.write(line + '\n')
    print "Number of nodes "+ str(len(nodeDict.keys()))


    #Create collection with documents in edgelist
    for document in db[statistics_collection].find():
        if nodeDict.get(document.get("_id")) is not None:
            db[id_collection].insert(document)
    i = 0
    #Set new id numbers and save in dictionarty.
    dictionaryNewID = dict()
    for doc1 in db[id_collection].find():
        dictionaryNewID[doc1.get("idNum")] = i
        db[id_collection].update({'_id': doc1.get("_id")}, {'$set': {'idNum': i}})
        i = i+1
    #update the edgelist with new id numbers

    "Number of nodes " + str(len(dictionaryNewID.keys()))
    with open('edgelist.txt','r') as f:
        with open('NewEdgelist.txt', 'w') as fp:
            line = f.readline().strip('\n')
            while line:
                val = line.split(' ')
                s = str(dictionaryNewID.get(int(val[0])))+' '+str(dictionaryNewID.get(int(val[1])))+'\n'
                fp.write(s)
                line = f.readline().strip('\n')

    print "Number of edges " + str(len(edgedict.keys()))
if __name__ == '__main__':
    print len(users)
    create_idNum()
    creat_list()
