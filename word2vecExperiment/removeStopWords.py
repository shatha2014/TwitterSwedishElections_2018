
stopwords= []
#get the stop words from the file
def get_stop_words():
    filepath = 'stopword.txt'
    with open(filepath, encoding="utf-8") as fp:
        line = fp.readline()
        while line:
            stopwords.append(line.strip('" [ ] "" \n'))
            line = fp.readline()

#remove stop words in the textilfe containing tweets
def r_stop_words():
    data= []
    filepath = 'cleanTweets.txt'
    with open(filepath,"r+", encoding="utf-8") as fp:
        line = fp.readline()
        while line:
            words = line.split()
            noStopWords = [word for word in words if word not in stopwords]
            done = ' '.join(noStopWords)
            data.append(done)
            line = fp.readline()

    with open("NoStopTweets.txt","a", encoding="utf-8") as fp:
        for d in data:
            fp.write(d+'\n')

if __name__ == '__main__':
    get_stop_words()
    r_stop_words()