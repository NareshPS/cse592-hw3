#! /usr/bin/python

import math
import png
import math

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

    def toPixelValue(self, value):
        return int(value)*255

    def plotImage(self, fileName, l):
        png.from_array([map(self.toPixelValue, l[i:i+32]) for i in xrange(0,len(l),32)], 'L').save(fileName)
        
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
    samples         = [1,2]
    samplesName     = "AUTO"
    samplesValues   = ["noauto", "auto"]
    attributes      = [[1,2],[1,2,3,4],[1,2],[1,2],[1,2,3,4],[1,2]]
    attribNames     = ["STABILITY", "ERROR", "SIGN", "WIND", "MAGNITUDE", "VISIBILITY"]
    attribValues    = [["stab", "xstab"],["XL", "LX", "MM", "SS"],["pp", "nn"],["head", "tail"],["Low", "Medium", "Strong", "OutOfRange"],["yes", "no"]]
    ratioCalc       = False

    def __init__(self):
        pass

    def readDataFile(self, fileName):
        fp  = open(fileName, 'r')
        return [map(int, line.strip().split()) for line in fp.readlines()]

    def loadInputFiles(self):
        self.shuttle_data   = self.readDataFile(self.shuttle)

    def chooseBestSplit(self, data, attribs):
        gain    = [(self.splitAndCompute(data, i),i) for i in attribs]
        #print gain
        maxGain = max(gain) 
        splits  = []
        attrib  = maxGain[1]
        if maxGain[0]==0.0:
            return ([], attrib)
        for i in self.attributes[attrib]:
            splits.append([])

        for sample in data:
            idx = self.attributes[attrib].index(sample[attrib+1])
            splits[idx].append(sample)
        return (splits, attrib)

    def splitAndCompute(self, data, attrib):
        curSamples  = self.countSamples(data)
        curGain     = self.gainValue(curSamples[0], curSamples[1])
        splits      = []
        newGain     = 0.0
        for i in self.attributes[attrib]:
            splits.append([])

        for sample in data:
            idx = self.attributes[attrib].index(sample[attrib+1])
            splits[idx].append(sample)

        for split in splits:
            newSamples  = self.countSamples(split)
            newGain     = newGain + (float(newSamples[0]+newSamples[1])/float(curSamples[0]+curSamples[1]))*self.gainValue(newSamples[0], newSamples[1])
        retGain = curGain-newGain
        if self.ratioCalc is True:
            return retGain/self.intrinsicValue(data, splits)
        return retGain

    def intrinsicValue(self, data, splits):
        iv      = 0.0
        lenData = len(data)
        for split in splits:
            lenSplit    = len(split)
            ratio       = float(lenSplit)/float(lenData)
            iv  = iv + (ratio*math.log(ratio, 2))

        return -iv

    def countSamples(self, data):
        p   = 0
        n   = 0
        for sample in data:
            if sample[0]==self.samples[0]:
                p   = p+1
            elif sample[0]==self.samples[1]:
                n   = n+1
        return (p,n)

    def gainValue(self, p, n):
        if p is 0 or n is 0:
            return 0.0
        pos = float(p)/float(p+n)
        neg = float(n)/float(p+n)
        return (-pos*math.log(pos, 2)-neg*math.log(neg, 2))

    def recurseSelection(self, data, attribs, default, tabs):
        counts  = self.countSamples(data)
        if len(data)==0:
            self.reportText = self.reportText + tabs + 'Prediction: ' + default
            return
        elif counts[0]==0:
            self.reportText = self.reportText + tabs + 'Prediction: ' + self.samplesValues[1]
            return
        elif counts[1]==0:
            self.reportText = self.reportText + tabs + 'Prediction: ' + self.samplesValues[0]
            return
        else:
            splits,attrib   = self.chooseBestSplit(data, attribs)
            del attribs[attribs.index(attrib)]
            col = 0
            for split in splits:
                self.reportText = self.reportText + tabs + self.attribNames[attrib] + '=' + self.attribValues[attrib][col]
                self.recurseSelection(split, list(attribs), default, tabs+'  ') 
                col = col + 1

    def runDecisionTree(self):
        self.reportText = self.reportText + '\n\subsection{Decision Tree for Information Gain}\n\\begin{verbatimtab}[8]'
        self.recurseSelection(self.shuttle_data, range(len(self.attributes)), self.samplesValues[0], '\n  ')
        self.reportText = self.reportText + '\n\end{verbatimtab}'
        self.ratioCalc  = True
        self.reportText = self.reportText + '\n\subsection{Decision Tree for Information Gain Ratio}\n\\begin{verbatimtab}[8]'
        self.recurseSelection(self.shuttle_data, range(len(self.attributes)), self.samplesValues[0], '\n  ')
        self.reportText = self.reportText + '\n\end{verbatimtab}'

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
