import numpy as np
import codecs
from sklearn.metrics.pairwise import cosine_similarity

# import word2vec
from gensim.models.wrappers import FastText
from gensim.models import Word2Vec
from gensim.models import Doc2Vec
#Evaluate word2vec model
#csv file is tweet ,same topic, different topic
def use_model_word2vc(model):
    new_model = Word2Vec.load(model)
    test_size = 0
    correct = 0
    tweetvec = [0,0,0]
    fp = codecs.open('testTwe.txt', encoding='utf-8')
    line = fp.readline()
    tweetVectorValue = np.zeros((1, new_model.vector_size), dtype='float32')
    line = fp.readline().strip('\n')
    while line:
        tweets = line.split(',')
        for i in range(0,3):
            length = len(tweets[i])
            for word in tweets[i].split():
                if word in new_model.wv.vocab:
                    tweetVectorValue = np.add(tweetVectorValue, new_model.wv.get_vector(word).reshape(1, -1))
                else:
                    length = length - 1
            tweetvec[i] = np.divide(tweetVectorValue, float(length))
        test_size += 1

        trueVecSim = cosine_similarity(tweetvec[0], tweetvec[1])
        falseVecSim = cosine_similarity(tweetvec[0], tweetvec[2])
        if trueVecSim.item(0)>falseVecSim.item(0):
            correct += 1
        tweetVectorValue = np.zeros((1, new_model.vector_size), dtype='float32')
        line = fp.readline().strip('\n')
    fp.close()
    print(model + " accuracy: " + str(float(correct)/test_size))
    print(correct)

#Evaluate the Fasttext model
def use_model_fasttext(model):
    fastModel = FastText.load_fasttext_format('cc.sv.300.bin')
    test_size = 0
    correct = 0
    tweetvec = [0,0,0]
    fp = codecs.open('testTwe.txt', encoding='utf-8')
    line = fp.readline()
    tweetVectorValue = np.zeros((1, fastModel.vector_size), dtype='float32')
    line = fp.readline().strip('\n')
    while line:
        tweets = line.split(',')
        for i in range(0,3):
            length = len(tweets[i])
            for word in tweets[i].split():
                if word in fastModel.wv.vocab:
                    tweetVectorValue = np.add(tweetVectorValue, fastModel.wv[word].reshape((1, 300)))
                else:
                    length = length - 1
            tweetvec[i] = np.divide(tweetVectorValue, float(length))
        test_size += 1

        trueVecSim = cosine_similarity(tweetvec[0], tweetvec[1])
        falsevecSim = cosine_similarity(tweetvec[0], tweetvec[2])
        if trueVecSim.item(0)>falsevecSim.item(0):
            correct += 1
        tweetVectorValue = np.zeros((1, fastModel.vector_size), dtype='float32')
        line = fp.readline().strip('\n')
    fp.close()
    print(model+ " accuracy: " + str(float(correct)/test_size))
    print(correct)

#Evaluate doc2vec models
def use_model_doc2vc(model):
    new_model = Doc2Vec.load(model)
    test_size = 0
    correct = 0
    tweetvec = [0,0,0]
    print(len(new_model.docvecs))
    fp = codecs.open('many.csv', encoding='utf-8')
    line = fp.readline()
    line = fp.readline().strip('\n')
    print(line)
    while line:
        tweets = line.split(',')
        for i in range(0,3):
            tweetvec[i] = new_model.docvecs[int(tweets[i])].reshape(1,300)
        test_size += 1
        trueVecSim = cosine_similarity(tweetvec[0], tweetvec[1])
        falseVecSim = cosine_similarity(tweetvec[0], tweetvec[2])
        if trueVecSim.item(0)>falseVecSim.item(0):
            correct += 1
        line = fp.readline().strip('\n')
    fp.close()
    print(model+ " accuracy: " + str(float(correct)/test_size))
if __name__ == '__main__':
    #use_model_word2vc('SkipGrammodel.bin')
   # use_model_word2vc('CBOWModel.bin')
    use_model_doc2vc("DmModelV100W3.bin")
    use_model_doc2vc("DmModelV100W5.bin")

    use_model_doc2vc("DmModelV200W3.bin")
    use_model_doc2vc("DmModelV200W5.bin")

    use_model_doc2vc("DmModelV300W5.bin")

    use_model_doc2vc("DBOWmodelV100W3.bin")
    use_model_doc2vc("DBOWmodelV100W5.bin")

    use_model_doc2vc("DBOWmodelV200W3.bin")
    use_model_doc2vc("DBOWmodelV200W5.bin")

    use_model_doc2vc("DBOWmodelV300W3.bin")
    use_model_doc2vc("DBOWmodelV300W5.bin")

    #use_model_fasttext('fastTextPreTrained/cc.sv.300.bin')