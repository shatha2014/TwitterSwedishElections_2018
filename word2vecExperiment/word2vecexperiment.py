import os

import numpy as np
import codecs

# import word2vec
from gensim.models import Word2Vec
from sklearn.cluster import KMeans

#create tweets file with no extra signs
def create_clean_tweetFile():
    filepath = 'sverige_tweets.csv'
    data = []
    with open(filepath, encoding="utf-8") as fp:
        line = fp.readline()
        while line:
            line = fp.readline()
            s = line.strip('" [ ] "" \n')
            data.append(s.lower())

    with open("cleanTweets.txt","a", encoding="utf-8") as fp:
        for d in data:
            fp.write(d+'\n')

# define training data

#Train word2vec models.
#Skip-gram or cbow test
def train_model():
    filepath = 'NoStopTweets.txt'
    data = []
    with open(filepath, encoding="utf-8") as fp:
        line = fp.readline()
        while line:
            data.append(line.strip('" [ ] "" \n').split())
            line = fp.readline()

    print(data[1])
    # train model
    SkipGrammodel = Word2Vec(data, size= 300,min_count=1, window= 3 , workers = 4, sg =1, iter = 15 )

    CBOWModel = Word2Vec(data, size= 300,min_count=1, window= 3, workers = 4, sg =0, iter = 15 )
    # summarize the loaded model
    print(SkipGrammodel)
    words = list(SkipGrammodel.wv.vocab)
    print(words)
# print(words)
# access vector for one word
    result = SkipGrammodel.most_similar(positive = ['gammal'], topn=5)
    print(result)

    result = CBOWModel.most_similar(positive = ['gammal'], topn=5)
    print(result)

# save model
    SkipGrammodel.save('SkipGrammodel.bin')
    CBOWModel.save('CBOWModel.bin')
# For every data line
# Get the vector value of each word
# Get the medium value of the vector
# Save that value for the tweet in dictionary
# Do k-means algorithm on the vectors saved for the tweets
# See what the results from the clustering is.
def use_model(model, figureName, labelstext):
    # load model
    new_model = Word2Vec.load(model)
    print(new_model.vector_size)
    print(new_model.wv.get_vector("glennstrid").shape)
    print(new_model.wv.get_vector("riksdagsledamot").reshape((1,300)))
    i = 0
    tweetVectorValue = np.zeros((1, new_model.vector_size), dtype='float32')
    tweetVecArray = np.zeros((1669284,new_model.vector_size), dtype='float32')
    print(tweetVecArray.shape)

    print(tweetVecArray[0])
    fp = codecs.open('NoStopTweets.txt', encoding='utf-8')
    line = fp.readline()
    while line:
        words = line.split()
        length = len(words)
        if length == 0:
            tweetVecArray[i] = np.zeros((1, new_model.vector_size), dtype='float32')
        else:
            for word in words:
                tweetVectorValue = np.add(tweetVectorValue, new_model.wv.get_vector(word).reshape((1,300)))
            tweetVecArray[i] = np.divide(tweetVectorValue, float(length))
        line = fp.readline()
        tweetVectorValue = np.zeros((1, new_model.vector_size), dtype='float32')
        if i % 100000 == 0:
            print(i)
        i = i + 1
    fp.close()
    print(i)

    print("start k-means")
    kmeans = KMeans(n_clusters=20).fit(tweetVecArray)
    labels = kmeans.labels_
    f = open(labelstext, 'w+')
    for label in labels:
        f.write(str(label) + '\n')
    f.close()

if __name__ == '__main__':
    #get the tweets from the db
    # os.system('''mongoexport -d test -c "sverige" -fields stagged_text --csv -o sverige_tweets.csv''')
    #train_model()
    use_model('SkipGrammodel.bin', 'skip.png', 'skip20.txt')
    use_model('CBOWModel.bin', 'cbow.png', 'cbow20.txt')
