#Adapeted code original script created by filippiazikou
#Found here: https://github.com/filippiazikou/Tweetopolitics/blob/master/iGraph/graphParties.py
# Get the graph libraries
from igraph import *

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

# Reading parties
partyNames = config.get('parties', 'names').split(',')

# Reading party users
partyUsers = {}
allPartyUsers = []
for party in partyNames:
    partyUsers[party] = []
    for doc in db[statistics_collection].find({'party': party}, {'_id': 1}):
        partyUsers[party].append(doc['_id'].encode('utf-8'))
        allPartyUsers.append(doc['_id'].encode('utf-8'))

# Reading Party Colours
partyColours = {}
for party in partyNames:
    partyColours[party] = config.get('partyColours', party)

edgelist = []


def append_graph(username, connections):
    gen = (c for c in connections if
           (c in allPartyUsers and (c, username) not in edgelist and (username, c) not in edgelist))
    for c in gen:
        edgelist.append((c, username))


def get_edges():
    for post in db[statistics_collection].find({'party': {'$ne': 'none'}, 'value.posts': {'$gt': 5}}):
        append_graph(post['_id'], list(set(post['value']['friends'])))
    print "list is ready"
    print("Number of edges:")
    print(len(edgelist))
    # write edges to file
    with open('edgelistParties', 'w') as f:
        for t in edgelist:
            line = ' '.join(str(x) for x in t)
            f.write(line + '\n')


def get_colour(label):
    for party in partyNames:
        if label in partyUsers[party]:
            # print 'colorized: '+label+' '+str(len(label))
            return partyColours[party]
    # print 'grey: '+label+' '+str(len(label))
    return 'grey'


def init_graph():
    with open('edgelistParties', 'r') as f:
        mentions = [(line.rstrip().split(" ")[0], line.rstrip().split(" ")[1]) for line in f]
    mentions = sorted(mentions)

    # Now convert the dates/mention to edges and weights
    nodeA, nodeB = zip(*mentions)
    nodes = set(nodeA) | set(nodeB)
    nodes = sorted(list(nodes))
    print("number of nodes:")
    print(len(nodes))
    nodeMap = dict([(v, i) for i, v in enumerate(nodes)])
    edges = [(nodeMap[e[0]], nodeMap[e[1]]) for e in mentions]
    edges, weights = map(list, zip(*[[e, edges.count(e)] for e in set(edges)]))
    g = Graph(edges)
    g.es['weight'] = weights
    g.vs['label'] = nodes
    g.vs["color"] = [get_colour(label) for label in g.vs['label']]

    # g.vs["color"]

    layout = g.layout("kamada_kawai")
    out = plot(g, layout=layout, vertex_size=5, vertex_label_size=0, bbox=(1000, 1000))
    out.save('graph2.png')


# plot(g, layout = layout, vertex_label_dist=1,vertex_size=10, bbox = (1000, 1000), margin = 20)

if __name__ == '__main__':
    get_edges()
    init_graph()
