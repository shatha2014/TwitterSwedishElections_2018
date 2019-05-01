from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

#Get the tweets corosponding to the cluster the tweet is in and count the most common word of each cluster
def get_tweets(cluster,labels):
    line_number = 0
    tweet_list = [None]*20
    tweets = []
    with open("NoStopTweets.txt", encoding="utf-8") as fp:
        line = fp.readline()
        while line:
            s = line.strip('\n')
            tweets.append(s)
            line = fp.readline()

    for i in range(0,20):
        tweet_list[i] = []
    with open(cluster, encoding="utf-8") as fp:
        line = fp.readline().strip('\n')
        while line:
            for word in tweets[line_number].split():
                tweet_list[int(line)].append(word)
            line = fp.readline().strip('\n')
            line_number += 1
    f = open(labels,'w',encoding="utf-8")
    for i in range(0, 20):
        cnt = Counter()
        for word in tweet_list[i]:
            cnt[word] += 1
        print("Cluster "+ str(i)+" ")
        for item in cnt.most_common(5):
            f.write(item[0] + " ")
            print(item)
        f.write("\n")
    f.close()

#Plot the clusters with the labels choosen
def plot(clusterFile,labelsFile,img):
    print(clusterFile)
    clusters = []
    labels = []
    with open(clusterFile, encoding="utf-8") as fp:
        line = fp.readline().strip('\n')
        while line:
            clusters.append(int(line))
            line = fp.readline().strip('\n')
    with open(labelsFile, encoding="utf-8") as fp:
        line = fp.readline().strip('\n')
        while line:
            labels.append(line)
            line = fp.readline().strip('\n')
    df = pd.DataFrame(clusters)
    #plt.switch_backend('Agg')
    ax = df[0].value_counts().plot(kind='bar', figsize=(15, 15))
    print(df[0].value_counts())
    xlabels = [item.get_text() for item in ax.get_xticklabels()]
    xNewLabels = []
    i = 1
    for label in xlabels:
        newX = str(i)+ ". " + labels[int(label)]
        print(newX)
        xNewLabels.append(newX)
        i += 1
    ax.set_xticklabels(xNewLabels)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=22, ha="right", rotation_mode="anchor")

    plt.ylabel('Tweets in cluster', fontsize=12)

    plt.savefig(img)

if __name__ == '__main__':
    #get_tweets("fast.txt","fastLabels.txt")
    #get_tweets("cbow.txt", "cbowLabels.txt")
    #get_tweets("skip.txt", "skipLabels.txt")
    #get_tweets("skip20.txt", "skipLabels20.txt")
    #get_tweets("cbow20.txt", "cbowLabels20.txt")
    #get_tweets("fast20.txt", "fastLabels20.txt")

    #get_tweets("dbow15.txt","dbow15Labels.txt")
    #get_tweets("dbow20.txt", "dbow20Labels.txt")
    #get_tweets("dm15.txt", "dm15Labels.txt")
    #get_tweets("dm20.txt", "dm20labels.txt")

    get_tweets("dm20New.txt", "dm20newLabels.txt")
    get_tweets("dmbowConcat20.txt", "dbowConcat20Labels.txt")
    #get_tweets("dm20.txt", "dm20labels.txt")

    #plot("dbow15.txt","dbow15Labels.txt", "dbow15.png")
    #plot("dbow20.txt", "dbow20Labels.txt", "dbow20.png")
    #plot("dm15.txt", "dm15Labels.txt", "dm15.png")
    #plot("dm20.txt", "dm20labels.txt", "dm20.png")

    #plot("fast20.txt", "fastLabels20.txt", "fast20.png")
    #plot("skip20.txt", "skipLabels20.txt", "skip20.png")
    #plot("cbow20.txt", "cbowLabels20.txt", "cbow20.png")

    plot("dm20New.txt", "dm20newLabels.txt", "dm20New.png")
    plot("dmbowConcat20.txt", "dbowConcat20Labels.txt", "dmbowConcat20.png")

    #plot("fast.txt","fastLabels.txt","fast.png")
    #plot("cbow.txt", "cbowLabels.txt", "cbow.png")
    #plot("skip.txt", "skipLabels.txt", "skip.png")