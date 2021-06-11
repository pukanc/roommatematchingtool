import json, time, re
import excel2json
from hungarian_algorithm import algorithm
debug = False

#Debug off == user-mode, Debug on debug
if debug == True:
    firstExcel = "Test.xls"
    secondJSON = "Form Responses.json"
    excel2json.convert_from_file(str(firstExcel))
else:
    while True:
        try:
            if len(firstExcel) == 0:
                #Gettings the name of the Excel file -- Needs to be in xls!!!
                firstExcel = input("What is the name of the of the file? eg. prefs_table.xls    ")
                excel2json.convert_from_file(str(firstExcel))
        
        except NameError:
            firstExcel = input("What is the name of the of the file? eg. prefs_table.xls    ")
            excel2json.convert_from_file(str(firstExcel))
    
            #Input the name of the second JSON file -- Wait and check your folder you should see new JSON files
        secondJSON = input("Check your folder and pick the JSON file you want to use. eg. Form Responses.json    ")
        try:
            jdata = json.loads(open(str(secondJSON)).read())
            break
        except FileNotFoundError:
                pass


#Handling of the questions -- All questions in a list
def getAllList():
    res = json.loads(open(str(secondJSON)).read())
    list = []
    for key in res[0].keys():
        list.append(key)
    return list

#Var for all option that exist -- 
allOptionsList = getAllList()


#For searching in the JSON file -- Name And then the block number
def lookForData(jClass, numberWhere):
    jdata = json.loads(open(str(secondJSON)).read())
    try:
        return jdata[numberWhere][jClass]
    except KeyError:
        print("Not existing")
        return False

#Returns an int, number start with a zero
def numberOfParticipants():
    nOfparticipants = -1
    while True:
        try:
            lookForData("Name ID", nOfparticipants)
        except IndexError:
            break
        nOfparticipants =  nOfparticipants + 1
    return nOfparticipants


#Returns all the data that a participant has
def dataForParticipant(number):
    jdata = json.loads(open(secondJSON).read())
    data = []
    for i in range(0,len(getAllList())):
        data.append(jdata[number][allOptionsList[i]])
    return data
#Window  - Doulbe points - Two integers needed
def categoryOne(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[3] - otherP[3]
    if minus < 0:
        minus = minus * (-1)
    return minus * 2

#Speaker music + Playing music, two integers -- Special case
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

#Cleanliness orderliness - double, two integers needed 
def categoryFour(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[6] - otherP[6]
    if minus < 0:
        minus = minus * (-1)
    return minus * 2

#Sharing of items, reversed special, two ints needed 
def categoryFiveSix(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[8]
    otherPq5 = 6 - otherP[8]
    calc1 = mainP[7] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[7]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2
#Quiet space, reversed special, two ints neeeded 
def categorySevenEight(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[10]
    otherPq5 = 6 - otherP[10]
    calc1 = mainP[9] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[9]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2

#Friends over, specia but not reversed, two ints are needed  
def categoryNineTen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[12]
    otherPq5 = otherP[12]
    calc1 = mainP[11] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[11]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2

#Living space, special but not reversed, two ints needed 
def categoryElevenTwelve(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[14]
    otherPq5 = otherP [14]
    calc1 = mainP[13] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[13]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2

#Sleeping, special alogorithm
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

#Execution two ints, 
def allCategories(mem1, mem2):
    together = categoryOne(mem1,mem2) + categoryTwoThree(mem1,mem2) + categoryFour(mem1,mem2) + categoryFiveSix(mem1,mem2) + categorySevenEight(mem1,mem2) +categoryNineTen(mem1,mem2) + categoryElevenTwelve(mem1,mem2) + categoryThirteenFourteen(mem1,mem2)
    return together*together


#Edits the output, adds 1 to the members ID so they allign with the JSON -- 
def outputEditor(output):
    outcome1 = re.findall("\d+", output)
    outcome2 = [int(i) for i in outcome1]
    for a in range(2,len(outcome2),3):
        outcome2[a] -= 1
    for a in range(0,len(outcome2)):
        outcome2[a] += 1
    return outcome2



#Making the groups of people, inputs two strings (Names of the groups)
def groupMaker(group1, group2):
    namesDict = {}
    storingDic = {}
    group1List = []
    group2List = []
    for group in range(numberOfParticipants()):
        if lookForData("Group", group) == group1:
            group1List.append(int(lookForData("Name ID", group) - 1))
        elif lookForData("Group", group) == group2:
            group2List.append(int(lookForData("Name ID", group) - 1))
    #Need to add a check for len of list here --- Error handling needs to be added
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
    print(" ")
    print(" ")
    list1 = outputEditor(outcome)
    for rem in range(2,int(len(list1)/2), 2):
        del list1[rem]
    rommno = 0
    add = 0
    nList = []
    print("The output of the algorithm is: {}".format(outcome))
    print("IDS matching {}".format(list1))
    print()
    for rem in range(int(len(list1)/2)):
        rommno += 1
        nList.clear()
        nList.append(list1[add])
        nList.append(list1[add+1])
        add += 2
        print("Room {}: {}, {}".format(rommno, nList[0], nList[1]))

#Print out all participants and questions --
def announceData():
    print("Number of registered participants: {}".format(numberOfParticipants()))
    print("Number of registered questions: {}".format(len(getAllList())))



    

#Announces data
announceData()
time.sleep(2)
#Input groups
print("Which groups should be used! eg. F3, F4")
fg = input("Group one: ")
sg = input("Group two: ")
group1 = groupMaker(fg, sg)
#Algorithm we are using -- 
outcome = str(algorithm.find_matching(group1, matching_type = 'min', return_type = 'list'))
#Output
finalOut(outcome)
