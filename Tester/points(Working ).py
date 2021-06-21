import json, time, re
import excel2json
from hungarian_algorithm import algorithm
#Start
#Function for reporting errors
def errorMessage(text):
    print("[ERROR] {}".format(text))

#Start -- Name of the EXCEL sheet + The name of the JSON file
#firstExcel = ""
#secondJSON = ""
#TTexcel2json.convert_from_file(str(firstExcel))

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
        errorMessage("File not found!")
        pass

#firstExcel -- Name of the excel file
#secondJSON -- Name of the JSON file

#Handling of the questions -- Giving data to the operator
def getAllList():
    res = json.loads(open(str(secondJSON)).read())
    list = []
    for key in res[0].keys():
        list.append(key)
    print(list)
    input()
    return list



def loadAllQuestions():
    jdata = json.loads(open(secondJSON).read())

#For searching in the JSON file ,,,,Name And then the block number
def lookForData(jClass, numberWhere):
    jdata = json.loads(open(str(secondJSON)).read())
    try:
        return jdata[numberWhere][jClass]
    except KeyError:
        print("Not existing")
        return False

#Returns all the data that a participant has
def dataForParticipant(number):
    jdata = json.loads(open(secondJSON).read())
    data = []
    for i in range(0,18):
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
#These questions are not used anymore

#Lights, double, two integers needed 
def categoryTwo(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[4] - otherP[4]
    if minus < 0:
        minus = minus * (-1)
    return minus * 2
#Sound senstivity, double points, two integers neeeded 
def categoryThree(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[5] - otherP[5]
    if minus < 0:
        minus = minus * (-1)
    return minus * 2

#Speaker music + Playing music, two integers -- Special case
def categoryFourFive(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[7]
    otherPq5 = 6 - otherP[7]
    calc1 = mainP[6] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[6]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2

#Cleanliness orderliness - double, two integers needed 
def categorySix(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[8] - otherP[8]
    if minus < 0:
        minus = minus * (-1)
    return minus * 2
#Sharing of items, reversed special, two ints needed 

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
#Quiet space, reversed special, two ints neeeded 
def categoryNineTen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = 6 - mainP[12]
    otherPq5 = 6 - otherP[12]
    calc1 = mainP[11] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[11]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2

#Friends over, specia but not reversed, two ints are needed  
def categoryElevenTwelve(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[14]
    otherPq5 = otherP[14]
    calc1 = mainP[13] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[13]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2

#Living space, special but not reversed, two ints needed 
def categoryThirteenFourteen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    mainPq5 = mainP[16]
    otherPq5 = otherP[16]
    calc1 = mainP[15] - otherPq5
    if calc1 < 0:
        calc1 = calc1 * (-1)
    calc2 = mainPq5 - otherP[15]
    if calc2 < 0:
        calc2 = calc2 * (-1)
    return calc1 + calc2

#Sleeping, double, two ints
def categoryFifteen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[17] - otherP[17]
    if minus < 0:
        minus = minus * (-1)
    return minus * 2

# Waking up, double, two ints
def categorySixteen(mainParticipant, otherparticipant):
    mainP = dataForParticipant(mainParticipant)
    otherP = dataForParticipant(otherparticipant)
    minus = mainP[17] - otherP[17]
    if minus < 0:
        minus = minus * (-1)
    return minus * 2
#Execution two ints, 
def allCategories(mem1, mem2):
    together = categoryOne(mem1,mem2) + categoryTwo(mem1,mem2) + categoryThree(mem1,mem2) + categoryFourFive(mem1,mem2) + categorySix(mem1,mem2) + categorySevenEight(mem1,mem2) + categoryNineTen(mem1,mem2) + categoryElevenTwelve(mem1,mem2) + categoryThirteenFourteen(mem1,mem2) + categoryFifteen(mem1,mem2) + categorySixteen(mem1,mem2)
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
    for group in range(80):
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
    print(namesDict)
    return(namesDict)



    
#Here the pointing function is called -- For now this is the error handling
try:
    group1 = groupMaker("F3", "F4")
except IndexError:
    print("[ERROR] Number of participants is not matching!")
    time.sleep(3)
    exit()
#Algorithm we are using -- 
outcome = str(algorithm.find_matching(group1, matching_type = 'min', return_type = 'list'))
#Output -- 
print("The output of the algorithm is: {}".format(outcome))
print("Edited so the IDs match: {}".format(outputEditor(outcome)))
