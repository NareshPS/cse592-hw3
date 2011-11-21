#! /usr/bin/python

import math
from PIL import Image
import struct

import reportWriter

class Prob1:
    '''
        This class solves problem 1 of HW 3.
    '''
    train           = 'optdigits_tra.dat'
    train_trans     = 'optdigits_tra_trans.dat'
    trial           = 'optdigits_trial.dat'
    trial_trans     = 'optdigits_trial_trans.dat'
    imgExtn         = '.png'
    reportText      = '\n\section{Problem 1}'

    def __init__(self):
        pass

    def readDataFile(self, fileName):
        fp  = open(fileName, 'r')
        return [map(int, line.strip().split()) for line in fp.readlines()]

    def loadInputFiles(self):
        self.train_data         = self.readDataFile(self.train)
        self.train_trans_data   = self.readDataFile(self.train_trans)
        self.trial_data         = self.readDataFile(self.trial)
        self.trial_trans_data   = self.readDataFile(self.trial_trans)

    def top3Indices(self, distance):
        return sorted(range(len(distance)), key=distance.__getitem__)[:3]

    def computeDistance(self, i_v, j_v):
        return math.sqrt(sum([(float(x[0])-float(x[1]))**2 for x in zip(i_v, j_v)]))

    def find3Neighbors(self, train_d, trial_d):
        distances   = []
        for i in trial_d:
            distances.append([self.computeDistance(i[:64],j[:64]) for j in train_d])
        return [self.top3Indices(dist) for dist in distances]

    def plotImage(self, fileName, bitStream):
        bitStream.reverse()
        imgBuffer   = ''.join([chr(bitStream[i*32+j]*255) for i in range(32) for j in range(32)])
        img = Image.frombuffer('L', (32,32), imgBuffer)
        img.save(fileName)

    def plotGroup(self, trial_i, train_i):
        imageList   = []
        self.plotImage(str(trial_i)+self.imgExtn, self.trial_data[trial_i][:1024]) 
        imageList.append(str(trial_i)+self.imgExtn)
        for i in train_i:
            self.plotImage(str(trial_i)+'_'+str(i)+self.imgExtn, self.train_data[i][:1024])
            imageList.append(str(trial_i)+'_'+str(i)+self.imgExtn)

        self.reportText = self.reportText + reportWriter.reportWriter.addFigures(imageList)

    def runKNN(self):
        i   = 0
        for top3 in self.find3Neighbors(self.train_trans_data, self.trial_trans_data):
            self.plotGroup(i, top3)
            i   = i+1

    def getReportText(self):
        return self.reportText

class Prob2:
    shuttle         = 'shuttle_ext_unique.dat'
    imgExtn         = '.png'
    reportText      = '\n\section{Problem 2}'

    def __init__(self):
        pass

    def readDataFile(self, fileName):
        fp  = open(fileName, 'r')
        return [map(int, line.strip().split()) for line in fp.readlines()]

    def loadInputFiles(self):
        self.shuttle_data   = self.readDataFile(self.shuttle)

    def runDecisionTree(self):
        pass

    def getReportText(self):
        return self.reportText

if __name__ == '__main__':
    p1  = Prob1()
    p1.loadInputFiles()
    p1.runKNN()
    rt1 = p1.getReportText()

    p2  = Prob2()
    p2.loadInputFiles()
    p2.runDecisionTree()
    rt2 = p2.getReportText()


    r   = reportWriter.reportWriter('Report.tex', 'latex.tmpl.tex')
    r.appendToReport(rt1)
    r.appendToReport(rt2)
    r.writeReport()
