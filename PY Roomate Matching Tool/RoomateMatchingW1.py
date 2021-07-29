import json, time, re, excel2json, os
from typing import Dict
from hungarian_algorithm import algorithm
from alive_progress import alive_bar
from datetime import datetime
class Values:
    version = "0.9.1"
    debug = True                                    #Debug off == user-mode, Debug on debug
    missingParticipant = False                      #Is there a missing participant
    excelName = "Test.xls"                          #Settings for debug 1
    jsonName  = "Form Responses.json"               #Settings for debug 2
    questionOffsets = {"Group" : 0, "Slovak" : 1, "Name ID" : 2, "Q1" : 3, "Q2Q3" : [4,5], "Q4" : 6, "Q5Q6" : [7,8], "Q7Q8": [9,10], "Q9Q10" : [11,12], "Q11Q12" : [13,14], "Q13Q14" : [15,16]}
    allOptionsList = []                             #Loading all the questions 
    startTime = 0                                   #Start time of the operation 
    endTime   = 0                                   #End time of the operation
    group1 = []                                     #Group 1 list
    group2 = []                                     #Group 2 list
    cacheList = []                                  #For caching
    internationalSt = False                         #For international students -- If True than then they can be in 1 room -- If False they cant be in 1 room
sett = Values()                                     #Creating a global object

def makeLog(typeOfLog = "LOG", where = "", stringToPass = "NULL", sprint = False):
    """
    Making logs into the new logging file.
    1. Arg - ['LOG' - Log, 'ERR' - ERROR, 'FERR' - FATAL ERROR exits, 'CLR' - Clears the whole file] -- If none then "LOG"
    2. Arg - String/Int more specification, function-- etc.. -- If none then ""
    3. Arg - String/Int that should be passed into the log! -- If none then "NULL"
    4. Arg - Should it be printed in the console? -- If none then "False"
    """
    if typeOfLog == "LOG":
        newString = f"[LOG - {where}] {stringToPass} \n"
    elif typeOfLog == "ERR":
        newString = f"[ERROR - {where}] {stringToPass} \n"
    elif typeOfLog == "FERR":
        newString = f"[FATAL ERROR - {where}] {stringToPass} \n"
    elif typeOfLog == "CLR":
        newString = ""
        file = open("rmLog.txt", "w")
        file.write(newString)
        file.close()
    else:
        newString = f"{'[ERROR] - '} makeLog(), arg1 '{typeOfLog}' is invalid! \n"
    if sprint:
        print(f"\n{newString}\n")
    file = open("rmLog.txt", "a")
    file.write(newString)
    file.close()
    if typeOfLog == "FERR":
        path = os.getcwd() + r"\rmLog.txt"
        print(f"Check rmLog.txt for more information! It can be found here {path}!")
        print("\n\n")
        input("Press enter to exit!")
        exit(0)
    return True

                                                    #Intial input, --IF DEBUG TRUE DISABLED-- .xls, .json file input
if sett.debug == True:
    excel2json.convert_from_file(str(sett.excelName))
else:
    localCounter = 0
    while True:
        try:
            localCounter += 1
            if  localCounter == 1:                                                                     #Enter the .xls file
                print("What is the name of the of the file? eg. prefs_table.xls")
                sett.excelName = input()
                excel2json.convert_from_file(str(sett.excelName))
        
        except NameError:                                                                              #File not found, try one more time
            makeLog("ERR", "XLS file converter","File not found!", True)
            print("What is the name of the of the file? eg. prefs_table.xls")
            sett.excelName = input()
            excel2json.convert_from_file(str(sett.excelName))
    
        #Input the name of the second JSON file -- Wait and check your folder you should see new JSON files
        print("Check your folder and pick the JSON file you want to use. eg. Form Responses.json")
        sett.jsonName = input()
        try:
            json.loads(open(str(sett.jsonName)).read())
            break
        except FileNotFoundError:
            makeLog("ERR", "JSON file selector", "File not found!", True)

#Converts time -- for the stopwatch
def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Results calculated, it took {0}h:{1}m:{2}s to calculate!".format(int(hours),int(mins),round(int(sec))))
#Handling of the questions -- All the questions are returned in a list
def getAllList():
    res = json.loads(open(str(sett.jsonName)).read())
    list = []
    #Add a log event
    if res[1].keys() == res[2].keys():
        for key in res[0].keys():
            list.append(key)
    return list

#Loading all the quesitons
sett.allOptionsList = getAllList()


#Searches in the JSON file -- Name of the attribute and the number of the block where it is located (starts with zero)
def lookForData(jClass, numberWhere):
    jdata = json.loads(open(str(sett.jsonName)).read())
    try:
        return jdata[numberWhere][jClass]
    except KeyError:
        makeLog("LOG", f"lookForData({jClass},{numberWhere})", "Data not found!")
        return False

#Returns the number of the participants(int), !!!starts with a 1
def numberOfParticipants():
    nOfparticipants = 0
    while True:
        try:
            lookForData("Name ID", nOfparticipants)
        except IndexError:
            break
        nOfparticipants += 1
    return nOfparticipants


#Returns all the data that a participant has, !!!starts with a zero
def dataForParticipant(number):
    jdata = json.loads(open(sett.jsonName).read())
    data = []
    for i in range(0,len(getAllList())):
        data.append(jdata[number][sett.allOptionsList[i]])
    return data
#---------------------------------------------------------------------------------------------------------
#Q1 - Window - Doulbe points - Two integers needed
def categoryOne(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[sett.questionOffsets["Q1"]] - otherP[sett.questionOffsets["Q1"]]
    return abs(minus) * 2

#Q2,Q3 - Speaker music + Playing music, two integers -- Special case
def categoryTwoThree(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[sett.questionOffsets["Q2Q3"][1]]
    otherPq5 = 6 - otherP[sett.questionOffsets["Q2Q3"][1]]
    calc1 = mainP[sett.questionOffsets["Q2Q3"][0]] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[sett.questionOffsets["Q2Q3"][0]]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2

#Q4 - Cleanliness orderliness - double, two ints needed 
def categoryFour(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[sett.questionOffsets["Q4"]] - otherP[sett.questionOffsets["Q4"]]
    return abs(minus) * 2

#Q5,Q6 - Sharing of items, reversed special, two ints needed 
def categoryFiveSix(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[sett.questionOffsets["Q5Q6"][1]]
    otherPq5 = 6 - otherP[sett.questionOffsets["Q5Q6"][1]]
    calc1 = mainP[sett.questionOffsets["Q5Q6"][0]] - otherPq5
    calc2 = mainPq5 - otherP[sett.questionOffsets["Q5Q6"][0]]
    return abs(calc1) + abs(calc2)

#Q7,Q8 - Quiet space, reversed special, two ints neeeded 
def categorySevenEight(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[sett.questionOffsets["Q7Q8"][1]]
    otherPq5 = 6 - otherP[sett.questionOffsets["Q7Q8"][1]]
    calc1 = mainP[sett.questionOffsets["Q7Q8"][0]] - otherPq5
    calc2 = mainPq5 - otherP[sett.questionOffsets["Q7Q8"][0]]

    return abs(calc1) + abs(calc2)

#Q9,Q10 - Friends over, specia but not reversed, two ints are needed  
def categoryNineTen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[sett.questionOffsets["Q9Q10"][1]]
    otherPq5 = otherP[sett.questionOffsets["Q9Q10"][1]]
    calc1 = mainP[sett.questionOffsets["Q9Q10"][0]] - otherPq5
    calc2 = mainPq5 - otherP[sett.questionOffsets["Q9Q10"][0]]
    return abs(calc1) + abs(calc2)

#Q11,Q12 - Living space, special but not reversed, two ints needed 
def categoryElevenTwelve(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[sett.questionOffsets["Q11Q12"][1]]
    otherPq5 = otherP [sett.questionOffsets["Q11Q12"][1]]
    calc1 = mainP[sett.questionOffsets["Q11Q12"][0]] - otherPq5
    calc2 = mainPq5 - otherP[sett.questionOffsets["Q11Q12"][0]]
    return abs(calc1) + abs(calc2)

#Q13,Q14 - Sleeping, special alogorithm
def categoryThirteenFourteen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    #first person
    sleepF1 = mainP[sett.questionOffsets["Q13Q14"][0]] - otherP[sett.questionOffsets["Q13Q14"][0]]
    wakeF1 = mainP[sett.questionOffsets["Q13Q14"][1]] - otherP[sett.questionOffsets["Q13Q14"][1]]
    #second person
    sleepF2 = otherP[sett.questionOffsets["Q13Q14"][0]] - mainP[sett.questionOffsets["Q13Q14"][0]]
    wakeF2 = otherP[sett.questionOffsets["Q13Q14"][1]] - mainP[sett.questionOffsets["Q13Q14"][1]]
    #Person one sleep
    if sleepF1 < 0:
        person1s = (-sleepF1 + 1)/(6-mainP[14])/(5/4)
    else:
        person1s = 0
    #Person two sleep
    if sleepF2 < 0:
        person2s = (-sleepF2 + 1)/(6-otherP[14])/(5/4)
    else:
        person2s = 0
    #Person one wake
    if wakeF1 > 0:
        person1w = (wakeF1 + 1)/(6-mainP[14])/(5/4)
    else:
        person1w = 0
    #Person two wake
    if wakeF2 > 0:
        person2w = (wakeF2 + 1)/(6-otherP[14])/(5/4)
    else:
        person2w = 0
    return (person1w + person2w + person1s + person2s) * 2

#---------------------------------------------------------------------------------------------------------

#Execution two ints -- represeting members (Member ID - 1)
def allCategories(mem1, mem2):
    together = categoryOne(mem1,mem2) + categoryTwoThree(mem1,mem2) + categoryFour(mem1,mem2) + categoryFiveSix(mem1,mem2) + categorySevenEight(mem1,mem2) +categoryNineTen(mem1,mem2) + categoryElevenTwelve(mem1,mem2) + categoryThirteenFourteen(mem1,mem2)
    firstp =  dataForParticipant(mem1)
    secondp = dataForParticipant(mem2)
    if sett.internationalSt == False and firstp[1] == "N" and secondp[1] == "N":
        together += 10000
    return together*together


#Edits the output, adds1 to the number so it alligns with the User ID
def outputEditor(output):
    outcome1 = re.findall("\d+", output)
    outcome2 = [int(i) for i in outcome1]
    for a in range(2,len(outcome2),3):
        outcome2[a] -= 1
    for a in range(0,len(outcome2)):
        outcome2[a] += 1
    return outcome2

#Last phase of generating the input for the algortihm -- Only used with the uneven number of members
def groupDic(group1Listt, group2Listt):
    namesDict = {}
    storingDic = {}
    for lists11 in range(len(group1Listt)):
            for listss in range(len(group2Listt)):
                exe = allCategories(group1Listt[lists11], group2Listt[listss])
                storingDic.update({group2Listt[listss] : int(exe)})
                if listss == (len(group1Listt) - 1):
                    namesDict.update({group1Listt[lists11] : storingDic})
                    namesDict.update({group1Listt[lists11] : storingDic})
                    storingDic = {}
    return namesDict
#From list1 to list2 -- List1, List2, indexNumber -- Mostly used in the uneven uneven algorithm
def moveElements(list1, list2, listNumber1): 
    list11 = list1.copy()
    list22 = list2.copy()
    value = list11[listNumber1]
    list22.append(list11[listNumber1])
    list11.pop(listNumber1)
    return [list11,list22,value]
#Used for unven groups, difference bettween members needs to be 1
def unevenGroups1(group1List, group2List, returnDict):  #Input -- False -- Returns the smallest sum -- True -- returns the dictionary
    if abs(len(group1List) - len(group2List)) != 1:
        makeLog("FERR", "unevenGroups1()", "Difference bettween the number of participants is not 1!", True)
        return False
    if len(group1List) - len(group2List) == 1: #In this case the dominant group is g1
        dominantGroup = 0
    else:                                      #Dominant group g2
        dominantGroup = 1
    #
    generatedValues = []
    sumAll = 0                 #Used in the loop
    testGroup = group1List     #Loadin buffer values
    bestGroup = group1List     #Loading bvuffer values
    #
    if dominantGroup == 1:                 #In case that the dominant group is g2 
        #Switching the groups
        buffer = group1List                # - = g1
        group1List = group2List            #g1 = g2
        group2List = buffer                #g2 = g1
        #Loading the new group 1
        testGroup = group1List
        bestGroup = group1List
    #Comparing one list to another, special algorithm
    for listMain in range(len(group1List)): #Generating the values for this group
        generatedValues.append(sumAll)      #Appends all the sums to a list
        testGroup = []                      #Creating a list
        testGroup.extend(group1List)        #Resets the value
        testGroup.pop(listMain)             #Deletes one object from LIST
        sumAll = 0
        for lists1 in range(len(group2List)):
            for lists in range(len(group2List)):
                exe = allCategories(testGroup[lists1], group2List[lists])
                sumAll += exe
    generatedValues.pop(0)                        #removes the first 0 from the list
        #
    checker = 10000000
    checker_value = 0
        #
    for check in range(len(generatedValues)):      #Searches for the smallest sum in the whole LIST
        if checker > generatedValues[check]:       #If a sum is smaller than checker then it gets into checker
            checker = generatedValues[check]
            checker_value = check
        #
    if returnDict == True:                                  #If we want the dict returned 
        sett.missingParticipant = bestGroup[checker_value]  #Saves the User ID to the class
        bestGroup.pop(checker_value)                        #Removes the member
        finalR = groupDic(bestGroup, group2List)            #Creates a Dict
        if sett.debug == True: print(finalR)
        return finalR
    return checker     

def sumOfArrays(array1, array2): #Input two arrays
    if len(array1) != len(array2): makeLog("FERR", "sumOfArrays", "Len Array1 and Len Array2 not matching", True)
    sumAll = 0
    for lists1 in range(len(array1)):
        for lists in range(len(array2)):
            exe = allCategories(array1[lists1], array2[lists])
            sumAll += exe
    return sumAll
#Cahing 
def cacheSetter(numericalCombination, value):          #The first is the number from for loops, second number is the value
    sortedCombination = "".join(sorted(str(numericalCombination)))
    if sortedCombination in sett.cacheList:
        return False
    sett.cacheList.append(sortedCombination)
    sett.cacheList.append(value)
    return True
def cacheGetter(numericalCombination):                                     #The first is the number from for loops
    sortedCombination = "".join(sorted(str(numericalCombination)))
    if sortedCombination in sett.cacheList:
        index = sett.cacheList.index(sortedCombination)
        return sett.cacheList[index + 1]                                    #Returns the value
    return False

#Cahing 
                                       #In case that we only want the smallest sum returned
def unUnD1e(list1, list2, diff): #list, list,  - int, int 
    #
    testList1 = list1.copy()  #Resaving values
    testList2 = list2.copy()  #Resaving values
    testlist1n = list1.copy()
    testlist2n = list2.copy()
    #
    usedList = []
    saveValue = 1000000000000
    if diff == 1:                       #Case where the difference is 2, 1 member needs to be moved
        if sett.debug == True: print("[DBG - unUnD1e] The difference is 2, using 'diff == 1'")
        with alive_bar(len(list1)) as bar:
            for mem1 in range(len(list1)):       #Making the pairs and calculating the sums
                bar()
                listSave = testList1[mem1]
                rtrn = moveElements(testList1,testList2,mem1)
                if cacheGetter(str(listSave) + str(mem1)) == False:                      #Not found un cache 
                    outcome = sumOfArrays(rtrn[0], rtrn[1])
                    cacheSetter(str(listSave) + str(mem1), outcome)
                if cacheGetter(str(listSave) + str(mem1)) == True:
                    outcome = cacheGetter(str(listSave) + str(mem1))
                if outcome < saveValue:          #Saving the best sum and data about it 
                    saveValue = outcome
                    itNubmer = mem1
        #Now editing the output
        rtrn = moveElements(testList1,testList2,itNubmer)
        if sett.debug == True: print("[DBG - unUnD1e] Difference 2!")
        return [rtrn[0],rtrn[1],saveValue]
    #
    if diff == 2:                     #Case where the difference is 4, 2 members needs to be moved
        if sett.debug == True: print("[DBG - unUnD1e] The difference is 4, using 'diff == 2'")
        #15 mins
        with alive_bar(len(list1)*len(list1)) as bar:
            for mem1 in range(len(list1)):
                for mem2 in range(len(list1)):
                    bar()
                    if mem1 == mem2:      #Checks if the numbers are equal
                        continue
                    if sorted(str(mem1) + str(mem2)) in usedList:                                       #Optimization
                        continue
                    usedList.append(sorted(str(mem1) + str(mem2)))
                    listNo = [mem1,mem2]
                    listName = [testlist1n[mem1], testlist1n[mem2]]
                    testlist2n.append(testlist1n[mem1])
                    testlist2n.append(testlist1n[mem2])
                    testlist1n.remove(listName[0])
                    testlist1n.remove(listName[1])
                    #
                    if cacheGetter(str(listName[0]) + str(listName[1]) + str(mem1) + str(mem2)) == False:                      #Not found in cache 
                        outcome = sumOfArrays(testlist1n, testlist1n)
                        cacheSetter(str(listName[0]) + str(listName[1]) + str(mem1) + str(mem2), outcome)
                    #
                    if cacheGetter(str(listName[0]) + str(listName[1]) + str(mem1) + str(mem2)) != False:
                        outcome = cacheGetter(str(listName[0]) + str(listName[1]) + str(mem1) + str(mem2))                     #Found in cache
                    #
                    testlist1n = list1.copy()
                    testlist2n = list2.copy()
                    if outcome < saveValue:          #Saving the best sum and data about it
                        saveValue = outcome
                        itNubmer = listNo
                        name = listName
        testlist2n.append(testlist1n[itNubmer[0]])
        testlist2n.append(testlist1n[itNubmer[1]])
        testlist1n.remove(name[0])
        testlist1n.remove(name[1])
        if sett.debug == True: print("[DBG - unUnD1e] The lowest sum was {}".format(saveValue))
        return [testlist1n,testlist2n,saveValue]
    #
    if diff == 3:
        if sett.debug == True: print("[DBG - unUnD1e] The difference is 6, using 'diff == 3'")
        with alive_bar(len(list1)*len(list1)*len(list1)) as bar:
            for mem1 in range(len(list1)):
                for mem2 in range(len(list1)):
                    for mem3 in range(len(list1)):
                        bar()
                        if mem1 in [mem2,mem3] or mem2 in [mem1,mem3] or mem3 in [mem1,mem2] :     #Optimization
                            continue
                        if sorted(str(mem1) + str(mem2) + str(mem3)) in usedList:                                       #Optimization
                            continue
                        usedList.append(sorted(str(mem1) + str(mem2) + str(mem3)))
                        listNo = [mem1,mem2,mem3]
                        listName = [testlist1n[mem1], testlist1n[mem2], testlist1n[mem3]]
                        testlist2n.append(testlist1n[mem1])
                        testlist2n.append(testlist1n[mem2])
                        testlist2n.append(testlist1n[mem3])
                        testlist1n.remove(listName[0])
                        testlist1n.remove(listName[1])
                        testlist1n.remove(listName[2])
                        #
                        if cacheGetter(str(listName[0]) + str(listName[1]) + str(listName[2]) + str(mem1) + str(mem2) + str(mem3)) == False:
                            outcome = sumOfArrays(testlist1n, testlist1n)
                            cacheSetter(str(listName[0]) + str(listName[1]) + str(listName[2]) + str(mem1) + str(mem2) + str(mem3), outcome)
                        #
                        if cacheGetter(str(listName[0]) + str(listName[1]) + str(listName[2]) + str(mem1) + str(mem2) + str(mem3)) != False:
                            outcome = cacheGetter(str(listName[0]) + str(listName[1]) + str(listName[2]) + str(mem1) + str(mem2) + str(mem3))
                        #
                        testlist1n = list1.copy()
                        testlist2n = list2.copy()
                        if outcome < saveValue:          #Saving the best sum and data about it 
                            saveValue = outcome
                            itNubmer = listNo
                            name = listName
        testlist2n.append(testlist1n[itNubmer[0]])
        testlist2n.append(testlist1n[itNubmer[1]])
        testlist2n.append(testlist1n[itNubmer[2]])
        testlist1n.remove(name[0])
        testlist1n.remove(name[1])
        testlist1n.remove(name[2])
        if sett.debug == True: print("[DBG - unUnD1e] The lowest sum was {}".format(saveValue))
        return [testlist1n,testlist2n,saveValue]
    #
    if diff == 4:
        if sett.debug == True: print("[DBG - unUnD1e] The difference is 8, using 'diff == 4'")
        with alive_bar(len(list1)*len(list1)*len(list1)*len(list1)) as bar:
            for mem1 in range(len(list1)):
                for mem2 in range(len(list1)):
                    for mem3 in range(len(list1)):
                        for mem4 in range(len(list1)):
                            bar()
                            if mem1 in [mem2,mem3,mem4] or mem2 in [mem1,mem3,mem4] or mem3 in [mem1,mem2,mem4] or mem4 in [mem1,mem2,mem3]: #Optimization
                                continue
                            if sorted((str(mem1) + str(mem2) + str(mem3) + str(mem4))) in usedList:                                       #Optimization
                                continue
                            usedList.append(sorted(str((str(mem1) + str(mem2) + str(mem3) + str(mem4)))))               #Optimization
                            listNo = [mem1,mem2,mem3,mem4]
                            listName = [testlist1n[mem1], testlist1n[mem2], testlist1n[mem3], testlist1n[mem4]]
                            testlist2n.append(testlist1n[mem1])
                            testlist2n.append(testlist1n[mem2])
                            testlist2n.append(testlist1n[mem3])
                            testlist2n.append(testlist1n[mem4])
                            testlist1n.remove(listName[0])
                            testlist1n.remove(listName[1])
                            testlist1n.remove(listName[2])
                            testlist1n.remove(listName[3])
                            if cacheGetter(str(listName[0]) + str(listName[1]) + str(listName[2]) + str(listName[3]) + str(mem1) + str(mem2) + str(mem3) + str(mem4)) == False:
                                outcome = sumOfArrays(testlist1n, testlist1n)
                                cacheSetter(str(listName[0]) + str(listName[1]) + str(listName[2]) + str(listName[3]) + str(mem1) + str(mem2) + str(mem3) + str(mem4), outcome)
                            if cacheGetter(str(listName[0]) + str(listName[1]) + str(listName[2]) + str(listName[3]) + str(mem1) + str(mem2) + str(mem3) + str(mem4)) != False:
                                outcome = cacheGetter(str(listName[0]) + str(listName[1]) + str(listName[2]) + str(listName[3]) + str(mem1) + str(mem2) + str(mem3) + str(mem4))
                            testlist1n = list1.copy()
                            testlist2n = list2.copy()
                            if outcome < saveValue:          #Saving the best sum and data about it 
                                saveValue = outcome
                                itNubmer = listNo
                                name = listName
        testlist2n.append(testlist1n[itNubmer[0]])
        testlist2n.append(testlist1n[itNubmer[1]])
        testlist2n.append(testlist1n[itNubmer[2]])
        testlist2n.append(testlist1n[itNubmer[3]])
        testlist1n.remove(name[0])
        testlist1n.remove(name[1])
        testlist1n.remove(name[2])
        testlist1n.remove(name[3])
        if sett.debug == True: print("[DBG - unUnD1e] The lowest sum was {}".format(saveValue))
        if diff > 4:
            print("Difference bigger than 8, currently not supported!")
            time.sleep(15)
            exit()
        return [testlist1n,testlist2n,saveValue]
#Algorithm for groups where the difference is bigger than 1
def unevenUnevenAlgo(list1,list2):
    if (len(list1) - len(list2)) > 0:          #Dominant group1(List1)
        difference = (len(list1) - len(list2)) #Difference 

    else:                                      #Dominant group2(List2)
        difference = (len(list2) - len(list1)) #Difference 
        buffer = list1
        list1 = list2
        list2 = buffer

    if difference % 2 == 0:                    #1st case -- difference mod 2 is 0
        difference = difference / 2            #1/2 of the dif
        case = unUnD1e(list1,list2,difference)
        list1 = case[0]
        list2 = case[1]
    else:                                      #ODD numbers
        print("[SYS] - Which option do you want to use:")         #Checks if the input is valid
        print("[SYS] - 1. Faster algorithm but less accurate?")
        print("[SYS] - 2. Slower algorithm but more accurate?")
        while True:
            uInput = input("Your input(1,2): ")
            uInput = int(uInput)
            if uInput == 1 or uInput == 2:
                break
            print("[ERROR] Invalid input! Only options are 1 or 2! \n\n")
            makeLog("LOG", "unevenUnevenAlgo - Algo selection", "Bad user input!")
        #
        makeLog("LOG", "Faster/Slower algorithm", f"Input: {uInput}")
        print()
        print()
        if uInput == 2:
            saveValue = 10000000
            if sett.debug == True: print("[DBG - unUnD1e] Continuing with the slower algortihm!")
            print("[SYS] - This process will be repeated a few times!")
            for dif in range(len(list1)):
                clist1 = list1.copy()
                clist2 = list2.copy()
                missMem = clist1[dif]
                clist1.pop(dif)
                case = unUnD1e(clist1,clist2,difference-1)
                if case[2] < saveValue:
                    saveValue = case[2]
                    bestClist1 = case[0]
                    bestClist2 = case[1]
                    cmissedMem =  missMem
            bestClist1.append(cmissedMem)
            return unevenGroups1(bestClist1,bestClist2, True)
        if uInput == 1:
            if sett.debug == True: print("[DBG - unUnD1e] Continuing with the faster algortihm!")
            clist1 = list1.copy()
            clist2 = list2.copy()
            buffer = clist1[0]
            clist1.pop(0)
            case = unUnD1e(clist1,clist2,difference-1)
            clist1 = case[0]
            clist1.append(buffer)
            clist2 = case[1]
            return unevenGroups1(clist1,clist2, True)
    if sett.debug == True: 
        print()
        print("[DEBUG - unevenUnevenAlgo] List 1: {} len({}), List 2: {} len({})".format(list1,len(list1),list2,len(list2)))
        print()
    return [list1,list2]
#Plain dict creaton for the even algorithm
def evenAlgo(group1List, group2List): 
    namesDict = {}
    storingDic = {}
    for lists1 in range(len(group1List)):
        for lists in range(len(group1List)):
            exe = allCategories(group1List[lists1], group2List[lists])
            storingDic.update({group2List[lists] : int(exe)})
            if lists == (len(group1List) - 1):
                namesDict.update({group1List[lists1] : storingDic})
                storingDic = {}
    if sett.debug==True: print(namesDict)
    return namesDict                 #Returns dict

#Making the groups of people, inputs two strings (Names of the groups)
def groupMaker(group1, group2):
    group1List = []
    group2List = []
    for group in range(numberOfParticipants()):
        if lookForData("Group", group) == group1:
            group1List.append(int(lookForData("Name ID", group) - 1))
        elif lookForData("Group", group) == group2:
            group2List.append(int(lookForData("Name ID", group) - 1))
    #
    if len(group1List) == 0 or len(group2List) == 0:
        makeLog("FERR", "groupMaker", f"One of the groups has 0 participants, G1: {len(group1List)}, G2: {len(group2List)}", True)
    if abs(len(group1List) - len(group2List)) == 1:   #Calls the function for uneven numbers with difference 1
        return unevenGroups1(group1List,group2List,True)
    #
    elif len(group1List) == len(group2List):          #Creating the dict -- Number of participants is even
        return evenAlgo(group1List, group2List)
    #
    elif abs(len(group1List) - len(group2List)) > 1:    #More people are uneven
        rtrn = unevenUnevenAlgo(group1List,group2List)  #Returns the edited lists that are even or uneven
        if type(rtrn) is dict:                          #If it is a ready to go dictionary
            return rtrn
        if len(rtrn[0]) == len(rtrn[1]):                #If it is a list that needs to be converted into a dict          
            return evenAlgo(rtrn[0], rtrn[1])
    else:
        makeLog("FERR", "groupMaker()", "Unknown", True)

    
#Final output system, edits the output and puts it into groups, input should be the output from the algorithm
def finalOut(outcome):
    if sett.debug == True: 
        print()
        print("[DEBUG - finalOut] The output of the algorithm is: {}".format(outcome))
        print()
    print()
    time_convert(sett.endTime - sett.startTime)                                             #Prints out the time it took
    print()
    print("Numbers are matching with the Name IDs!!")
    f = open("roommates.txt","w")
    d = datetime.now().strftime("%d/%B/%Y - %H:%M:%S")
    outputSupervisor = []
    trigger = False
    f.write(f"[{d}] \n")
    for a in range(len(outcome)):                                                           #Prints out by rooms
        out = outputEditor(str(outcome[a]))
        print("Room {}: {}, {} with a pair-value {}".format(a+1, out[0], out[1], out[2]))
        if out[0] in outputSupervisor or out[1] in outputSupervisor:
            trigger = True
        outputSupervisor.append(out[0])
        outputSupervisor.append(out[1])
        f.write("Room {}: {}, {} with a pair-value {} \n".format(a+1, out[0], out[1], out[2]))
    if sett.missingParticipant != False:
        print("Room {}: {}, - alone".format(a+2, sett.missingParticipant+1))
        f.write("Room {}: {}, - alone \n".format(a+2, sett.missingParticipant+1))
        if sett.missingParticipant+1 in outputSupervisor:
            trigger = True
    print()
    path = os.getcwd() + r"\roommates.txt"
    makeLog("LOG", "finalOut", f"File roommates.txt was created! It can be found here: {path}", True)
    f.close()
    if trigger:
        makeLog("FERR", "Output", "One participant detected in multiple rooms", True)

#Prints out some basic data

def announceData():
    print("\nVersion: {} \n".format(sett.version))
    print("Number of registered participants: {}".format(numberOfParticipants()))
    print("Number of registered questions: {} \n".format(len(getAllList())))
    makeLog("LOG", "STARTUP", f"Version: {sett.version}")
    makeLog("LOG", "STARTUP", f"Debug: {sett.debug}")
    makeLog("LOG", "STARTUP", f"Number of registered participants: {numberOfParticipants()}")
    makeLog("LOG", "STARTUP", f"Number of registered questions: {len(getAllList())}")

def internationalStudents():
    while True:
        print()
        print("Can one room be composed of 2 international students? [y/n]")
        a = input()
        if a == "y" or a == "Y":
            sett.internationalSt = True
            makeLog("LOG", "internationalStudents()", "sett.internationalSt = True")
            return
        if a == "n" or a == "N": 
            sett.internationalSt = False
            makeLog("LOG", "internationalStudents()", "sett.internationalSt = False")
            return
        makeLog("ERR", "internationalStudents()", "Invalid input!", True)
#Announces data
def checkGroups():
    pass
def runtime():
    makeLog("CLR") #Clears the LOG file
    announceData()
    #Input group
    print("Which groups should be used! eg. F3, F4")
    fg = input("Group one: ")
    sg = input("Group two: ")
    makeLog("LOG", "input Groups",f"Group 1: {fg}, Second Group: {sg}")
    internationalStudents()
    sett.startTime = time.time()                                                                 #Start of stopwatch
    group1 = groupMaker(fg, sg)                                                                  #Makes the groups and turns them into DICT with generated numbers
    print(group1)
    print(algorithm.find_matching(group1, matching_type = 'min', return_type = 'list') )
    outcome = algorithm.find_matching(group1, matching_type = 'min', return_type = 'list')       #Algorithm
    sett.endTime = time.time()                                                                   #End of stopwatch
    finalOut(outcome)                                                                            #Final string editting 
    input("Press enter to exit!")
    makeLog("LOG","exit","Program has exited with code 0")
    exit(0)

runtime()
