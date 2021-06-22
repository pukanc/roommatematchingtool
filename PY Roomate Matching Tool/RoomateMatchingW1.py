import json, time, re
import excel2json
from hungarian_algorithm import algorithm

class Values:
    debug = True                                    #Debug off == user-mode, Debug on debug
    missingParticipant = False                      #Is there a missing participant
    excelName = "Test.xls"                          #Settings for debug 1
    jsonName  = "Form Responses.json"               #Settings for debug 2
    allOptionsList = []                             #Loading all the questions 
    startTime = 0                                   #Start time of the operation 
    endTime   = 0                                   #End time of the operation
    group1 = []                                     #Group 1 list
    group2 = []                                     #Group 2 list
sett = Values()                                     #Creating a global object

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
            print("[ERR] File not found!")
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
            print("[ERR] File not found!")

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
        print("Not existing")
        return False

#Returns the number of the participants(int), !!!starts with a zero
def numberOfParticipants():
    nOfparticipants = -1
    while True:
        try:
            lookForData("Name ID", nOfparticipants)
        except IndexError:
            break
        nOfparticipants =  nOfparticipants + 1
    return nOfparticipants


#Returns all the data that a participant has, !!!starts with a zero
def dataForParticipant(number):
    jdata = json.loads(open(sett.jsonName).read())
    data = []
    for i in range(0,len(getAllList())):
        data.append(jdata[number][sett.allOptionsList[i]])
    return data

#Q1 - Window - Doulbe points - Two integers needed
def categoryOne(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[3] - otherP[3]
    return abs(minus) * 2

#Q2,Q3 - Speaker music + Playing music, two integers -- Special case
def categoryTwoThree(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[5]
    otherPq5 = 6 - otherP[5]
    calc1 = mainP[4] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[4]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2

#Q4 - Cleanliness orderliness - double, two ints needed 
def categoryFour(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[6] - otherP[6]
    return abs(minus) * 2

#Q5,Q6 - Sharing of items, reversed special, two ints needed 
def categoryFiveSix(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[8]
    otherPq5 = 6 - otherP[8]
    calc1 = mainP[7] - otherPq5
    calc2 = mainPq5 - otherP[7]
    return abs(calc1) + abs(calc2)

#Q7,Q8 - Quiet space, reversed special, two ints neeeded 
def categorySevenEight(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[10]
    otherPq5 = 6 - otherP[10]
    calc1 = mainP[9] - otherPq5
    calc2 = mainPq5 - otherP[9]

    return abs(calc1) + abs(calc2)

#Q9,Q10 - Friends over, specia but not reversed, two ints are needed  
def categoryNineTen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[12]
    otherPq5 = otherP[12]
    calc1 = mainP[11] - otherPq5
    calc2 = mainPq5 - otherP[11]
    return abs(calc1) + abs(calc2)

#Q11,Q12 - Living space, special but not reversed, two ints needed 
def categoryElevenTwelve(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[14]
    otherPq5 = otherP [14]
    calc1 = mainP[13] - otherPq5
    calc2 = mainPq5 - otherP[13]
    return abs(calc1) + abs(calc2)

#Q13,Q14 - Sleeping, special alogorithm
def categoryThirteenFourteen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    #first person
    sleepF1 = mainP[15] - otherP[15]
    wakeF1 = mainP[16] - otherP[16]
    #second person
    sleepF2 = otherP[15] - mainP[15]
    wakeF2 = otherP[16] - mainP[16]
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
            for listss in range(len(group1Listt)):
                exe = allCategories(group1Listt[lists11], group2Listt[listss])
                storingDic.update({group2Listt[listss] : int(exe)})
                if listss == (len(group1Listt) - 1):
                    namesDict.update({group1Listt[lists11] : storingDic})
                    storingDic = {}
    return namesDict

def  uneven1(): #Will be for the new uneven
    pass


#Making the groups of people, inputs two strings (Names of the groups)
def groupMaker(group1, group2):
    group1List = []
    group2List = []
    for group in range(numberOfParticipants()):
        if lookForData("Group", group) == group1:
            group1List.append(int(lookForData("Name ID", group) - 1))
        elif lookForData("Group", group) == group2:
            group2List.append(int(lookForData("Name ID", group) - 1))
                                                                                #Uneven number of participants!!!!
    if len(group1List) != len(group2List):      #Checks for the difference
        if abs(len(group1List) - len(group2List)) == 1:
            if len(group1List) - len(group2List) == 1: #Dominant group 1
                dominantGroup = 0
            else:                                      #Dominant group 2 
                dominantGroup = 1
            #
            generatedValues = []
            sumAll = 0                 #Used in the loop
            testGroup = group1List
            bestGroup = group1List
            if dominantGroup == 1:        
                #Switching the groups
                buffer = group1List
                group1List = group2List
                group2List = buffer
                #Loading the new group 1
                testGroup = group1List
                bestGroup = group1List
            #Comparing one list to another, special algorithm
            for listMain in range(len(group1List)): #Generating the values for this group
                generatedValues.append(sumAll)      #Appends all the sums to a list
                testGroup = []                #Creating a list
                testGroup.extend(group1List)  #Resets the value
                testGroup.pop(listMain)       #Deletes one object from LIST
                sumAll = 0
                for lists1 in range(len(group2List)):
                    for lists in range(len(group2List)):
                        exe = allCategories(testGroup[lists1], group2List[lists])
                        sumAll += exe
            generatedValues.pop(0)            #removes the first 0 from the list
            #
            checker = 10000000
            checker_value = 0
            #
            for check in range(len(generatedValues)):      #Searches for the smallest sum in the whole LIST
                if checker > generatedValues[check]:       #If a sum is smaller than checker then it gets into checker
                    checker = generatedValues[check]
                    checker_value = check
            #
            sett.missingParticipant = bestGroup[checker_value]  #Saves the User ID to the class
            bestGroup.pop(checker_value)                        #Removes the number
            finalR = groupDic(bestGroup, group2List)            #Creates a Dict
            if sett.debug == True: print(finalR)
            return finalR
 

        #More people are uneven
        else:
            print("Difference of paricipants bigger than 1, not supported yet!")
            time.sleep(3)
            exit()
                                                                        #Number of participants is equal
    else:                                                               #Creating the dict -- Number of participants is even
        namesDict = {}
        storingDic = {}
        for lists1 in range(len(group1List)):
            for lists in range(len(group1List)):
                exe = allCategories(group1List[lists1], group2List[lists])
                storingDic.update({group2List[lists] : int(exe)})
                if lists == (len(group1List) - 1):
                    namesDict.update({group1List[lists1] : storingDic})
                    storingDic = {}
    return(namesDict)

    
#Final output system, edits the output and puts it into groups, input should be the output from the algorithm
def finalOut(outcome):
    if sett.debug == True: print("The output of the algorithm is: {}".format(outcome))
    print()
    time_convert(sett.endTime - sett.startTime)                                             #Prints out the time it took
    print()
    print("Numbers are matching with the Name IDs!!")
    for a in range(len(outcome)):                                                           #Prints out by rooms
        out = outputEditor(str(outcome[a]))
        print("Room {}: {}, {}".format(a+1, out[0], out[1]))
    if sett.missingParticipant != False:
        print("Room {}: {}, - alone".format(a+2, sett.missingParticipant+1))


#Prints out some basic data
def announceData():
    print("Number of registered participants: {}".format(numberOfParticipants()))
    print("Number of registered questions: {}".format(len(getAllList())))


#Announces data
announceData()
time.sleep(2)


#Input group
print("Which groups should be used! eg. F3, F4")
fg = input("Group one: ")
sg = input("Group two: ")
sett.startTime = time.time()                                                                 #Start of stopwatch
group1 = groupMaker(fg, sg)                                                                  #Makes the groups and turns them into DICT with generated numbers
outcome = algorithm.find_matching(group1, matching_type = 'min', return_type = 'list')       #Algorithm
sett.endTime = time.time()                                                                   #End of stopwatch
finalOut(outcome)                                                                            #Final string editting 
