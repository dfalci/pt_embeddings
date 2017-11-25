# encoding: utf-8

from SentenceSegmenter import SentenceGenerator,SentenceBroker
from gensim.models import Word2Vec
import sys
import time

class W2VModel:

    def __init__(self, modelFile='model.vec'):
        self.modelFile = modelFile
        self.model = None
        self.sentences = None
        self.inputFile = None
        self.inputDirectory = None
        self.bigram = None
        self.trigram = None
        self.quadrigram = None
        self.sentenceBroker = SentenceBroker()

    def train(self, embeddingSize=150, epochs=10, windowSize=5, minimalCount=5, inputDirectory='./', inputFile='wiki_00', seed=13, threads=4):
        """
        Treina um modelo de palavras do tipo skipgram
        :param inputDirectory:
        :param inputFile:
        :return:
        """
        start = time.time()
        self.inputDirectory = inputDirectory
        self.inputFile = inputFile

        self.sentences = SentenceGenerator(dirname=self.inputDirectory, fname=self.inputFile)
        self.model = Word2Vec(self.sentences, seed=seed, sg=1, size=embeddingSize, iter=epochs, window=windowSize, min_count=minimalCount, workers=threads)
        self.model.save(self.modelFile)

        print 'Sentencas : '+str(self.sentences.sentNum)
        print 'Tokens : '+str(self.sentences.tokenNum)
        print 'Articles : '+str(self.sentences.artNum)
        print 'Tempo decorrido para treinar o modelo '+str(time.time() - start)
        sys.stdout.flush()

    def load(self):
        """
        Carrega o modelfile indicado no construtor
        :return:
        """
        self.model = Word2Vec.load(self.modelFile)

    def getRawVector(self, word):
        """
        Captura o vetor de n dimensoes dada uma palavra qualquer
        :param word:
        :return:
        """
        return self.model[self.sentenceBroker.prepareLine(word)]


    def getSimilarity(self, w1, w2):
        """
        Dadas duas palavras, calcula o grau de similaridade a partir do coseno
        :param w1:
        :param w2:
        :return:
        """
        return self.model.similarity(self.sentenceBroker.prepareLine(w1), self.sentenceBroker.prepareLine(w2))


    def getNotInContext(self, values):
        """
        Dada uma colecao de palavras, verifica quais delas nao estao presentes no contexto
        :param values:
        :return:
        """
        val = []
        for este in values:
            val.append(self.sentenceBroker.prepareLine(este))
        return self.model.doesnt_match(val)


    def getMostSimilar(self, positive, number=10, negative=[]):
        """
        dado um conjunto de palavras retorna a mais similar a uma palavra chave
        :param positive:
        :param number:
        :param negative:
        :return:
        """
        val = []
        for este in positive:
            val.append(self.sentenceBroker.prepareLine(este))

        return self.model.most_similar(val, negative, number)


if __name__ == '__main__':
    dimensions = int(sys.argv[1])
    filename = 'model'+str(dimensions)+'.vec'

    print 'treinando modelo com '+str(dimensions)

    model = W2VModel(filename)
    model.train(dimensions, 10, 5, 5, './', 'wiki_00', 13, 3)
    print 'Ended'
