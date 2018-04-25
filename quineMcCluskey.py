from numpy import*
import time
import itertools


prec = {"=":1,'*':5, ">":2,"+":3,"^":4, "~":6,"(":0, ")":0}
ops = set(["+",">","=","^","~",'*'])

def listOfVars(tokens):
    howMany = 0
    mySet = set()
    for token in tokens:
        isAlpha = True
        for char in token:
            if not char.isalpha():
                isAlpha = False
        if  isAlpha and  token not in mySet:
            howMany += 1
            mySet = mySet.union({token})
    return sorted((mySet))


def createTab(howMany):
    if howMany == 0:
        return []
    i = 0
    tab = zeros((2**howMany, howMany),int)    
    for x in range(2**howMany):
        j = 0
        x = bin(x)[2:].zfill(howMany)
        x = str(x)
        for y in x:
            tab[i][j] = str(y)
            j += 1
        i += 1
    return tab

def compare(x, y):
    if x.count('0') < y.count('0'):
        return -1
    else:
        return 1


def alternative(el1, el2):
    if el1 == '1' or el2 == '1':
        return '1'
    else: 
        return '0'


def implication(el1, el2):
    if el1 == '1' and el2 == '0':
        return '0'
    else: 
        return '1'
    
    
def equivalence(el1, el2):
    if el1 == el2:
        return '1'
    else:
        return '0'
    
    
def xor(el1, el2):
    if el1 == el2:
        return '0'
    else:
        return '1'

def conjunction(el1, el2):
    if el1 == '1' and el2 == '1':
        return '1'
    else:
        return '0'
    
def executeLogicExpr(operant, el1, el2):
    if operant == '+': return alternative(el1, el2)
    if operant == '>': return implication(el1, el2)
    if operant == '=': return equivalence(el1, el2)
    if operant == '^': return  xor(el1, el2)
    if operant == '*': return conjunction(el1, el2)
    
    
def executeNegation(el):
    if el == '1':
        return '0'
    else:
        return '1'
    
    
def reasult(tokens):
    if len(tokens) == 1:
        return tokens
    else:
        isNeg = False
        fstOp = 0
        i = 0
        for token in tokens:
            if not str(token).isdigit() and fstOp == 0:
                if token == '~':
                    isNeg = True
                else:
                    isNeg = False
                fstOp = i
            i = i + 1
        if isNeg:
            return reasult(tokens[:fstOp-1] + [executeNegation(tokens[fstOp-1])] + tokens[fstOp+1:])
        else:
            return reasult(tokens[:fstOp-2] + [executeLogicExpr(tokens[fstOp], tokens[fstOp-2], tokens[fstOp-1])] + tokens[fstOp+1:]) 
                   

def checkWhenTrue(tokens, tabOfCases, vars):
    copied = tokens
    i = 0
    finalList = []
    for line in tabOfCases:
        copied = tokens
        j = 0
        for char in line:
            copied = list(map(lambda x: str(char) if vars[j] == x else str(x), copied))
            j += 1
        if reasult(copied) == ['1']:
            finalList = finalList + [i]
        i += 1
    if finalList != []:
        return finalList
    else:
        if reasult(tokens) == ['1']:
            return ['-1']
        else:
            return ['-2']
        
        

def stringToTokens(string):
    tokens =[]
    newToken = ""
    wasLastChar = False
    for char in string:
        
        if char.isalpha():
            if wasLastChar:
                newToken = newToken + char
            else:
                tokens.append(newToken)
                newToken = char
            wasLastChar = True
        else:
            tokens.append(newToken)
            newToken = char
            wasLastChar = False
    tokens.append(newToken)
    return tokens[1:]
            
        

def onpexpr(tokens):
    output = []
    stack = []
    for item in tokens:
        if item in ops:
            while stack and prec[stack[-1]] >= prec[item]:
                output.append(stack.pop())
            stack.append(item)
        elif item == "(":
            stack.append("(")
        elif item == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
        else:
            output.append(item)
    while stack:
        output.append(stack.pop())
    return output


def withoutSpaces(tokens):
    finalList = []
    for token in tokens:
        if token != '' and token != ' ':
            finalList.append(token)
    return finalList
            

def makeTuples(tokens, leng):
    if len(tokens) == 1:
        return tokens
    finalList = []
    howManyDif = 0
    for i in range(0, len(tokens)):
        for j in range(i+1, len(tokens)):
            
            for k in range (0, len(tokens[0])):
                #print("i-->", tokens[i][k], "  j -->",tokens[j][k] )
                if tokens[i][k] != tokens[j][k]:
                    howManyDif = howManyDif + 1  
            #print(tokens[i],"   " ,tokens[j], "   ", howManyDif)
            if howManyDif == 1:
                    finalList.append((tokens[i],tokens[j]))
            howManyDif = 0
    for token in tokens:
        if not token in list(itertools.chain(*finalList)):
            finalList.append((token,))
    #print(finalList)
    return reduceTuples(finalList)
        

def reduceTuples(tuples):
    finalList = []
    newTup =''
    for tup in tuples:
        if len(tup) > 1:
            for i in range(0,len(tup[0])):
                if tup[0][i] != tup[1][i]:
                    newTup = newTup + '-'
                else:
                    newTup = newTup + tup[0][i]
            finalList.append(newTup)
        else:
            finalList.append(tup[0])
        newTup = ''
    return finalList
            
        
def create2dArray(reduced, trueValues):
    matrix = [['0000' for x in range(len(trueValues) + 1)] for y in range(len(reduced) + 1)]
    j = 0
    matrix
    for row in matrix:
        if j > 0:
            row[0] = reduced[j-1]
        j = j + 1
    trueValues = ['0000'] + trueValues    
    matrix[0] = trueValues
    return matrix
    
    
    
def binToVars(tokens, varss):
    finalList = []
    newVar = ''
    for token in tokens:
        for i in range(0, len(varss)):
            if token[i] == '1':
                if newVar == '':
                    newVar =varss[i]
                else:
                    newVar = newVar + '*' + varss[i]
            elif token[i] == '0':
                if newVar =='':
                    newVar = '~' + varss[i]
                else:
                    newVar = newVar + '*~' + varss[i]
        finalList.append(newVar)
        newVar = ''
    return finalList


def final(matrix):
    isRight = True
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if i > 0 and j > 0:
                for k in range(0, len(matrix[0][1])):
                    if not (matrix[i][0][k] == matrix[0][j][k] or matrix[i][0][k] == '-' or 
                            matrix[0][j][k] == '-'):
                        isRight = False
                if isRight:
                    matrix[i][j] =' x  '
                isRight = True
    return findMinimum(matrix)
          
def findMinimum(matrix):
    #print(matrix)
    isIncluded = len(matrix[0]) * [False]
    isIncluded[0] = True
    others = []
    finalList = []
    listOfOnly = len(matrix[0]) * [-1]
    for j in range(1, len(matrix[0])):
        for i in range (1, len(matrix)):
            if matrix[i][j] == ' x  ':
                if listOfOnly[j] == -1:
                    listOfOnly[j] = i
                else:
                    listOfOnly[j] = -2
    for j in range(1, len(listOfOnly)):
        if listOfOnly[j] > -1:
            finalList.append(matrix[listOfOnly[j]][0])
            for k in range(1, len(listOfOnly)):
                if matrix[listOfOnly[j]][k] == ' x  ':
                    isIncluded[k] = True
    finalList = list(set(finalList))
    #print(finalList)
    if isWholeListTrue(isIncluded):
        return finalList
    for j in range(1, len(matrix)):
        if not matrix[j][0] in finalList:
            others.append(j)
    for j in range(1, len(others)):
        for combination in itertools.combinations(others, j):
            copiedIsIncluded = list(isIncluded)
            #print("New ->>", copiedIsIncluded)
            copiedFinalList = list(finalList)
            for each in combination:
                copiedFinalList.append(matrix[each][0])
                for k in range(1, len(isIncluded)):
                    if matrix[each][k] == ' x  ':
                        copiedIsIncluded[k] = True
            #print(combination)
            #print(matrix[combination[0]][0])
            #print(copiedIsIncluded)
            if isWholeListTrue(copiedIsIncluded):
                return copiedFinalList
            
            
def isWholeListTrue(myList):
    for el in myList:
            if el == False:
                return False
    return True
                    
          
                        
def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print (matrix[i][j])
        print('')
                            


def main(expr):
    tokens = stringToTokens(expr)
    onp = withoutSpaces(onpexpr(tokens))
    varss = listOfVars(tokens)
    tabOfCases = createTab(len(varss))
    listOfTrue = checkWhenTrue(onp,tabOfCases,varss)
    #print(listOfTrue)
    if listOfTrue == ['-2']: print(0)
    elif listOfTrue == ['-1']: print(1)
    else:
        listOfTrue =  [bin(x)[2:].zfill(len(varss)) for x in listOfTrue]
        listOfTrue = sorted(listOfTrue, key = lambda x: x.count('0'), reverse = True)
        #print(listOfTrue)
        tuples = sorted(list(set(makeTuples(listOfTrue,1))))
        newTuples = sorted(list(set(makeTuples(tuples,1))))
    
        while newTuples != tuples:
            tuples = sorted(list(newTuples))
            newTuples = sorted(list(set(makeTuples(tuples,1))))
        #print(tuples)
        #print(tuples)
        #tuples = list(set(makeTuples(tuples,1)))
        tuples = sorted(tuples, key = lambda x: x.count('-'), reverse = True)
        matrix = create2dArray(tuples, listOfTrue)
        #print(matrix)
        newMatrix = final(matrix)
        #print(newMatrix)
        finalVars = binToVars(newMatrix,varss)
        finalString = finalVars[0]
        for i in range(1, len(newMatrix)):
            finalString = finalString + " + " +finalVars[i]
            
        print(finalString)