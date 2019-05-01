import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('confTopic.cfg')
partyNames = config.get('parties', 'names').split(',')

#Create lines of the exported files.
if __name__ == '__main__':
    for party in partyNames:
        f = open(party+".csv", 'r+')
        n = f.read().replace(',', ',\n')
        f.truncate(0)
        f.write(n)
        f.close()
