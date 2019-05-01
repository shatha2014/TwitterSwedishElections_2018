import collections

from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from sklearn.cluster import KMeans
import numpy as np
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#Train dofc2vec model
def train_model(modelName,dmYes,vectorS,windowS,mCount):

    print(len(documents))
    print(documents[0])

    print(modelName + "start training")

    model = Doc2Vec(dm =dmYes, vector_size=vectorS, min_count = mCount, window=windowS, workers=4, epoch = 20)
    model.build_vocab(documents)
    model.train(documents, total_examples=model.corpus_count, epochs=model.iter)

    print(model.docvecs.count)
    # save model
    model.save(modelName)

#Cluster the tweets using the choosen model
def use_model(model, labelstext,clusters):
    # load model
    new_model = Doc2Vec.load(model)

    tweetVecArray = np.zeros((1669284,new_model.vector_size), dtype='float32')
    print(tweetVecArray.shape)
    fp = codecs.open('NoStopTweets.txt', encoding='utf-8')
    line = fp.readline()
    i = 0
    while line:
        words = line.split()
        tweetVecArray[i] = new_model.infer_vector(words).reshape(1, -1)
        line = fp.readline()
        if i % 100000 == 0:
            print(i)
        i = i + 1
    fp.close()

    print(tweetVecArray[len(tweetVecArray)-1])
    print("Start clustering.")
    kmeans = KMeans(n_clusters=clusters).fit(tweetVecArray)
    labels = kmeans.labels_
    print(len(labels))
    f = open(labelstext, 'w+')
    for label in labels:
        f.write(str(label)+'\n')
    f.close()

def train_all_models():
    train_model("DmModelV100W3.bin",1,100,3,2)
    train_model("DmModelV100W5.bin",1,100,5,2)

    train_model("DmModelV200W3.bin",1,200,3,2)
    train_model("DmModelV200W5.bin",1,200,5,2)

    train_model("DmModelV300W3.bin",1,300,3,2)
    train_model("DmModelV300W5.bin",1,300,5,2)


    train_model("DBOWmodelV100W3.bin",0,100,3,2)
    train_model("DBOWmodelV100W5.bin",0,100,5,2)

    train_model("DBOWmodelV200W3.bin",0,200,3,2)
    train_model("DBOWmodelV200W5.bin",0,200,5,2)

    train_model("DBOWmodelV300W3.bin",0,300,3,2)
    train_model("DBOWmodelV300W5.bin",0,300,5,2)

    train_model("DBOWmodelV200W5Min1.bin", 0, 200, 5, 1)
    train_model("DBOWmodelV200W5Min5.bin", 0, 200, 5, 5)

    train_model("DBOWmodelV300W5Min1.bin", 0, 300, 5, 1)
    train_model("DBOWmodelV300W5Min5.bin", 0, 300, 5, 5)

    train_model("DmModelV300W5Min1.bin",1,300,5,1)

    train_model("DmModelV300W7Min1.bin",1,300,7,1)
    train_model("DmModelV300W3Min1.bin",1,300,3,1)

def train_concat():
    train_model("concatDBOWmodelV200W3.bin",0,200,3,2)
    train_model("concatDBOWmodelV200W5.bin",0,200,5,2)
    train_model("concatDBOWmodelV300W3Min1.bin",0,300,3,1)
    train_model("concatDBOWmodelV300W5.bin",0,300,5,2)
    train_model("concatDBOWmodelV300W5Min1.bin", 0, 300, 5, 1)
    train_model("concatDBOWModelV300W7Min1.bin",0,300,7,1)

    train_model("concatDmModelV200W3.bin",1,200,3,2)
    train_model("concatDmModelV200W5.bin",1,200,5,2)
    train_model("concatDmModelV300W5Min1.bin",1,300,5,1)
    train_model("concatDmModelV300W5.bin",1,300,5,2)
    train_model("concatDMmodelV300W3.binMin1", 1, 300, 3, 1)
    train_model("concatDmModelV300W7Min1.bin",1,300,7,1)
if __name__ == '__main__':

    # define training data
    filepath = 'NoStopTweets.txt'
    # filepath = 'concatTweets.txt'
    data = []
    dataDict = collections.OrderedDict()

    # with open(filepath, encoding="utf-8") as fp:
    fp = codecs.open(filepath, encoding='utf-8')
    line = fp.readline()
    while line:
        dataDict[line.strip('" [ ] "" \n')] = 1
        line = fp.readline()
    # while line:
    #  data.append(line.split())
    #   line = fp.readline()
    # fp.close()
    print(len(dataDict.keys()))
    # data = dataDict.keys()
    for d in dataDict.keys():
        data.append(d.split(' '))
    print(data[0])
    print(len(data))

    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(data)]
    print(documents[0])

    #train_all_models()
    #train_concat
    #use_model("DBOWmodelV300W5.bin","dbow15.txt",15)
    #use_model("DmModelV300W5.bin","dm15.txt",15)
    #use_model("DBOWmodelV300W5.bin","dbow20.txt",20)
    use_model("DmModelV300W5.bin","dm20.txt",20)
    use_model("concatDBOWmodelV300W3Min1.bin", "dmbowConcat20.txt", 20)
    #use_model('test.bin', 'test.png', 'labels.txt')
    #use_model('DMmodel.bin','DMmodel.png','DMmodel.txt')
    #use_model('DBOWmodel.bin', 'DBOWmodel.png', 'DBOWmodel.txt')