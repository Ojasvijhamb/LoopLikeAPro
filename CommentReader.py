import tokenize

def getLineWithNumber(filename):
    tokens = tokenize.open(filename)
    line = tokens.readline()
    lineNumber = 1
    lineWithNumber = []
    while line != '':
        lineWithNumber.append((line, lineNumber))
        line = tokens.readline()
        lineNumber += 1
    return lineWithNumber

def getLinesCommentedParallel(lines):
    lineNumbersToMakeParallel = []
    for line in lines:
        if ('#parallel') in line[0]:
            lineNumbersToMakeParallel.append(line[1])
    return lineNumbersToMakeParallel
