import json, time, excel2json, os, math
from typing import Dict
import km_matcher as km
from datetime import datetime
class Values:
    version = "1.0.1"
    debug = False                                    #Debug off == user-mode, Debug on debug
    missingParticipant = False                      #Is there a missing participant
    excelName = "Test.xls"                          #Settings for debug 1
    jsonName  = "Form Responses 1.json"             #Settings for debug 2 
    questionOffsets = {"Group" : 0, "Name ID" : 1 ,"Slovak" : 2, "RA" : 3, "Ban" : 4,"Hall" : 5, "Mixed" : 6 ,"Q1" : 7, "Q2Q3" : [8,9],
    "Q4" : 10, "Q5Q6" : [11,12], "Q7Q8": [13,14], "Q9Q10" : [14,15,16], "Q11Q12" : [17,18], "Q13Q14" : [19,20,21]} 
    allOptionsList = []                             #Loading all the questions 
    startTime = 0                                   #Start time of the operation 
    endTime   = 0                                   #End time of the operation
    group1 = []                                     #Group 1 list
    group2 = []                                     #Group 2 list
    dictionary = {}                                 #Used in the output system
    uneven = False                                  #Is the output from the hungarian uneven
    #
    internationalSt = False                        #For international students -- If True than then they can be in 1 room -- If False they cant be in 1 room
    oldStudentsHall = True                         #If true "Hall" will be taken into account - If false it wont
    mixedhalls = True                              #True - Program will take into account the mixing rules \ False - It wont -- Mixing rules "Mixed"
    raBan = True                                   #If true two RA members in a matching will get a penalty
    memberBans = True                              #If true then members who share the same ban number will get a penalty
    dummyMember = True                             #Dummy member -- Set true means that the dummy will get into the smaller group -- False means it will get in the bigget group 

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
        print(f"Fatal Error check rmLog.txt for more information! It can be found here {path}!")
        print("\n\n")
        input("Press enter to exit!")
        exit(0)
    return True

def start():
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

def time_convert(sec):
    """Converts time -- for the stopwatch"""
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Results calculated, it took {0}h:{1}m:{2}s to calculate!".format(int(hours),int(mins),round(int(sec))))
    makeLog("LOG", "time_convert()", "Results calculated, it took {0}h:{1}m:{2}s to calculate!".format(int(hours),int(mins),round(int(sec))))

def getAllList():
    """
    Handling of the questions -- All the questions are returned in a list
    """
    res = json.loads(open(str(sett.jsonName)).read())
    list = []
    #Add a log event
    if res[1].keys() == res[2].keys():
        for key in res[0].keys():
            list.append(key)
    return list




def lookForData(jClass, numberWhere):
    """
    Searches in the JSON file -- Name of the attribute and the number of the block where it is located (starts with zero)
    """
    if jClass not in sett.allOptionsList:
        jClass = sett.allOptionsList[jClass]
    jdata = json.loads(open(str(sett.jsonName)).read())
    try:
        return jdata[numberWhere][jClass]
    except KeyError:
        makeLog("LOG", f"lookForData({jClass},{numberWhere})", "Data not found!")
        return False

def numberOfParticipants():
    """
    Returns the number of the participants(int), !!!starts with a 1
    """
    nOfparticipants = 0
    while True:
        try:
            lookForData(sett.questionOffsets["Name ID"], nOfparticipants)
        except IndexError:
            break
        nOfparticipants += 1
    return nOfparticipants


def dataForParticipant(number):
    """
    Returns all the data that a participant has, !!!starts with a zero
    """
    jdata = json.loads(open(sett.jsonName).read())
    data = []
    try:
        for i in range(0,len(getAllList())):
            data.append(jdata[number][sett.allOptionsList[i]])
    except IndexError:
        return False
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
    mainPq5 = (mainP[sett.questionOffsets["Q2Q3"][0]]-1)*(otherP[sett.questionOffsets["Q2Q3"][1]]-1)
    otherPq5 = (otherP[sett.questionOffsets["Q2Q3"][0]] - 1)*(mainP[sett.questionOffsets["Q2Q3"][1]]-1)
    return round(math.sqrt(mainPq5) + math.sqrt(otherPq5), 2)

#Q4 - Cleanliness orderliness - double, two ints needed 
def categoryFour(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[sett.questionOffsets["Q4"]] - otherP[sett.questionOffsets["Q4"]]
    return abs(minus) * 2

#Q5,Q6 - Sharing of items, reversed special, two ints needed  ----- Not matching (2,45)  4
def categoryFiveSix(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = (mainP[sett.questionOffsets["Q5Q6"][0]]-1)*(otherP[sett.questionOffsets["Q5Q6"][1]]-1)
    otherPq5 = (otherP[sett.questionOffsets["Q5Q6"][0]] - 1)*(mainP[sett.questionOffsets["Q5Q6"][1]]-1)
    return round(math.sqrt(mainPq5) + math.sqrt(otherPq5), 2)

#Q7,Q8 - Quiet space, reversed special, two ints neeeded    (4.90) - 2
def categorySevenEight(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    one = (mainP[sett.questionOffsets["Q7Q8"][0]]-1)*(otherP[sett.questionOffsets["Q7Q8"][1]] - 1)
    two = (otherP[sett.questionOffsets["Q7Q8"][0]] - 1)*(mainP[sett.questionOffsets["Q7Q8"][1]] - 1)
    return round(math.sqrt(one)+math.sqrt(two), 2)

#Q9,Q10 - Friends over, specia but not reversed, two ints are needed  (0.96) -- 1
def categoryNineTen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[sett.questionOffsets["Q9Q10"][1]]
    otherPq5 = otherP[sett.questionOffsets["Q9Q10"][1]]
    I2 = mainP[sett.questionOffsets["Q9Q10"][0]]
    J2 = mainP[sett.questionOffsets["Q9Q10"][1]]
    K2 = mainP[sett.questionOffsets["Q9Q10"][2]]
    K3 = otherP[sett.questionOffsets["Q9Q10"][2]]
    J3 = otherP[sett.questionOffsets["Q9Q10"][1]]
    I3 = otherP[sett.questionOffsets["Q9Q10"][0]]
    if J2 <= K3:
    	one = 0
    else:
    	one = (J2-K3)*(I2-1)
    	one = math.sqrt(one)
    ###
    if J2 <= K3:
    	two = 0
    else:
    	two = (J2 - K3) * (I2-1)/4
    oneTwo = (one+two)/2
    ##
    if J3<=K2:
    	three = 0
    else:
    	three= (J3-K2)*(I3-1)
    	three = math.sqrt(three)
    if J3<=K2:
    	four = 0
    else:
    	four = (J3-K2)*(I3-1)/4
    threeFour =  (three + four)/2
    return round(oneTwo + threeFour, 2)


#Q11,Q12 - Living space, special but not reversed, two ints needed 
def categoryElevenTwelve(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[sett.questionOffsets["Q11Q12"][1]]
    otherPq5 = otherP[sett.questionOffsets["Q11Q12"][1]]
    calc1 = mainP[sett.questionOffsets["Q11Q12"][0]] - otherPq5
    calc2 = mainPq5 - otherP[sett.questionOffsets["Q11Q12"][0]]
    ###
    one = (abs(mainP[sett.questionOffsets["Q11Q12"][1]] - otherP[sett.questionOffsets["Q11Q12"][0]])*(mainP[sett.questionOffsets["Q11Q12"][0]] - 1))/ 4
    two = (abs(otherP[sett.questionOffsets["Q11Q12"][1]] - mainP[sett.questionOffsets["Q11Q12"][0]])*(otherP[sett.questionOffsets["Q11Q12"][0]]-1))/  4
    return one + two

#Q13,Q14 - Sleeping, special alogorithm
def categoryThirteenFourteen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    #first person
    sleepF1 = mainP[sett.questionOffsets["Q13Q14"][1]] - otherP[sett.questionOffsets["Q13Q14"][1]] #0
    wakeF1 = mainP[sett.questionOffsets["Q13Q14"][2]] - otherP[sett.questionOffsets["Q13Q14"][2]]   # -1
    #second person
    sleepF2 = otherP[sett.questionOffsets["Q13Q14"][1]] - mainP[sett.questionOffsets["Q13Q14"][1]]  #0
    wakeF2 = otherP[sett.questionOffsets["Q13Q14"][2]] - mainP[sett.questionOffsets["Q13Q14"][2]]   # 1
    #Person one sleep
    if sleepF1 < 0:
        person1s = (-sleepF1 + 1)/(6-mainP[sett.questionOffsets["Q13Q14"][0]])/(5/4)
    else:
        person1s = 0
    #Person two sleep
    if sleepF2 < 0:
        person2s = (-sleepF2 + 1)/(6-otherP[sett.questionOffsets["Q13Q14"][0]])/(5/4)
    else:
        person2s = 0
    #Person one wake
    if wakeF1 > 0:
        person1w = (wakeF1 + 1)/(6-mainP[sett.questionOffsets["Q13Q14"][0]])/(5/4)
    else:
        person1w = 0
    #Person two wake
    if wakeF2 > 0:
        person2w = (wakeF2 + 1)/(6-otherP[sett.questionOffsets["Q13Q14"][0]])/(5/4)
    else:
        person2w = 0
    return (person1w + person2w + person1s + person2s) * 2

#---------------------------------------------------------------------------------------------------------

#Execution two ints -- represeting members (Member ID - 1)
def allCategories(mem1, mem2):
    """
    Returns a sum
    1. Arg - Name ID - 1 of the participant
    2. Arg - Name ID - 1 of the participant
    """
    together = categoryOne(mem1,mem2) + categoryTwoThree(mem1,mem2) + categoryFour(mem1,mem2) + categoryFiveSix(mem1,mem2) + categorySevenEight(mem1,mem2) +categoryNineTen(mem1,mem2) + categoryElevenTwelve(mem1,mem2) + categoryThirteenFourteen(mem1,mem2)
    firstp =  dataForParticipant(mem1)
    secondp = dataForParticipant(mem2)
    #RA matching
    if sett.raBan == True:  
        if firstp[sett.questionOffsets["RA"]] != "" and firstp[sett.questionOffsets["RA"]] == secondp[sett.questionOffsets["RA"]] and firstp[sett.questionOffsets["RA"]] == "Y":
            together += 10000
            #Penalty for two ARs
    #Member bans
    if sett.memberBans == True: 
            if firstp[sett.questionOffsets["Ban"]] != "" and firstp[sett.questionOffsets["Ban"]] == secondp[sett.questionOffsets["Ban"]]:
                together = 100000
    #International students
    if sett.internationalSt == False and firstp[sett.questionOffsets["Slovak"]] == "N" and secondp[sett.questionOffsets["Slovak"]] == "N":
        together += 10000
    #MixedHalls 
    if sett.mixedhalls == True:
        if firstp[sett.questionOffsets["Mixed"]] == "Y" and secondp[sett.questionOffsets["Mixed"]] == "NN" :
            together += 10000
    if sett.mixedhalls == True: 
        if firstp[sett.questionOffsets["Mixed"]] == "NN" and secondp[sett.questionOffsets["Mixed"]] == "Y":
            together = 100000
    #Old students hall
    if sett.oldStudentsHall == True:
            if firstp[sett.questionOffsets["Hall"]] != "" and secondp[sett.questionOffsets["Hall"]] != "" and firstp[sett.questionOffsets["Hall"]] != secondp[sett.questionOffsets["Hall"]]:
                together = 100000
    return together**2


def outputEditor(output, getSumOutOfAlgo = False):
    """
    1. Arg - Output from the Hungarian Algorithm
    2. Arg - If true the program will pass the sum output from the algorithm
    Alligns the numbers with the real PID numbers.
    Outputs [[0,1,2],[4,5,6]]
    """
    rtrnList = []
    for mem in range(len(output) - 1):
        string = output[mem]
        newOut = string[0].split(",")
        rtrnList.append([int(newOut[0]),int(newOut[1]),float(newOut[2])])
    rtrnList.append(output[len(output) - 1][0])
    makeLog("LOG", "outputEditor()", "Output from the algorithm was converted successfully")
    if getSumOutOfAlgo == True:
        return float(output[len(output) - 1][0])
    '''
    Editing the numbers to the original numbers
    '''
    dictKeys = list(sett.dictionary.keys())
    smallDict = sett.dictionary[list(sett.dictionary.keys())[0]] 
    dictMem = list(smallDict.keys())
    #Changing the X
    for num in range(len(dictKeys)):
        number = rtrnList[num][0]
        rtrnList[num][0] = dictKeys[number] + 1
    #Changing the Y
    for num in range(len(dictMem)):
        number = rtrnList[num][1]
        rtrnList[num][1] = dictMem[number] + 1
    #0 member
    for mem in range(len(rtrnList)):
            if rtrnList[mem][0] == 77778:
                rtrnList[mem][0] = rtrnList[mem][1]
                rtrnList[mem][1] = "- alone"
            if rtrnList[mem][1] == 77778:
                rtrnList[mem][1] = "- alone"
    #Creating two lists -- Because of unevenUneven
    oldRtrnList = rtrnList.copy()
    rtnrList2 = []
    if sett.uneven == True:
        oldRtrnList = rtrnList.copy()
        cacheList = []
        rtnrList2 = []
        for members in range(len(oldRtrnList) - 1):   #Accesing every part of rtnList
            if rtrnList[members][0] in cacheList or rtrnList[members][1] in cacheList:
                rtnrList2.append(rtrnList[members])
                oldRtrnList.remove(rtrnList[members])
                continue
            cacheList.append(rtrnList[members][0])
            cacheList.append(rtrnList[members][1])
    return [oldRtrnList, rtnrList2]

def groupDicUN(group1Listt, group2Listt, dummyMember = 77777):
    """
    Specifically made for the new unevenalgorithm because it has some special functionality!
    1. Arg - list 1
    2. Arg - list 2
    3. Arg - DummyMember -- Native(False) -- But the dummy member should be passed
    """
    #Which group is dominant(bigger)?
    g1 = group1Listt.copy()
    g2 = group2Listt.copy()
    newList = []
    newList.extend(group1Listt)
    newList.extend(group2Listt)
    group1Listt = newList
    group2Listt = newList
    if len(newList) != len(newList):
        makeLog("FERR", "groupDic()", "Group1List and Group2List is not the same size")
    namesDict = {}
    storingDic = {}
    for lists11 in range(len(group1Listt)):            #First for loop
            for listss in range(len(group2Listt)):     #Second for loop
                if group1Listt[lists11] == group2Listt[listss]:
                    exe = 100000
                #Dummy member
                elif dummyMember == group1Listt[lists11] or dummyMember == group2Listt[listss]:
                    if sett.dummyMember == True:
                        if dummyMember != group1Listt[lists11] and group1Listt[lists11] in g2:
                            exe = 100000
                        elif dummyMember != group1Listt[listss] and group1Listt[listss] in g2:
                            exe = 100000
                        else:
                            exe = 0
                    elif dummyMember != group1Listt[lists11] and group1Listt[lists11] in g1:
                        exe = 100000
                    elif dummyMember != group1Listt[listss] and group1Listt[listss] in g1:
                        exe = 100000
                    else:
                        exe = 0
                elif group1Listt[lists11] in g2 and group2Listt[listss] in g2:
                    exe = 100000
                else:
                    exe = allCategories(group1Listt[lists11], group2Listt[listss])
                #
                storingDic.update({group2Listt[listss] : int(exe)})
                if listss == (len(group1Listt) - 1):
                    namesDict.update({group1Listt[lists11] : storingDic})
                    namesDict.update({group1Listt[lists11] : storingDic})
                    storingDic = {}
    return namesDict
def dictTranslator(dictt):
    """
    1. Arg - DictOfDicts
    Translates the old form of dictonaries into the appropriate ListsOfLists format.
    """
    sett.dictionary = dictt
    mainList = []
    for x in list(dictt.values()):
        mainList.append(list(x.values()))
    #
    for number in range(len(mainList)):
        for number2 in range(len(mainList[number])):
            mainList[number][number2] = 3000 - mainList[number][number2]
            pass
    if len(mainList) > 1:
        pass
    else:
        makeLog("FERR", "dictTranslator()", f"Lenght of the translation is: {len(mainList)}")
    if len(mainList) == len(mainList[0]):
        makeLog("LOG", "dictTranslator()", "Dict was translated to a list successfully")
    else:
        makeLog("FERR","dictTranslator(dictt)","len(x) != len(y)", True)
    return mainList
def unevenAlgorithm(list1, list2):
    """
    Algorithm for solving uneven lists
    1. Arg - List 1 
    2. Arg - List 2
    """
    makeLog("LOG", "unevenAlgorithm()", "Using unevenAlgorithm")
    if (len(list1) + len(list2)) % 2 == 0:
        even = True
        makeLog("LOG", "unevenAlgorithm()", f"Lists are even! Even: {even}")
    else:
        even = False
        makeLog("LOG", "unevenAlgorithm()", f"Lists are odd! Even: {even}")
    copy_list1 = list1.copy()
    copy_list2 = list2.copy()
    newList = []
    #newList now is the list of all lists
    if even == True: 
        rtn = groupDicUN(copy_list1,copy_list2, False)
    if even == False:
        if sett.dummyMember == True:
            copy_list2.append(77777) #dummy member
        else:
            copy_list1.append(77777)
        rtn = groupDicUN(copy_list1,copy_list2, 77777)
    makeLog("LOG", "unevenAlgorithm()", "Dict was returned")
    return rtn
#Algorithm for groups where the difference is bigger than 1
def unevenUnevenAlgo(list1,list2):
    if (len(list1) - len(list2)) > 0:          #Dominant group1(List1)
        difference = (len(list1) - len(list2)) #Difference 

    else:                                      #Dominant group2(List2)
        difference = (len(list2) - len(list1)) #Difference 
        buffer = list1
        list1 = list2
        list2 = buffer
    dictOut = unevenAlgorithm(list1,list2)
    return dictOut

def evenAlgo(group1List, group2List, dummyMember = False): 
    namesDict = {}
    storingDic = {}
    for lists1 in range(len(group1List)):
        for lists in range(len(group1List)):
            if dummyMember == True:
                if 77777 == group1List[lists1] or 77777 == group2List[lists]:
                    exe = 0
                else:
                    exe = allCategories(group1List[lists1], group2List[lists])
            else:
                exe = allCategories(group1List[lists1], group2List[lists])
            storingDic.update({group2List[lists] : int(exe)})
            if lists == (len(group1List) - 1):
                namesDict.update({group1List[lists1] : storingDic})
                storingDic = {}
    return namesDict                 #Returns dict

#Making the groups of people, inputs two strings (Names of the groups)
def groupMaker(group1, group2):
    group1List = []
    group2List = []
    for group in range(numberOfParticipants()):
        if lookForData("Group", group) == group1:
            group1List.append(int(lookForData(sett.questionOffsets["Name ID"], group) - 1))
        elif lookForData("Group", group) == group2:
            group2List.append(int(lookForData(sett.questionOffsets["Name ID"], group) - 1))
    #
    makeLog("LOG", "groupMaker()", f"Group 1 size: {len(group1List)}, Group 2 size: {len(group2List)}" )
    if len(group1List) == 0 or len(group2List) == 0:
        makeLog("FERR", "groupMaker", f"Size of one or both groups is 0", True)
    #
    elif len(group1List) == len(group2List):          #Creating the dict -- Number of participants is even
        makeLog("LOG", "groupMaker()", f"evenAlgo() was called because the number of participants is even")
        sett.uneven = False
        return evenAlgo(group1List, group2List)
    #uneven 1
    elif abs(len(group1List) - len(group2List)) == 1:
        makeLog("LOG", "groupMaker()", f"evenAlgo() was called because the number of participants is bigger than one, dummy member attached")
        if len(group1List) < len(group2List):
            group1List.append(77777)
        else:
            group2List.append(77777)
        return evenAlgo(group1List, group2List, True)
    #
    else:
        makeLog("LOG", "groupMaker()", f"unevenUnevenAlgo() was called because the number of participants is not even: {abs(len(group1List) - len(group2List))}")
        sett.uneven = True
        rtrn = unevenUnevenAlgo(group1List,group2List)
        if type(rtrn) is dict:
            return rtrn

#Final output system, edits the output and puts it into groups, input should be the output from the algorithm
def finalOut(outcome):
    print()
    time_convert(sett.endTime - sett.startTime)                                             #Prints out the time it took
    print()
    print("Numbers are matching with the Name IDs!! \n\n")
    try:
        f = open("roommates.txt","w")
    except PermissionError:
        makeLog("FERR", "finalOut()", "PermissionError - Program can not acces the roommates.txt. Try to turn off your txt editor")
    try:
        s = open("roommates.csv", "w")
    except PermissionError:
        makeLog("FERR", "finalOut()", "PermissionError - Program can not acces the roommates.csv file. Try to turn off Excel...")
    s.write('"Room number" "Member 1" "Member 2" "Weight" "Total Weight"\n')
    d = datetime.now().strftime("%d/%B/%Y - %H:%M:%S")
    f.write(f"[{d}] \n")
    out = outputEditor(outcome)
    price = 0
    price1 = 0
    print("--- Matching 1 ---")
    f.write("--- Matching 1 ---\n")
    for a in range(len(out[0]) - 1):#Prints out by rooms -- -1 because the value is attached
        price += abs(out[0][a][2]-3000)
        if out[0][a][1] == "- alone":
            print("Room {}: {} - alone".format(a+1, out[0][a][0], out[0][a][1]))
            f.write("Room {}: {} -alone \n".format(a+1, out[0][a][0], out[0][a][1]))
            s.write(f'{a+1} {out[0][a][0]} {"alone"} {""}\n')
            continue
        s.write(f'{a+1} {out[0][a][0]} {out[0][a][1]} {abs(out[0][a][2]-3000)}\n')
        print("Room {}: {}, {} with a pair-value {}".format(a+1, out[0][a][0], out[0][a][1], abs(out[0][a][2]-3000)))
        f.write("Room {}: {}, {} with a pair-value {} \n".format(a+1, out[0][a][0], out[0][a][1], abs(out[0][a][2]-3000)))
    makeLog("LOG", "finalOut()","Matching 1 ... OK")
    ###########################
    #Second out
    if len(out[1]) > 0:
        print("\n\n--- Matching 2 ---")
        f.write("\n--- Matching 2 ---\n")
        s.write(f'{""} {""} {""} {""}\n')
        for a in range(len(out[1])):#Prints out by rooms
            price1 += abs(out[1][a][2]-3000)
            if out[1][a][1] == "- alone":
                print("Room {}: {} - alone".format(a+1, out[1][a][0], out[1][a][1]))
                f.write("Room {}: {} - alone\n".format(a+1, out[1][a][0], out[1][a][1]))
                s.write(f'{a+1} {out[1][a][0]} {"alone"} {""}\n')
                continue
            s.write(f'{a+1} {out[1][a][0]} {out[1][a][1]} {abs(out[1][a][2]-3000)}\n')
            print("Room {}: {}, {} with a pair-value {}".format(a+1, out[1][a][0], out[1][a][1], abs(out[1][a][2]-3000)))
            f.write("Room {}: {}, {} with a pair-value {} \n".format(a+1, out[1][a][0], out[1][a][1], abs(out[1][a][2]-3000)))
        makeLog("LOG", "finalOut()","Matching 2 ... OK")
    makeLog("LOG", "finalOut()",f"The sum is: Price 1: {price} Price 2: {price1}")
    f.write(f"\nThe total sum is: {price + price1}")
    print(f"\nThe sum is: Matching 1: {price} Matching 2: {price1}")
    s.write(f'"" "" "" "" {price + price1}')
    #
    path = os.getcwd() + r"\roommates.txt"
    path1 = os.getcwd() + r"\roommates.csv"
    print(f"\nFile roommates.csv was created! It can be found here: {path1}")
    print(f"File roommates.txt was created! It can be found here: {path}\n")
    makeLog("LOG", "finalOut", f"File roommates.txt was created! It can be found here: {path}", False)
    makeLog("LOG", "finalOut", f"File roommates.csv was created! It can be found here: {path1}")
    f.close()
    s.close()
#Prints out some basic data

def announceData():
    print("\nVersion: {} \n".format(sett.version))
    print("Number of registered participants: {}".format(numberOfParticipants()))
    print("Number of registered questions: {} \n".format(len(getAllList())))
    makeLog("LOG", "STARTUP", f"Version: {sett.version}")
    makeLog("LOG", "STARTUP", f"Debug: {sett.debug}")
    makeLog("LOG", "STARTUP", f"Number of registered participants: {numberOfParticipants()}")
    makeLog("LOG", "STARTUP", f"Number of registered questions: {len(getAllList())}")

def announceSettings():
    """
    Will announce the current settings
    No Args 
    """
    print("\n\n\n\n\n---SETTINGS---\n")
    #
    print(f"1. It is not allowed for 2 international students to be roommates: {bool(1-sett.internationalSt)} \n")
    makeLog("LOG","announceSettings()", f"Is it allowed for 2 international students to be roommates: {sett.internationalSt}")
    #
    print(f"2. Already assigned halls will be taken into into account: {sett.oldStudentsHall} \n")
    makeLog("LOG","announceSettings()", f"Already assigned halls will be taken into into account: {sett.oldStudentsHall}")
    #
    print(f"3. Hall preferred sex will be taken into account: {sett.mixedhalls} \n")
    makeLog("LOG", "announceSettings()", f"Hall preferred sex will be taken into account: {sett.mixedhalls}")
    #
    print(f"4. 2 RAs can not be roommates: {sett.raBan} \n")
    makeLog("LOG", "announceSettings()", f"2 RAs can not be roommates: {sett.raBan}")
    #
    print(f"5. Roommate bans will be taken into account: {sett.memberBans} \n")
    makeLog("LOG", "announceSettings()", f"Roommate bans will be taken into account: {sett.memberBans}")
    #
    print(f"6. Dummy roommate matched to bigger group: {sett.dummyMember} \n")
    makeLog("LOG", "announceSettings()", f"Dummy roommate matched to bigger group: {sett.dummyMember}")

def setSettings():
    """
    Let the user specify/check the current settings
    No args needed
    """
    announceSettings()
    cin = input("\nDo you want to change the settings [y/n] ")
    if str(cin) == "y" or str(cin) == "Y":
        x = True
        while x:
            print("\n\n\n")
            announceSettings()
            cin = input("Please select the question you want to edit [1,2,3,4,5,6] ")
            try:
                cin = int(cin)
            except:
                makeLog("ERR", "setSettings()", f"User input was invalid: {cin}")
                print("Input is invalid! \n")
                continue
            if cin == 1:
                new = input("It is not allowed for 2 international students to be roommates: [true, false] ")
                if str(new) == "true" or str(new) == "True":
                    new = False     #inverted
                elif str(new) == "false" or str(new) == "False":
                    new = True      #inverted
                else:
                    makeLog("ERR", "setSettings()", f"cin==1 User input was invalid: {new}")
                    print("Input was invalid!")
                    time.sleep(1)
                    continue
                sett.internationalSt = new
                setSettings()
                return
            ####
            if cin == 2:
                new = input("Already assigned halls will be taken into into account: [true,false] ")
                if str(new) == "true" or str(new) == "True":
                    new = True
                elif str(new) == "false" or str(new) == "False":
                    new = False
                else:
                    makeLog("ERR", "setSettings()", f"cin==2 User input was invalid: {new}")
                    print("Input was invalid!")
                    time.sleep(1)
                    continue
                sett.oldStudentsHall = new
                setSettings()
                return
            ###
            if cin == 3:
                new = input("Hall preferred sex will be taken into account: [true,false] ")
                if str(new) == "true" or str(new) == "True":
                    new = True
                elif str(new) == "false" or str(new) == "False":
                    new = False
                else:
                    makeLog("ERR", "setSettings()", f"cin==3 User input was invalid: {new}")
                    print("Input was invalid!")
                    time.sleep(1)
                    continue
                sett.mixedhalls = new
                setSettings()
                return
            ###
            if cin == 4:
                new = input("2 RAs can not be roommates: [true,false] ")
                if str(new) == "true" or str(new) == "True":
                    new = True     
                elif str(new) == "false" or str(new) == "False":
                    new = False     
                else:
                    makeLog("ERR", "setSettings()", f"cin==4 User input was invalid: {new}")
                    print("Input was invalid!")
                    time.sleep(1)
                    continue
                sett.raBan = new
                setSettings()
                return
            ###
            if cin == 5:
                new = input("Roommate bans will be taken into account: [true,false] ")
                if str(new) == "true" or str(new) == "True":
                    new = True
                elif str(new) == "false" or str(new) == "False":
                    new = False
                else:
                    makeLog("ERR", "setSettings()", f"cin==5 User input was invalid: {new}")
                    print("Input was invalid!")
                    time.sleep(1)
                    continue
                sett.memberBans = new
                setSettings()
                return
            if cin == 6:
                new = input("Dummy roommate matched to bigger group: [true,false] ")
                if str(new) == "true" or str(new) == "True":
                    new = True
                elif str(new) == "false" or str(new) == "False":
                    new = False
                else:
                    makeLog("ERR", "setSettings()", f"cin==5 User input was invalid: {new}")
                    print("Input was invalid!")
                    time.sleep(1)
                    continue
                sett.dummyMember = new
                setSettings()
                return
            else:
                makeLog("ERR", "setSettings()", f"User failed to choose the question he/she wants to edit: {cin}")
                print("Invalid input")
                time.sleep(1)
    else:
        print("\n\n")
        return True
def runtime():
    """
    Main function
    """
    makeLog("CLR") #Clears the LOG file
    #Input group
    start()
    sett.allOptionsList = getAllList()
    announceData()
    print("\n\n")
    print("Which groups should be used! eg. F3, F4")
    fg = input("Group one: ")
    sg = input("Group two: ")
    makeLog("LOG", "input Groups",f"Group 1: {fg}, Second Group: {sg}")
    setSettings()
    sett.startTime = time.time()                                                                 #Start of stopwatch
    group1 = dictTranslator(groupMaker(fg, sg))
    matcher = km.KMMatcher(group1)
    outcome = matcher.solve(verbose=True)
    sett.endTime = time.time()                                                                   #End of stopwatch
    finalOut(outcome)                                                                       #Final string editting 
    input("Press enter to exit!")
    makeLog("LOG","exit","Program has exited with code 0")
    exit(0)
runtime()
