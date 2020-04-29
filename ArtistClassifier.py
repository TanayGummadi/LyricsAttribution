import json
import sys
import re
import random
import nltk
import timeit
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from timeit import default_timer as timer

class ArtistClassifier:

    def __init__(self, inputFile, featuresetSize=5000000, testRatio=0.15):
        self.inputFile = inputFile
        self.documents = []
        self.words = []
        self.featuresetSize = featuresetSize
        self.testRatio = testRatio
        self.featureWords = None
        self.classifier = None

    def read_json(self):
        with open(self.inputFile, 'r') as readFile:
            songDict = json.load(readFile)
            for artistName in songDict:
                for song in songDict[artistName]:

                    originalLyrics = songDict[artistName][song]
                    stopWords = set(stopwords.words('english'))
                    extraStopWords = ["re", "ve", "t", "m", "d", "s"]
                    for stopWord in extraStopWords:
                        stopWords.add(stopWord)
                    lyrics, artistName = re.findall('\w+', ''.join(originalLyrics[:]).lower()), artistName
                    porter = PorterStemmer()
                    lyrics = [porter.stem(w) for w in lyrics if w not in stopWords]

                    for word in lyrics:
                        self.words.append(word.lower())

                    self.documents.append((lyrics, artistName))

    def generate_word_features(self):
        frequencyDist = nltk.FreqDist()
        for word in self.words:
            frequencyDist[word] += 1
        self.featureWords = list(frequencyDist)[:self.featuresetSize]

    def document_features(self, document):
        documentWords = set(document)
        features = {}
        for word in self.featureWords:
            features['contains({})'.format(word)] = (word in documentWords)
        return features

    def train_naive_bayes_classifier(self):
        if not self.featureWords:
            self.read_json()
            self.generate_word_features()
        random.shuffle(self.documents)
        feature_sets = [(self.document_features(d), c) for (d, c) in self.documents]
        cutoff = int(len(feature_sets) * self.testRatio)
        trainSet, testSet = feature_sets[cutoff:], feature_sets[:cutoff]
        self.classifier = nltk.NaiveBayesClassifier.train(trainSet)
        return (nltk.classify.accuracy(self.classifier, trainSet)*100, nltk.classify.accuracy(self.classifier, testSet)*100)

    def classify_new_song(self, lyrics):
        if not self.featureWords:
            self.read_json()
            self.generate_word_features()
        testFeatures = {}
        for word in self.featureWords:
            stopWords = set(stopwords.words('english'))
            extraStopWords = ["re", "ve", "t", "m", "d", "s"]
            for stopWord in extraStopWords:
                stopWords.add(stopWord)
            lyrics = re.findall('\w+', ''.join(lyrics[:]).lower())
            porter = PorterStemmer()
            lyrics = [porter.stem(w) for w in lyrics if w not in stopWords]
            testFeatures['contains({})'.format(word.lower())] = (word.lower() in lyrics)
        return self.classifier.classify(testFeatures)

    def test_new_songs(self, path):
        with open(path, 'r') as readFile:
            testDict = json.load(readFile)
            for artistName in testDict:
                for song in testDict[artistName]:
                    lyrics = testDict[artistName][song]
                    classifiedArtist = artistClassifier.classify_new_song(lyrics)
                    print("Song: {}, By: {}; Classified as artist: {}".format(song, artistName, classifiedArtist))

if __name__== "__main__":
    if(len(sys.argv) != 3 or not sys.argv[1].endswith('.json') or not sys.argv[2].isdigit()):
        print("Invalid args")
        sys.exit(1)
    artistClassifier = ArtistClassifier(inputFile=sys.argv[1])
    totalTrials = int(sys.argv[2])
    totalTestAcc = 0
    totalTrainAcc = 0
    start = timer()
    for i in range(totalTrials):
        print("Starting run {} of {}...".format(i+1, totalTrials))
        curTestAcc = artistClassifier.train_naive_bayes_classifier()[0]
        curTrainAcc = artistClassifier.train_naive_bayes_classifier()[1]
        totalTestAcc += curTestAcc
        totalTrainAcc += curTrainAcc
        print("Run {} Train Acc: {:.2f}, Test Acc: {:.2f}".format(i+1, curTestAcc, curTrainAcc))
    end = timer()
    print("In {} runs: Train Acc: {:.2f}, Test Acc: {:.2f}. Time Elapsed: {} seconds".format(totalTrials, totalTestAcc/totalTrials, totalTrainAcc/totalTrials, end-start))



