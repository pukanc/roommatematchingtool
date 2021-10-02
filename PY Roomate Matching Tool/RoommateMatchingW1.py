import json, time, excel2json, os, math
import huAlgo as km
import blossomAlgo as blossom
from datetime import datetime

class Values:
    version = "1.0.2"
    debug = False                               #Debug off == user-mode, Debug on debug
    excelName = "Test.xls"                          #Settings for debug 1
    jsonName  = "Form Responses 1.json"             #Settings for debug 2 
    questionOffsets = {"Group" : 1, "Name ID" : 2 ,"Slovak" : 3, "RA" : 4, "Ban" : 5, "Antiban" : 6,"Hall" : 7, "Mixed" : 8 ,"Q1" : 9, "Q2Q3" : [10,11],
    "Q4" : 12, "Q5Q6" : [13,14], "Q7Q8": [15,16], "Q9Q10" : [16,17,18], "Q11Q12" : [19,20], "Q13Q14" : [21,22,23]} 
    allOptionsList = []                             #Loading all the questions 
    startTime = 0                                   #Start time of the operation 
    endTime   = 0                                   #End time of the operation
    dictionary = {}                                 #Used in the output system
    uneven = False                                  #Is the output from the hungarian uneven
    dictOfNames = {}                                #Saving the ids to the names
    matrix  = {None}                                #Matrix used in the final dump
    usedBlossom = False                             #True if the blossom algorithm was used
    dummyMemberName = 77777                         #Checks if a dummy member was added
    #
    internationalSt = False                        #For international students -- If True than then they can be in 1 room -- If False they cant be in 1 room
    oldStudentsHall = True                         #If true "Hall" will be taken into account - If false it wont
    mixedhalls = True                              #True - Program will take into account the mixing rules \ False - It wont -- Mixing rules "Mixed"
    raBan = True                                   #If true two RA members in a matching will get a penalty
    memberBans = True                              #If true then members who share the same ban number will get a penalty
    memberAntiban = True                           #it should also look at whether they're not "antibanned", and only gives the penalty if they are not antibanned.
    dummyMember = True                             #Dummy member -- Set true means that the dummy will get into the smaller group -- False means it will get in the bigget group 
    newStudentsMixedHall = False                   #New students only matched together if OK with mixed hall/ If this setting is changed to TRUE, it will add a penalty of 100000 to 

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
    d = datetime.now().strftime("%H:%M:%S")
    file = open("rmLog.txt", "a")
    file.write(f"[{d}] " + newString)
    file.close()
    if typeOfLog == "FERR":
        path = os.getcwd() + r"\rmLog.txt"
        print(f"Fatal Error check rmLog.txt for more information! It can be found here {path}!")
        print("\n\n")
        input("Press enter to exit!")
        exit(0)
    return True

def start():
    if sett.debug != True:
        #Trying to find the .xls file
        dirs = os.listdir()
        counter = 0
        sett.excelName = None
        print("\n\nSearching for an .xls file!")
        makeLog("LOG", "start()", "Searching for an .xls file")
        for num in range(len(dirs)):
            if len(dirs[num].split(".xls")) == 2: 
                if len(str(dirs[num].split(".xls")[1])) == 0:
                    counter += 1
                    sett.excelName = str(dirs[num])
            #Two xls files found
            if counter == 2:
                sett.excelName = None
                break
        #Xls
        if sett.excelName != None:
            print("Found!")
            makeLog("LOG", "start()", "Found")
            excel2json.convert_from_file(sett.excelName)
        else:
            print("Not found!")
            makeLog("LOG", "start()", "File not found!")
            sett.excelName = str(input("\nPlease input the name of the .xls file! "))
            excel2json.convert_from_file(sett.excelName)
        #Xls
        time.sleep(2.5)
        makeLog("LOG", "start()", "File converted to .json")
        makeLog("LOG", "start()", "Searching for an json. file")
        #Json
        print("\n\nSearching for the created .json file!")
        dirs = os.listdir() #Update
        sett.jsonName = None
        counter = 0
        for num in range(len(dirs)):
            if len(dirs[num].split(".json")) == 2:
                counter += 1
                sett.jsonName = str(dirs[num])
            #Two json files found
            if counter == 2:
                sett.jsonName = None
                break
        ###
        if sett.jsonName != None:
            print("Found!")
            time.sleep(2.5)
            print("\n\n\n")
            makeLog("LOG", "start()", "Json found")
        else:
            print("Not found!")
            time.sleep(2.5)
            makeLog("LOG", "start()", "Json file not found!")
            sett.jsonName = str(input("\nPlease input the name of the .json file! "))
            print("\n\n\n")
        try:
            json.loads(open(str(sett.jsonName)).read())
        except FileNotFoundError:
            makeLog("ERR", "JSON file selector", "File not found!", True)
    else:
        excel2json.convert_from_file(str(sett.excelName))

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
        if type(jClass) == str:
             jClass = sett.allOptionsList[sett.questionOffsets[jClass]]
        else:
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
    together = together**2
    #RA matching
    if sett.raBan == True:
        if firstp[sett.questionOffsets["RA"]] != "" and firstp[sett.questionOffsets["RA"]] == secondp[sett.questionOffsets["RA"]] and firstp[sett.questionOffsets["RA"]] == "Y":
            together += 10000
    #Member bans
    if sett.memberBans == True:
        if sett.memberAntiban == True:  #Ban with antiban
            if firstp[sett.questionOffsets["Antiban"]] != "" and firstp[sett.questionOffsets["Antiban"]] == secondp[sett.questionOffsets["Antiban"]]:#Checks if antibanned
                pass
            else: # not antibanned and checks if banned
                if firstp[sett.questionOffsets["Ban"]] != "" and firstp[sett.questionOffsets["Ban"]] == secondp[sett.questionOffsets["Ban"]]:
                    together += 100000
        else: #Pure Ban
            if firstp[sett.questionOffsets["Ban"]] != "" and firstp[sett.questionOffsets["Ban"]] == secondp[sett.questionOffsets["Ban"]]:
                together += 100000
    #International students
    if sett.internationalSt == False and firstp[sett.questionOffsets["Slovak"]] == "N" and secondp[sett.questionOffsets["Slovak"]] == "N":
        together += 10000
    #MixedHalls 
    if sett.mixedhalls == True:
        if firstp[sett.questionOffsets["Mixed"]] == "Y" and secondp[sett.questionOffsets["Mixed"]] == "NN" :
            together += 100000
        if firstp[sett.questionOffsets["Mixed"]] == "NN" and secondp[sett.questionOffsets["Mixed"]] == "Y":
            together += 100000
    #New students pairing halls
    if sett.newStudentsMixedHall == True:
        if firstp[sett.questionOffsets["Mixed"]] == "NN" and secondp[sett.questionOffsets["Mixed"]] == "NN":
            together += 100000
        if firstp[sett.questionOffsets["Mixed"]] == "NY" and secondp[sett.questionOffsets["Mixed"]] == "NN":
            together += 100000
        if firstp[sett.questionOffsets["Mixed"]] == "NN" and secondp[sett.questionOffsets["Mixed"]] == "NY":
            together += 100000
    #Old students hall
    if sett.oldStudentsHall == True:
            if firstp[sett.questionOffsets["Hall"]] != "" and secondp[sett.questionOffsets["Hall"]] != "" and firstp[sett.questionOffsets["Hall"]] != secondp[sett.questionOffsets["Hall"]]:
                together += 100000
    return  together


def outputEditor(output, getSumOutOfAlgo = False):
    """
    1. Arg - Output from the Hungarian Algorithm or Blossoms algorithm
    2. Arg - If true the program will pass the sum output from the algorithm
    Alligns the numbers with the real PID numbers.
    Outputs [[0,1,2],[4,5,6]]
    """
    if sett.usedBlossom == False:
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
        return [oldRtrnList, rtnrList2]
    ####
    if sett.usedBlossom == True:
        if getSumOutOfAlgo == True:
            makeLog("LOG","outputEditor()",f"Can not return getSumOutOfAlgo because sett.usedBlossom = {sett.usedBlossom}", True)
        retrnList = []
        a = list(sett.matrix.keys())    #Outside
        b = list(sett.matrix[a[0]].keys()) #Inside
        allMembers = []
        #For loop 1, a
        for mem in range(len(a)):
            if a[mem] in allMembers:
                continue
            allMembers.append(a[mem])
        #For loop 2, b
        for mem in range(len(b)):
            if b[mem] in allMembers:
                continue
            allMembers.append(b[mem])
        finalList = []
        for num in range(len(output)):
            if output[num] in allMembers or num in allMembers:
                if output[num] == 77777:
                    finalList.append([num+1, "- alone", sett.matrix[output[num]][num]])
                    allMembers.remove(num)
                    allMembers.remove(output[num])
                    continue
                finalList.append([num+1, output[num]+1, sett.matrix[output[num]][num]])
                allMembers.remove(num)
                allMembers.remove(output[num])
        return [finalList,[]]
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
    namesDict = {}
    storingDic = {}
    for lists11 in range(len(group1Listt)):            #First for loop
            for listss in range(len(group2Listt)):     #Second for loop
                #Same person penalty
                if group1Listt[lists11] == group2Listt[listss]:
                    exe = 100000
                #Dummy member

                elif dummyMember != False and (dummyMember == group1Listt[lists11] or dummyMember == group2Listt[listss]):
                    if dummyMember == group1Listt[lists11] or dummyMember == group2Listt[listss]:
                        if dummyMember == group1Listt[lists11] and dummyMember == group2Listt[listss]:
                            exe = 100000
                        elif sett.dummyMember == True:
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
                #Smaller group same matching - always
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
def blossomTranslator(dictt = None):
    """
    1. Arg - Dictionary
    - Used to translate dictoniaries that will be the input for the blossom algorithm.
    """
    if dictt == None:
        makeLog("FERR", "blossomTranslator()", "No argument was passed")
    makeLog("LOG","blossomTranslator()", "Using the blossom algorithm")
    dictOutKeys = list(dictt.keys())                 #These are the outside keys {_0_ : {AA : AA}}
    dictInKeys = list(dictt[dictOutKeys[0]].keys())  #These are the inside keys  {0 : {_AA_ : AA}}
    appendList = []
    used = []
    for num in range(len(dictOutKeys)):                      #Lenght of all the outside keys()
        for num2 in range(len(dictInKeys)):                  #Lenght of all the inside keys()
            if dictOutKeys[num] in used or dictInKeys[num2] in used:
                continue
            if dictOutKeys[num] == dictInKeys[num2]:
                continue
            c1 = list(dictt[dictOutKeys[num]].values())
            a = tuple((dictOutKeys[num], dictInKeys[num2], 0 - c1[num2]))
            appendList.append(a)
            if num2 == len(dictInKeys) - 1:
                used.append(dictOutKeys[num])

    sett.matrix = dictt
    sett.usedBlossom = True
    makeLog("LOG","blossomTranslator()", "Triangular matrix created")
    abc = blossom.maxWeightMatching(appendList, True)
    makeLog("LOG","blossomTranslator()", "Blossom matching created")
    return abc.copy()

def dictTranslator(dictt):
    """
    1. Arg - DictOfDicts
    Translates the old form of dictonaries into the appropriate ListsOfLists format.
    """
    sett.matrix = dictt
    sett.dictionary = dictt
    ####
    mainList = []
    for x in list(dictt.values()):
        mainList.append(list(x.values()))
    #
    for number in range(len(mainList)):
        for number2 in range(len(mainList[number])):
            mainList[number][number2] = 0 - mainList[number][number2]
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
    #Dominance
    dictOut = unevenAlgorithm(list1,list2)
    if type(dictOut) == dict:
        dictOut = blossomTranslator(dictOut)
    return dictOut

def evenAlgo(group1List, group2List, dummyMember = False): 
    namesDict = {}
    storingDic = {}
    for lists1 in range(len(group1List)):
        for lists in range(len(group1List)):
            if dummyMember == True:
                #Same member
                if 77777 == group1List[lists1] or 77777 == group2List[lists]:
                    exe = 0
                else:
                    exe = allCategories(group1List[lists1], group2List[lists])
            else:
                exe = allCategories(group1List[lists1], group2List[lists])
            storingDic.update({group2List[lists] : int(exe)})
            if lists == (len(group1List)-1):
                namesDict.update({group1List[lists1] : storingDic})
                storingDic = {}
    return namesDict                 #Returns dict


def groupMaker(group1, group2):
    """
    Making the groups of people, inputs two strings (Names of the groups)
    """
    group1List = []
    group2List = []

    for group in range(numberOfParticipants()):
        if lookForData("Group", group) == group1:
            group1List.append(group)
            sett.dictOfNames.update({group : lookForData(sett.questionOffsets["Name ID"], group)})
        elif lookForData("Group", group) == group2:
            group2List.append(group)
            sett.dictOfNames.update({group : lookForData(sett.questionOffsets["Name ID"], group)})
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
            sett.dummyMember = 77777
            group1List.append(77777)
        else:
            sett.dummyMember = 77777
            group2List.append(77777)
        return evenAlgo(group1List, group2List, True)
    #
    else:
        makeLog("LOG", "groupMaker()", f"unevenUnevenAlgo() was called because the number of participants is not even: {abs(len(group1List) - len(group2List))}")
        sett.uneven = True
        sett.usedBlossom = True
        rtrn = unevenUnevenAlgo(group1List,group2List)
        return rtrn

def finalOut(outcome):
    """
    Final output system, edits the output and puts it into groups, input should be the output from the algorithm
    """
    print()
    time_convert(sett.endTime - sett.startTime)                                             #Prints out the time it took
    print()
    try:
        f = open("roommates.txt","w")
    except PermissionError:
        makeLog("FERR", "finalOut()", "PermissionError - Program can not access roommates.txt. Try to turn off your txt editor")
    try:
        s = open("roommates.csv", "w")
    except PermissionError:
        makeLog("FERR", "finalOut()", "PermissionError - Program can not access roommates.csv file. Try to turn off Excel...")
    s.write('"Room number" "Member 1" "Member 2" "Weight" "Total Weight"\n')
    d = datetime.now().strftime("%d/%B/%Y - %H:%M:%S")
    f.write(f"[{d}] \n")
    #
    out = outputEditor(outcome)
    price = 0
    price1 = 0
    if sett.usedBlossom == True:
        print("--- Matching 1 --- Edmond's Blossom algorithm ---")
        f.write("--- Matching 1 --- Edmond's Blossom algorithm ---\n")
    else:
        print("--- Matching 1 --- Hungarian algorithm ---")
        f.write("--- Matching 1 --- Hungarian algorithm ---\n")
    #s for csv
    #f for the output document
    if sett.usedBlossom:
        numberParticipants = len(out[0])
    else:
        numberParticipants = len(out[0]) - 1
    for a in range(int(numberParticipants)):#Prints out by rooms -- -1 because the value is attached
        price += abs(out[0][a][2])
        if out[0][a][1] == "- alone":
            print("Room {}: {} - alone".format(a+1, sett.dictOfNames[out[0][a][0] - 1], out[0][a][1]))
            try:
                f.write("Room {}: {} -alone \n".format(a+1, sett.dictOfNames[out[0][a][0] - 1], out[0][a][1]))
                s.write(f'{a+1} {sett.dictOfNames[out[0][a][0] - 1]} {"alone"} {""}\n')
            except UnicodeEncodeError:
                f.write("Room {}: {} -alone \n".format(a+1, bytes(sett.dictOfNames[out[0][a][0] - 1], "ascii", "replace").decode("ascii", "replace"), out[0][a][1]))
                s.write(f'{a+1} {bytes(sett.dictOfNames[out[0][a][0] - 1],"ascii", "replace").decode("ascii","replace")} {"alone"} {""}\n')
            continue
        print("Room {}: {}, {} with a pair-value {}".format(a+1, sett.dictOfNames[out[0][a][0] - 1], sett.dictOfNames[out[0][a][1] - 1], abs(out[0][a][2])))
        try:
            s.write(f'{a+1} {sett.dictOfNames[out[0][a][0] - 1]} {str((sett.dictOfNames[out[0][a][1] - 1]))} {abs(out[0][a][2])}\n')
            f.write("Room {}: {}, {} with a pair-value {} \n".format(a+1, sett.dictOfNames[out[0][a][0] - 1], sett.dictOfNames[out[0][a][1] - 1], abs(out[0][a][2])))
        except UnicodeEncodeError:
            makeLog("LOG","finalOut()", "Unicode error detected")
            s.write(f'{a+1} {bytes(sett.dictOfNames[out[0][a][0] - 1], "ascii", "replace").decode("ascii","replace")} {bytes(sett.dictOfNames[out[0][a][1] - 1], "ascii", "replace").decode("ascii","replace")} {abs(out[0][a][2])}\n')
            f.write("Room {}: {}, {} with a pair-value {} \n".format(a+1, bytes(sett.dictOfNames[out[0][a][0] - 1], "ascii", "replace").decode("ascii","replace"), bytes(sett.dictOfNames[out[0][a][1] - 1],"ascii", "replace").decode("ascii","replace"), abs(out[0][a][2])))
    makeLog("LOG", "finalOut()","Matching 1 ... OK")
    ###########################
    makeLog("LOG", "finalOut()",f"Price 1: {price}")
    f.write(f"\nThe total sum is: {price}")
    print(f"\nThe sum is: {price}")
    s.write(f'"" "" "" "" {price }')
    #
    path = os.getcwd() + r"\roommates.txt"
    path1 = os.getcwd() + r"\roommates.csv"
    print(f"\nFile roommates.csv was created! It can be found here: {path1}")
    print(f"File roommates.txt was created! It can be found here: {path}\n")
    makeLog("LOG", "finalOut", f"File roommates.txt was created! It can be found here: {path}", False)
    makeLog("LOG", "finalOut", f"File roommates.csv was created! It can be found here: {path1}")
    f.write("\n\n-- Matrix Dump --\n")
    f.write(str(sett.matrix))
    makeLog("LOG", "finalOut()", "Matrix dump ... OK")
    f.close()
    s.close()

def fileLoader():
    print("\n\nSearching for 'matrix.txt'")
    inputFile = "matrix.txt"
    try:
        f = open(inputFile)
        makeLog("LOG", "fileLoader()", "matrix.txt found")
        print("Found!\n")
        time.sleep(2)
    except FileNotFoundError:
        print("Not found!\n")
        makeLog("ERR", "fileLoader()", "matrix.txt , user input required")
        inputFile = str(input("What is the name of the matrix file? [str] "))
        print("\n")
        try:
            f = open(inputFile)
        except FileNotFoundError:
            makeLog("FERR", "fileLoader()", f"File not found, user input: {inputFile}")
    finally:
        #Loading the data from the file
        string = f.read()
        f.close()
        try:
            dictionary = eval(string)
        except ValueError:
            makeLog("FERR", "fileLoader()", "Matrix.txt could not be loaded. Try to paste the code again or change editors")
        #Saves
        sett.dictionary = dictionary
        sett.matrix = dictionary
        #Saves
        #sett.dictOfNames.update({group : lookForData(sett.questionOffsets["Name ID"], group)})
        #
        a = list(dictionary.keys())
        b = list(dictionary[a[0]].keys())
        #Saving the members in the dictOfNames
        #Outer list
        #####
        for num in range(len(a)):
            sett.dictOfNames.update({a[num] : a[num]})
        #Inner
        for num in range(len(b)):
            sett.dictOfNames.update({b[num] : b[num]})
        makeLog("LOG","fileLoader()", "Matrix loaded, file handler closed, data loaded into variables")
        ########
    print("\nWhich algorithm would you like to use?")
    print("1. Hungarian algorithm, (||G1|-|G2||<=1)")
    print("2. Edmond's Blossom algorithm (|G1|-|G2||>1)")
    try:
        new = int(input("\n[1,2] "))
    except ValueError:
        makeLog("FERR", "fileLoader()", "Invalid user input, [1,2]")
    if new == 1: #Hungarian Algorithm
        makeLog("LOG", "fileLoader()", "Continuing with Hungarian Algorithm")
        group1 = dictTranslator(dictionary)
        matcher = km.KMMatcher(group1)
        outcome = matcher.solve(verbose=True)
        finalOut(outcome)
    else:        #Blossom algorithm
        makeLog("LOG", "fileLoader()", "Continuing with Edmond's Blossom algorithm")
        outcome = blossomTranslator(dictionary)
        finalOut(outcome)
        pass
    #End of this branch
    input("Press enter to exit!")
    makeLog("LOG","exit","Program has exited with code 0")
    exit(0)
def announceData():
    #print("\nVersion: {} \n".format(sett.version))
    print("Number of registered participants: {}".format(numberOfParticipants()))
    print("Number of registered questions: {} \n".format(len(getAllList())))
    #makeLog("LOG", "STARTUP", f"Version: {sett.version}")
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
    makeLog("LOG","announceSettings()", f" It is not allowed for 2 international students to be roommates: {bool(1-sett.internationalSt)}")
    #
    print(f"2. Already assigned halls will be taken into into account: {sett.oldStudentsHall} \n")
    makeLog("LOG","announceSettings()", f"Already assigned halls will be taken into into account: {sett.oldStudentsHall}")
    #
    print(f"3. Hall of preferred sex will be taken into account: {sett.mixedhalls} \n")
    makeLog("LOG", "announceSettings()", f"Hall of preferred sex will be taken into account: {sett.mixedhalls}")
    #
    print(f"4. 2 RAs can not be roommates: {sett.raBan} \n")
    makeLog("LOG", "announceSettings()", f"2 RAs can not be roommates: {sett.raBan}")
    #
    print(f"5. Roommate bans will be taken into account: {sett.memberBans} \n")
    makeLog("LOG", "announceSettings()", f"Roommate bans will be taken into account: {sett.memberBans}")
    #
    print(f"6. Roommate antibans will be taken into account: {sett.memberAntiban} \n")
    makeLog("LOG", "announceSettings()", f"Roommate antibans will be taken into account: {sett.memberAntiban}")
    #
    print(f"7. Dummy roommate matched to bigger group: {sett.dummyMember} \n")
    makeLog("LOG", "announceSettings()", f"Dummy roommate matched to bigger group: {sett.dummyMember}")
    #newStudentsMixedHall
    print(f"8. New students only matched together if OK with mixed hall: {sett.newStudentsMixedHall} \n")
    makeLog("LOG", "announceSettings()", f"New students only matched together if OK with mixed hall: {sett.newStudentsMixedHall}")

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
            cin = input("Please select the question you want to edit [1,2,3,4,5,6,7,8] ")
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
                new = input("Roommate antibans will be taken into account: [true,false] ")
                if str(new) == "true" or str(new) == "True":
                    new = True
                elif str(new) == "false" or str(new) == "False":
                    new = False
                else:
                    makeLog("ERR", "setSettings()", f"cin==6 User input was invalid: {new}")
                    print("Input was invalid!")
                    time.sleep(1)
                    continue
                sett.memberAntiban = new
                setSettings()
                return
            if cin == 7:
                new = input("Dummy roommate matched to bigger group: [true,false] ")
                if str(new) == "true" or str(new) == "True":
                    new = True
                elif str(new) == "false" or str(new) == "False":
                    new = False
                else:
                    makeLog("ERR", "setSettings()", f"cin==7 User input was invalid: {new}")
                    print("Input was invalid!")
                    time.sleep(1)
                    continue
                sett.dummyMember = new
                setSettings()
                return
            if cin == 8:
                new = input("New students only matched together if OK with mixed hall: [true, false] ")
                if str(new) == "true" or str(new) == "True":
                    new = True
                elif str(new) == "false" or str(new) == "False":
                    new = False
                else:
                    makeLog("ERR", "setSettings()", f"cin==8 User input was invalid: {new}")
                    print("Input was invalid!")
                    time.sleep(1)
                    continue
                sett.newStudentsMixedHall = new
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
    print(f"\nVersion: {sett.version}\n")
    makeLog("LOG", "STARTUP", f"Version: {sett.version}")
    try:
        startChoose = int(input("1. Do you want to load an .xls file?\n2. Do you want to load an already created matrix?\n[1/2] "))
    except ValueError:
        makeLog("FERR", "runtime()", "Invalid user input, int needed [1/2]")
    if startChoose == 1: 
        start()
        sett.allOptionsList = getAllList()
        announceData()
        print("\n\n")
        print("Which groups should be used! eg. F3, F4")
        fg = input("Group one: ")
        sg = input("Group two: ")
        makeLog("LOG", "input Groups",f"Group 1: {fg}, Second Group: {sg}")
        setSettings()
        sett.startTime = time.time()   
        out = groupMaker(fg, sg)
        if sett.usedBlossom == False:  #In case that the evenAlgo was used
            group1 = dictTranslator(out)
            matcher = km.KMMatcher(group1)
            outcome = matcher.solve(verbose=True)
        else: #Blossom output
            outcome = out
    #
    elif startChoose == 2:   #In case fileloader is used
        out = fileLoader()
    else:
        makeLog("FERR", "startChoose", f"Invalid input, input: {startChoose}")                                                              #Start of stopwatch                                                                  #End of stopwatch
    sett.endTime = time.time() 
    finalOut(outcome)                                                                       #Final string editing 
    input("Press enter to exit!")
    makeLog("LOG","exit","Program has exited with code 0")
    exit(0)

if __name__ == "__main__":
    runtime()
