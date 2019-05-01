import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import codecs

# import word2vec
from gensim.models.wrappers import FastText
from sklearn.cluster import KMeans


#Get clustering results using the Fasttext model.
def use_model():
    # load model
    fastModel = FastText.load_fasttext_format('cc.sv.300.bin')

    tweetVectorValue = np.zeros((1, fastModel.vector_size), dtype='float32')
    tweetVecArray = np.zeros((1669284 ,fastModel.vector_size), dtype='float32')
    i = 0
    print(tweetVecArray.shape)
    fp = codecs.open('NoStopTweets.txt', encoding='utf-8')
    line = fp.readline()
    while line:
        words = line.split()
        length = len(words)
        for word in words:
            if word in fastModel.wv.vocab:
                 tweetVectorValue = np.add(tweetVectorValue, fastModel.wv[word].reshape((1,300)))
            else:
                length = length-1
        if length == 0:
            tweetVecArray[i] = np.zeros((1, fastModel.vector_size), dtype='float32')
        else:
            tweetVecArray[i] = np.divide(tweetVectorValue, float(length))
        line = fp.readline()
        if i % 100000 == 0:
            print(i)
        i = i + 1
        tweetVectorValue = np.zeros((1, fastModel.vector_size), dtype='float32')
    fp.close()
    print(i)

    print("start kmeans")
    kmeans = KMeans(n_clusters=20).fit(tweetVecArray)
    labels = kmeans.labels_
    f = open('fast20.txt', 'w+')
    for label in labels:
        f.write(str(label) + '\n')
    f.close()
if __name__ == '__main__':
    use_model()
