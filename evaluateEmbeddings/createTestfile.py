import codecs

#Create Test file with tweets insted of tweets IDS
if __name__ == '__main__':
    tweets = []
    with open("NoStopTweets.txt", encoding="utf-8") as fp:
        line = fp.readline()
        while line:
            s = line.strip('\n')
            tweets.append(s)
            line = fp.readline()

    with open("many.csv", encoding="utf-8") as fp:
        with open("testTwe.txt",'w+', encoding="utf-8") as f:
            line = fp.readline()
            line = fp.readline()
            while line:
                s = line.strip('\n').split(',')
                print(tweets[int(s[0])])
                f.write(tweets[int(s[0])]+","+tweets[int(s[1])]+","+tweets[int(s[2])]+'\n')
                line = fp.readline()
