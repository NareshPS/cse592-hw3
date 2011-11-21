#! /usr/bin/python
import subprocess
import sys

class reportWriter:
    reportText  = ''
    pdfBinary   = 'pdflatex'
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
        imageTag    = '\subfigure[]{\includegraphics[]{%s}}'
        for i in range(len(figList)-1):
            imgText = imgText + imageTag%(figList[i]) + '\quad'
        imgText = imgText + imageTag%(figList[-1]) + '}'
        imgText = imgText + '\end{figure}'
        return imgText

    def generatePdf(self):
        print 'Generating Pdf'
        subprocess.call([self.pdfBinary, self.reportFile], stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr)

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
