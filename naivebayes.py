
def main():
    f = open("heart.csv",'r') #open our file
    tmp = f.read().split("\n") #split it up by newline
    del tmp[len(tmp)-1]
    del tmp[0]
    
    for i in range(len(tmp)):
        tmp[i] = tmp[i].split(",")
    X = []
    for element in tmp:
        X.append(element)
    continuousList = [0,3,4,7,9] #all of the indices of columns in our particular dataset which are continuous
    trainListPortion = []
    for i in range(1,139): #take a chunk of the data and use it as training
        trainListPortion.append(X[i])
    for i in range(166,277):
        trainListPortion.append(X[i])
    
    cnt = 0
    cnt2 = 0
    for i in range(278,303): #the following data is used for testing
        cnt = cnt + 1
        if NaiveBayes(trainListPortion,X[i][:-1],continuousList) == 0:
            cnt2 = cnt2 + 1
    print(str(100 * (cnt2/cnt)) + "% " + str(cnt2) + " / " + str(cnt))
    
    cnt = 0
    cnt2 = 0
    for i in range(140,165):
        cnt = cnt + 1
        if NaiveBayes(trainListPortion,X[i][:-1],continuousList) == 1:
            cnt2 = cnt2 + 1
    print(str(100 * (cnt2/cnt)) + "% " + str(cnt2) + " / " + str(cnt))
    

#NaiveBayes implementation that can be reused for other things
def NaiveBayes(train,test,continuous=[]):
    lst = [x for x in range(len(test)) if (not x in continuous)] #the indices of categorical data
    lst2 = [x for x in range(len(test)) if (x in continuous)] #the indices of continuous data
    positives = [] #holds the positives (where the last column is 1)
    negatives = [] #holds the negatives (where the last column is 0)
    for i in train:
        if int(i[len(i)-1]) == 1:
            positives.append(i) #if the entry in training set is positive (==1) add it to positives
        else:
            negatives.append(i)

    posCount = []
    negCount = []
    
    for i in lst:
        posCount.append(0)
        negCount.append(0)
        #Here we go through each element and compare the test data to our output
        #If it matches then we consider that correct and we calculate our error
        #based on that
        for element in positives:
            if int(element[i]) == int(test[i]):
                posCount[len(posCount)-1] = posCount[len(posCount)-1] + 1
        for element in negatives:
            if int(element[i]) == int(test[i]):
                negCount[len(negCount)-1] = negCount[len(negCount)-1] + 1
    
    #ratio of items that were correct vs incorrect
    positiveRatio = len(positives)/len(train)
    for i in posCount:
        positiveRatio = positiveRatio * (i/len(positives))
    negativeRatio = len(negatives)/len(train)
    for i in negCount:
        negativeRatio = negativeRatio * (i/len(negatives))
    
    
    #continuous
    for i in lst2:
        count = 0.0
        for element in positives:
            count = count + float(element[i])
        mean = count / len(positives)
        #Calculate the mean, add up all of the elements and divide by length
            
        variance = 0
        for element in positives:
            variance = variance + (float(element[i]) - mean)**2
        variance = abs(variance / (mean-1))
        #Calculate variance, refer to formula
        answer = ( 1 / ((2*3.1415926*variance)**0.5) ) * 2.7182818**(-1*((float(test[i])-mean)**2)/(2*variance))
        #Calculate overall answer in order to find if its positive/negative
        positiveRatio = positiveRatio * answer
        
        count = 0
        for element in negatives:
            count = count + float(element[i])
        mean = count / len(negatives)
            
        variance = 0
        for element in negatives:
            variance = variance + (float(element[i]) - mean)**2
        variance = variance / (mean-1)
        answer = ( 1 / ((2*3.1415926*variance)**0.5) ) * 2.7182818**(-1*((float(test[i])-mean)**2)/(2*variance))
        
        negativeRatio = negativeRatio * answer
        
    if positiveRatio > negativeRatio:
        return 1
    else:
        return 0

main()

