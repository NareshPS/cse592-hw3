#! /usr/bin/python

class reportWriter:
    reportText  = ''
    def __init__(self, reportFile, tmplFile):
        self.reportFile = reportFile
        self.tmplFile   = tmplFile

    def appendToReport(self, chunk):
        self.reportText = self.reportText + chunk

    @staticmethod
    def addFigures(figList):
        imgText = '''\n \\begin{figure}[H]
    \centering
    \mbox{
        '''
        imageTag    = '\subfigure[]{\includegraphics[width=0.25\\textwidth]{%s}}'
        for i in range(len(figList)-1):
            imgText = imgText + imageTag%(figList[i]) + '\quad'
        imgText = imgText + imageTag%(figList[-1]) + '}'
        imgText = imgText + '\end{figure}'
        return imgText

    def putInTable(self, listData):
        pass

    def writeReport(self):
        f   = open(self.reportFile, 'w')
        t   = open(self.tmplFile, 'r')
        for line in t.readlines():
            f.write(line)
        t.close()
        if self.reportText is not None:
            f.write(self.reportText)
        f.write('\n\n\end{document}')
        f.close()
