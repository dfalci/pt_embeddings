# encoding: utf-8
import os
import io
import re
import sys
from nltk.tokenize import RegexpTokenizer
import unicodedata
import nltk


class SentenceGenerator:
    """
    Objeto responsavel por iterar no arquivo indicado gerando sentencas de maneira natural.
    """

    def __init__(self, dirname, fname):
        self.dirname = dirname
        self.fname = fname
        self.sentenceBroker = SentenceBroker()
        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
        self.sentNum = 0
        self.tokenNum = 0
        self.artNum = 0

    def __iter__(self):
        """
        itera no arquivo
        :return:
        """
        for line in io.open(os.path.join(self.dirname, self.fname), encoding="utf-8"):
            if not self.sentenceBroker.mustSkip(line):
                for frase in self.sent_tokenizer.tokenize(line):
                    value = self.sentenceBroker.transformSentence(frase)
                    #print the current iteration status on every 10,000 examples
                    if self.sentNum % 10000 == 0:
                        print 'sentenca : '+str(self.sentNum)
                        print 'tokens : '+str(self.tokenNum)
                        print 'art : '+str(self.artNum)
                        sys.stdout.flush()
                    #if self.sentNum > 50000:
                    #    return
                    self.sentNum = self.sentNum + 1
                    self.tokenNum = self.tokenNum + len(value)
                    yield value
            else:
                #detects the beggining of the file and resets the value
                if '<doc' in line:
                    if 'title = "Astronomia">' in line:
                        print 'iteracao finalizada'
                        print 'sentenca : '+str(self.sentNum)
                        print 'tokens : '+str(self.tokenNum)
                        print 'art : '+str(self.artNum)
                        sys.stdout.flush()
                        self.artNum = 0
                        self.sentNum = 0
                        self.tokenNum = 0
                    self.artNum = self.artNum + 1

class SentenceBroker:
    """
    Quebra a linha
    """

    def __init__(self):
        self.skipElements= (
            '<doc',
            '</doc'
        )

    def mustSkip(self, line):
        """
        returns true if at least one of the reserved elements of wikipedia is being mapped
        :param line:
        :return:
        """
        for este in self.skipElements:
            if este in line:
                return True
        return False

    def prepareLine(self, line):
        line = line.rstrip('\n')

        # email e url
        line = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+', ' EMAIL ', line)
        line = re.sub(r'(?:https?://)?\w+(?:\.\w+)+(?:/\w+)*', ' URL ', line)
        line = re.sub(r'(?:[\#@]\w+)', 'HASH_NAME', line)

        line = line.lower()


        #transforma numeros
        line = re.sub(r'\d+(\d)*(\.\d+)*(\,\d+)*(\ \d+)?', '#', line)

        #remove os acentos
        nfkd = unicodedata.normalize('NFKD', line)
        line = u"".join([c for c in nfkd if not unicodedata.combining(c)])

        #separa as palavras com virgula
        line = re.sub(r'[ ]*,[ ]*', ' , ', line)
        line = re.sub(r'[ ]*\?[ ]*', ' ? ', line)
        line = re.sub(r'[ ]*\![ ]*', ' ! ', line)
        line = re.sub(r'[ ]*\.[ ]*', ' . ', line)
        line = re.sub(r'[ ]*\:[ ]*', ' : ', line)
        line = re.sub(r'[ ]*\"[ ]*', ' " ', line)
        line = re.sub(r'[ ]*\'[ ]*', " ' ", line)
        line = re.sub(r'[ ]*\([ ]*', ' ( ', line)
        line = re.sub(r'[ ]*\)[ ]*', ' ) ', line)
        line = re.sub(r'[ ]*\;[ ]*', ' ; ', line)
        return line

    def transformSentence(self, line):
        line = self.prepareLine(line)
        return line.strip().split(' ')

    #captura todas as sentencas de uma linha
    def splitSentence(self, line):
        yield line.split(' ')
        #yield self.tokenize(line)
