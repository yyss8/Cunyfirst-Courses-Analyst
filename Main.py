from load import loadData
from Search import ClsSearch
import os,csv
from Analyze import Rating

def login():
    #login cunyfirst
    print("")
    print("Please Enter Your Cunyfirst Username and Password to Login The System")
    #declare username and password to be global for class search feature    
    global username 
    global Password    
    username = input("Username: ")
    Password = input("Password: ")
    classData.id = username
    classData.pw = Password
    print("Loading..............")
    loginStatus = classData.load() #login cunyfirst with the username and password that user enters
    return loginStatus

def clsCheck(status):
    #cunyfirst class check feature
    print("1 - Spring 2016")
    print("2 - Summer 2016")
    print("3 - Fall 2016")
    userInput = input("Please select semster: ")
    if userInput == "1":
        clsSemster = "1162"
        smtName = 'Spring 2016'
    elif userInput == "2":
        clsSemster = "1166"
        smtName = 'Summer 2016'
    elif userInput == "3":
        clsSemster = "1169"
        smtName = 'Fall 2016'
    else:
        clsSemster =""
        print("In-correct Input!")

    if clsSemster != "":
        print("-----------Start loading data--------------")
        if status == True:
            cls = classData.loadClass(clsSemster) #preventing empty class array
            if len(cls) != 0:
                print("")
                print("-----Semster: %s Total Class: %s Total Credit: %s -----"%(smtName,str(len(cls)),str(classData.totalCdt)))
                print("")
                print(" %-10s\t%15s\t%26s\t%17s\t%31s\t%15s"%("Class Code","Time","Instructor","Room","Title","Credit"))
                print("===============================================================================================================================================")
                for i in range(0,len(cls)):
                    print("%-10s\t%22s\t%16s\t%17s\t%40s\t%2s"%(cls[i].clsCode,cls[i].time,cls[i].professor,cls[i].room,cls[i].title,str(cls[i].clsCdt)))
                print("")
            else:
                print("No Class Found!")
    else:
        print("Login Failed!")

def optLoginPage():
    #login cuny portal MyInfo to check class schedule if cunyfirst is maintaining
    print("")
    print("Please Enter Your Cuny Portal Username and Password to Login The Optional System")   
    classData.optID = input("Username: ")
    classData.optPW = input("Password: ")
    print("Loading..............")
    loginStatus = classData.optLoad() #login cuny portal
    return loginStatus


def optMenu(status):
    #show MyInfo menu
    stopProg = False
    while (stopProg != True):
        print("")
        print("-------------------------Optional Login Menu---------------------------")
        print("Optional system only supports current enrollment feature at this time!")
        print("1 - Current Enrollment")
        print("2 - Return To Main Menu")
        print("3 - Exit Program")
        userResp = input("Please select the features: ")
        if userResp == "1":
            optClsChk(status)
        elif userResp == "2":
            mainMenu()
            stopProg = True
        elif userResp == "3":
            classData.optLogout()
            stopProg = True
        else:
            print("In-correct Input!")

def optClsChk(status):
    #show class schedule from MyInfo
    if status == True:
        cls = classData.optLoadCls()
        if len(cls) != 0: #preventing empty class array
            print("")
            print("----------Total Class: %s Total Credit: %s ----------"%(str(len(cls)),str(classData.totalCdt)))
            print("")
            print("%-10s\t%13s\t%20s\t%28s\t%41s\t%17s"%("Class Code","Time","Instructor","Room","Title","Credit"))
            print("=======================================================================================================================================================")
            for i in range(0,len(cls)):
                print("%-10s\t%26s\t%11s\t%17s\t%30s\t%6s"%(cls[i].clsCode,cls[i].time,cls[i].professor,cls[i].room,cls[i].title,str(cls[i].clsCdt)))
            print("")
        else:
            print("No Class Found!")

    else:
        print("Login Failed")
    

def mainMenu():
    #show cunyfirst menu
    loginStatus = False
    while (loginStatus != True):
        #loop until login
        loginStatus = login()
        if loginStatus == True:
            print("----------You Have Successfully Logged Into The System-----------")
        else:
            #ask user to try optional login system or try another username or password
            print("")
            print("Login Failed! Do You Want To Use Optional Login Or Try Again?")
            print("1- Optional Login")
            print("2- Try Again")
            print("3- Exit")
            userResp = input("Please select the number: ")
            if userResp == "1":
                #go to cuny portal login page
                optStatus = optLoginPage() 
                
                if optStatus == True:
                    #show Myinfo menu if login succeds
                    optMenu(optStatus)
                else:
                    print("")
                    print("Optional System Login Failed")
                    print("")
                break
            elif userResp == "2":
                #allows user to try another username or password
                continue
            elif userResp == "3":
                #exit program
                break
            else:
                print("In-correct Input!")
            
    if loginStatus == True:
        stopProg = False
        while (stopProg != True):
            print("")
            print("1 - Current Enrollment")
            print("2 - Account Inquiry")
            print("3 - Search Class")
            print("4 - Re-login system")
            print("0 - Exit")
            userResp = input("Please select the features: ")
            print("")
            if userResp == "1":
                clsCheck(loginStatus)
            elif userResp == "4":
                classData.logOut()
                login()
            elif userResp == "2":
                accCheck(loginStatus)
            elif userResp == "0":
                classData.logOut()
                stopProg = True
            elif userResp == "3":
                clsSearch()
            else:
                print("In-correct Input!")

def accCheck(status):
    print("1 - Summary")
    print("2 - Due Date")
    print("")
    userInput = input("Please select number: ")
    if userInput == "1":
        print("-----------Start loading data--------------")
        if status == True:
            accStatus = classData.loadAccIqy()
            if accStatus == True:
                print("")
                print("---------------------Account Summary-------------------")
                print("")
                print("Current Due: " + (str(classData.curDue)))
                print("Future Due: " + (str(classData.furDue)))
                print("")
                print("     Semster \tOutstanding Charge \tPending Payment \tPending Fafsa \tTotal Due")
                print("===========================================================================================")
                for i in range(0,len(classData.smtName)):
                    if classData.pendingPmt[i] == " ":
                        pdAmount = str(0.00)
                    else:pdAmount = classData.pendingPmt
                    if classData.pendingFafsa[i] == " ":
                        pdFafsa = str(0.00)
                    else:pdFafsa = classData.pendingFafsa[i]
                    print(classData.smtName[i] + " \t     " + classData.smtDue[i] + " \t    %s\t\t      %s \t      \t"%(pdAmount[i],pdFafsa[i]) + classData.totalDue[i])
                print("")
            else:print("No Charge Found!")
    elif userInput == "2":
        if status == True:
            accStatus = classData.loadDueTime()
            if accStatus == True: 
                print("")
                print("-------------------Charges Due-------------------")
                print("")
                print("     Due Date \tRunning Total ")
                for i in range(0,len(classData.dueTime)):
                    print("    "+classData.dueTime[i] + " \t   $" + classData.dueDateAmount[i])
                print("")
            else:print("No Due Date Found!")
    else:print("In-correct Input!")        

def clsSearch():
    print("Initializing search features..............")
    search = ClsSearch()
    ClsSearch.id = username
    ClsSearch.pw = Password
    loginStatus = search.login()
    lastMenu = False
    while lastMenu != True:  
        print("")
        print("1- Search One Class")
        print("2- Search All Class")
        print("3- Class Analysis")
        print("4- Back")
        if loginStatus == True:
            ftSelected = input("Please select the features: ")
            if ftSelected != "3" and ftSelected != "4": #Initialize search feature for first two options
                collegeList = search.loadCollegeList()
                i = 1
                print("")
                clgSorted = sorted(collegeList)
                for college in clgSorted:
                    print(str(i) + " -  "+ collegeList[college]) 
                    i += 1
                print("")
                clgSelected = input("Please select the college: ")
                search.selectCollege(clgSorted[int(clgSelected) - 1])
                print("")        
                print("1 - Spring 2016")
                print("2 - Summer 2016")
                print("3 - Fall 2016")
                print("")
                smtSelected = input("Please select the semster: ")
                if smtSelected == "1":
                    term = "1162"
                elif smtSelected == "2":
                    term = "1166"
                elif smtSelected == "3":
                    term = "1169"
                else:
                    term = ""
                    print("In-correct Input!")
            
                if term != "":
                    search.loadTerm(term)
                    if ftSelected == "1":
                        search.search_One_Class()
                    elif ftSelected == "2":
                        clsSearchAll(search)
            elif ftSelected == "3":clsAnalyze()
            elif ftSelected == "4":
                lastMenu = True
                search.logOut()
            else:print("In-correct Input!")

def clsSearchAll(search):
    userResp = input("Do you want to include the professor rating in the report file?(y/n) ")
    fileName = input("Please enter a filename you want to save as: ")
    if userResp == "y" or userResp == "Y":
        search.search_All_Class(fileName,getRating = True)
        print("")
    elif userResp == "n" or userResp == "N":
        search.search_All_Class(fileName,getRating = False)
        print("")
    else:print("In-correct Input!")

def clsAnalyze():
    analyze = Rating()
    fileDict = {}
    fileCounter = 1
    for x in os.listdir('.'):
        if os.path.isfile(x) and os.path.splitext(x)[1]=='.csv':
            fileDict[str(fileCounter)] = x            
            print(str(fileCounter) + "- " + x)
            fileCounter += 1
    #get all the csv filenames in current directory
    try:
        if fileDict[str(1)]:
            fileSelected = input("Please select the file number that you want to analyze: ")
            if int(fileSelected) <= len(fileDict):
                   read_file = open(fileDict[fileSelected] ,'r')         
                   stopProg = False
                   while stopProg != True:
                       print("")
                       print("1- General Report")
                       print("2- Compare Rating Between Weekday and Weekend")
                       print("3- Compare Rating Between Different Time Period")
                       print("4- Back")
                       userResp= input("Please select the features: ")
                       if userResp == "1":
                           read_file.seek(0)
                           data = csv.reader(read_file,None)
                           next(data)
                           analyze.report(data)
                       elif userResp == '2':
                           read_file.seek(0)
                           data = csv.reader(read_file,None)
                           next(data)
                           analyze.ratingBetweenWdnWk(data)
                       elif userResp == '3':
                           read_file.seek(0)
                           data = csv.reader(read_file,None)
                           next(data)
                           analyze.ratingByTmRange(data)
                       elif userResp == '4':
                           stopProg = True
                       else:print("In-correct Input!")
                
            else:print("In-correct file number!")
    except KeyError: 
        print("")
        print("No Class Data Found!")
        print("Please generate a class report first by using the search for all classes feature!")


print("---------------------Welcome to CunyFaster---------------------")
classData = loadData() #initialize data
mainMenu()
print("-----------------Thank You For Using CunyFaster----------------")
