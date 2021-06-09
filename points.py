import json, time
import excel2json
from hungarian_algorithm import algorithm
#all the questions here
allOptionsList = ["Group", "Slovak", "Name ID", "Do you prefer to sleep with the window open?", 
"How sensitive are you to the lights being ON while you are sleeping?", "How sensitive are you to sound/noise while you are sleeping?",
"How important is it for you to play music on speaker in your room during the day?", 
"Do you mind if your roommate plays music on speaker in the room during the day?",
"How important is cleanliness & orderliness to you?",
"Do you mind sharing your personal items with your roommate?",
"How often do you use other people's items  (charger, comb, clothing, ...)",
"How important is it for your room to be a QUIET space for just you and your roommate?",
"How often would you like to have friends over?",
"What is the latest you would like to have friends over in your room?",
"What is the latest you would want your roommate to have his/her friends over in the room?",
"Do you prefer to use your room mainly as a sleeping space or as a living space?",
"Do you prefer to have a roommate who spends a lot of time in the room, or mainly just comes to room to sleep?",
"What time do you prefer to sleep?",
"What time do you prefer to wake up?"]
#Creates the JSON files
data = excel2json.convert_from_file('prefs_table.xls')

#For searching in the JSON file ,,,,Name And then the block number
def lookForData(jClass, numberWhere):
    jdata = json.loads(open('Form Responses.json').read())
    try:
        return jdata[numberWhere][jClass]
    except KeyError:
        print("Not existing")
        return False

#Returns all the data that a participant has
def dataForParticipant(number):
    jdata = json.loads(open('Form Responses.json').read())
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

#Lights double, two integers needed 
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
#Here will the data be stored

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
    #Need to add a check for len of lists
    for lists1 in range(len(group1List)):
        for lists in range(len(group1List)):
            exe = allCategories(group1List[lists1], group2List[lists])
            storingDic.update({group2List[lists] : int(exe)})
            if lists == (len(group1List) - 1):
                namesDict.update({group1List[lists1] : storingDic})
                storingDic = {}
    print(namesDict)
    return(namesDict)


try:
    group1 = groupMaker("F3", "F4")
except IndexError:
    print("[ERROR] Number of participants is not matching!")
print(algorithm.find_matching(group1, matching_type = 'min', return_type = 'list'))
print(algorithm.find_matching(group1, matching_type = 'min', return_type = 'total'))
#all the data will be stored here
"""
#Comparing all the people
for member1 in range(80):
    for member2 in range(1,80):
        exe = allCategories(member1, member2)
        storingDic.update({member2 : int(exe)})
        if member2 == 79:
            namesDict.update({member1 : storingDic})
            storingDic = {}
"""   

print("Done")
    

    

    
        


