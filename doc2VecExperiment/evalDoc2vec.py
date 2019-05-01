import collections

import codecs
from sklearn.metrics.pairwise import cosine_similarity


from gensim.models import Doc2Vec
#Update the evaluation file to work with when the model is trained on uniqe tweets
def update_eval_file():
    filepath = 'NoStopTweets.txt'
    data = []
    dataDict = collections.OrderedDict()
    # with open(filepath, encoding="utf-8") as fp:
    fp = codecs.open(filepath, encoding='utf-8')
    line = fp.readline()
    while line:
        dataDict[line.strip('\n')] = 1
        line = fp.readline()
    fp.close()
    print(len(dataDict.keys()))
    data = list(dataDict.keys())

    fp = codecs.open('testTwe.txt', encoding='utf-8')
    line = fp.readline()
    line = fp.readline().strip('" [ ] "" \n')
    tweetvec = [0, 0, 0]
    f = codecs.open('NewTestIds.csv','w+', encoding='utf-8')


    while line:
        tweets = line.split(',')
        for i in range(0, 3):
            x = 0
            while x < len(data):
                if data[x].strip() == tweets[i].strip():
                    tweetvec[i] = x
                    break
                x += 1
        f.write(str(tweetvec[0])+','+str(tweetvec[1])+','+str(tweetvec[2])+'\n')
        line = fp.readline().strip('\n').strip('" [ ] "" \n')
    f.close()
    fp.close()

#Test the doc2vec model using evaluation file.
def use_model_doc2vc(model):
    new_model = Doc2Vec.load(model)
    test_size = 0
    correct = 0
    tweetvec = [0, 0, 0]
    print(len(new_model.docvecs))
    fp = codecs.open('NewTestIds.csv', encoding='utf-8')
    line = fp.readline()
    line = fp.readline().strip('\n')
    print(line)
    while line:
        tweets = line.split(',')
        for i in range(0, 3):
            tweetvec[i] = new_model.docvecs[int(tweets[i])].reshape(1, -1)
        test_size += 1
        trueVecSim = cosine_similarity(tweetvec[0], tweetvec[1])
        falseVecSim = cosine_similarity(tweetvec[0], tweetvec[2])
        if trueVecSim.item(0) > falseVecSim.item(0):
            correct += 1
        line = fp.readline().strip('\n')
    fp.close()
    print(model + " accuracy: " + str(float(correct) / test_size))
#Test the accuracy of concanated model
def use_model_ConcaTdoc2vc(model):
    new_model = Doc2Vec.load(model)
    test_size = 0
    correct = 0
    tweetvec = [0, 0, 0]
    fp = codecs.open('testTwe.txt', encoding='utf-8')
    line = fp.readline()
    line = fp.readline().strip('\n')
    while line:
        tweets = line.split(',')
        for i in range(0, 3):
            tweetvec[i] = new_model.infer_vector(tweets[i].split(' ')).reshape(1, -1)
        test_size += 1
        trueVecSim = cosine_similarity(tweetvec[0], tweetvec[1])
        falseVecSim = cosine_similarity(tweetvec[0], tweetvec[2])
        if trueVecSim.item(0) > falseVecSim.item(0):
            correct += 1
        line = fp.readline().strip('\n')
    fp.close()
    print(model + " accuracy: " + str(float(correct) / test_size))


def eval_doc():
    use_model_doc2vc("DmModelV100W3.bin")
    use_model_doc2vc("DmModelV100W5.bin")


    use_model_doc2vc("DmModelV200W3.bin")
    use_model_doc2vc("DmModelV200W5.bin")



    use_model_doc2vc("DmModelV300W5.bin")
    use_model_doc2vc("DmModelV300W3.bin")



    use_model_doc2vc("DBOWmodelV100W3.bin")
    use_model_doc2vc("DBOWmodelV100W5.bin")

    use_model_doc2vc("DBOWmodelV200W3.bin")
    use_model_doc2vc("DBOWmodelV200W5.bin")

    use_model_doc2vc("DBOWmodelV300W3.bin")
    use_model_doc2vc("DBOWmodelV300W5.bin")


    use_model_doc2vc("DBOWmodelV200W5Min1.bin")
    use_model_doc2vc("DBOWmodelV200W5Min5.bin")



    use_model_doc2vc("DBOWmodelV300W5Min1.bin")
    use_model_doc2vc("DBOWmodelV300W5Min5.bin")

    use_model_doc2vc("DmModelV300W5Min1.bin")
    use_model_doc2vc("DmModelV300W7Min1.bin")
    use_model_doc2vc("DmModelV300W3Min1.bin")

def eval_doc_Concat():
    use_model_ConcaTdoc2vc("concatDBOWmodelV200W3.bin")
    use_model_ConcaTdoc2vc("concatDBOWmodelV200W5.bin")
    use_model_ConcaTdoc2vc("concatDBOWmodelV300W3Min1.bin")
    use_model_ConcaTdoc2vc("concatDBOWmodelV300W5.bin")
    use_model_ConcaTdoc2vc("concatDBOWmodelV300W5Min1.bin")
    use_model_ConcaTdoc2vc("concatDBOWModelV300W7Min1.bin")

    use_model_ConcaTdoc2vc("concatDmModelV200W3.bin")
    use_model_ConcaTdoc2vc("concatDmModelV200W5.bin")
    use_model_ConcaTdoc2vc("concatDmModelV300W5Min1.bin")
    use_model_ConcaTdoc2vc("concatDmModelV300W5.bin")
    use_model_ConcaTdoc2vc("concatDMmodelV300W3.binMin1")
    use_model_ConcaTdoc2vc("concatDmModelV300W7Min1.bin")

if __name__ == '__main__':
    #use_model_doc2vc("newDBOWmodelV300W3.bin")
    #use_model_doc2vc("newDBOWmodelV300W5.bin")
    #use_model_doc2vc("newDBOWmodelV300W5Min1.bin")

    #use_model_doc2vc("newDmModelV300W5Min1.bin")
    #use_model_doc2vc("newDmModelV300W5.bin")
    #use_model_doc2vc("newDMmodelV300W3.bin")
    #eval_doc()
    eval_doc_Concat()

    #update_eval_file()

