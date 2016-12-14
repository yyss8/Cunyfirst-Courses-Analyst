
"""
@author: Group B
"""

import urllib
import http.cookiejar
from bs4 import BeautifulSoup

class classes(object):
    def __inti__(self,title,time,room,professor,clsCode,clsCdt):
        self.title = title
        self.time = time
        self.room = room
        self.professor = professor
        self.clsCode = clsCode
        self.clsCdt = clsCdt

class loadData(object):
        
    cook=http.cookiejar.CookieJar() 
    global openner
    openner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cook)) 
    openner.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]     
    #header
    
    def __inti__(self,userID,pw,optID,optPW):
        self.id = userID 
        self.pw = pw
        self.optID = optID
        self.optPW = optPW
        
    def load(self):
        #cunyfirst login 
        loginId = self.id
        password = self.pw
        logUrl="https://home.cunyfirst.cuny.edu/access/dummy.cgi?login=%s&password=%s&submit.x=0&submit.y=0"%(loginId,password)  
        r=openner.open(logUrl)
        if 'Student Center' not in str(r.read()): #check if login succeed
            return False
        else:return True
        
    def optLoad(self):
        #cuny portal login, used only if cunyfirst is maintaining
        loginId = self.optID
        password = self.optPW
        logUrl = "https://myinfo.cuny.edu/cflitedummy.cgi?login=%s&password=%s&submit.x=0&submit.y=0&submit=Submit"%(loginId,password)
        r=openner.open(logUrl)
        if 'to CUNYfirst MyInfo' not in str(r.read()): #check if login succeed
            return False
        else:return True
        
    def loadClass(self,semster):
        #read class
        self.totalCdt = 0 #total credit counter
        content=openner.open('https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ACAD_CAREER=UGRD&EMPLID=000000000&INSTITUTION=BAR01&STRM=%s'%(semster))       
        soup = BeautifulSoup(content.read(),'lxml')
        clsArray = []
        
        for i in range(0,10): 
            #search class data
            cls = classes()
            clsCode = "E_CLASS_NAME$" + str(i) #search class
            clsContent = soup.find(id=clsCode)
            if str(clsContent) == 'None': #break from loop if there is no more class or invalid information
                continue
            else:
                rmCode = "DERIVED_REGFRM1_SSR_MTG_LOC_LONG$161$$" + str(i)
                timeCode = "DERIVED_REGFRM1_SSR_MTG_SCHED_LONG$160$$" + str(i) 
                nameCode = "E_CLASS_DESCR$" + str(i)
                profCode = "DERIVED_REGFRM1_SSR_INSTR_LONG$162$$" + str(i)
                creditCode = "STDNT_ENRL_SSVW_UNT_TAKEN$" + str(i)
                rmContent = soup.find(id=rmCode) #course room
                timeContent = soup.find(id=timeCode) #course time
                nameContent = soup.find(id=nameCode) #course name
                profContent = soup.find(id=profCode) #course professor
                creditContent = soup.find(id=creditCode) #course credit
      
                cls.clsCode = clsContent.contents[0]
                cls.time = timeContent.contents[0]
                cls.title = nameContent.contents[0]
                cls.professor = profContent.contents[0]
                cls.room = rmContent.contents[0]
                try:
                    #preventing from reading empty space into array
                    self.totalCdt += float(str(creditContent.contents[0]))
                    cls.clsCdt = float(str(creditContent.contents[0]))
                except ValueError:
                    self.totalCdt += 0
                    cls.clsCdt = 0.00
                clsArray.append(cls)
            
        return clsArray
            
    def optGetTermNum(self):
        """
        
        Read the list of term code from MyInfo into a dict
        Returns the term code that user selects
        
        """
        content=openner.open('https://myinfo.cuny.edu/cfalternate/CFAltController?param_schedule=push')
        soup = BeautifulSoup(content.read(),'lxml')
        terms = soup.find_all(id = "type_term") #get the list of term code
        termDict = {}
        termCounter = 1 
        for i in range(0,len(terms[0])):
            try:
                print(str(i + 1) + " - " + str(terms[0].contents[termCounter].contents[0]))
                termDict[str(i + 1)] = str(terms[0].contents[termCounter].get("value"))                
                termCounter +=2
            except IndexError: #break from loop if there is no more term 
                break
        
        userResp = input("Select the term that you want to check: ")
        return termDict[userResp]

    
    def optLoadCls(self):
        #read class from cuny portal MyInfo
        self.totalCdt = 0 # total credit counter
        term = self.optGetTermNum() # get term code
        
        content=openner.open('https://myinfo.cuny.edu/cfalternate/CFAltController?param_schedule=push&type_term_dropdown=%s'%(term))
        soup = BeautifulSoup(content.read(),'lxml')
        clsArray = []
        """
        
        Since there is no unique ID for each class data
        table width is used to sepearte the data
        there might errors for showing the classes from the college other than Baruch
        
        """
        clsTitle = soup.find_all("td",width="1000")
        cdt = soup.find_all("td",width="60")
        professor = soup.find_all("td",width="160")
        timeNRm = soup.find_all("td",width="250")
        
        #counter field
        rmCounter = 3
        tmCounter = 2
        titleCounter = 1
        cdCounter = 0
        b = 1
        
        for i in range(0,len(professor)):
            try:
                cls = classes()
                title = clsTitle[titleCounter].contents[0].contents[0] #get course title
                title_split = title.split('-',1) #seperate title into class code and course name
                cls.clsCode = title_split[0][1:len(title_split[0])-1] #get class code
                cls.title = title_split[1][1:len(title_split[1])] #get courses name
                cls.professor = professor[b].contents[0] #get course instructor
                cls.time = timeNRm[tmCounter].contents[0] #get course time
                cls.room = timeNRm[rmCounter].contents[0] #get course room number
                cls.clsCdt = cdt[cdCounter].contents[0][2:len(cdt[cdCounter].contents[0])-1] #get course credit
                self.totalCdt += int(cls.clsCdt[0])  
                
                clsArray.append(cls)
                
                #counters 
                b+= 2
                titleCounter+=1
                rmCounter += 4
                tmCounter += 4
                cdCounter += 1
            except IndexError:
                break #break from loop if there is no more class
            
        return clsArray
        

    def loadAccIqy(self):
        #get account inquiry page
        content = openner.open('https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_ACCT_SUMM.GBL?Page=SSF_SS_ACCT_SUMM&Action=U')
        soup = BeautifulSoup(content.read(),'lxml') 
        
        furDue = soup.find(id = 'SSF_SS_DERIVED_SSF_AMOUNT_TOTAL3') #get future due
        curDue = soup.find(id = 'SSF_SS_DERIVED_SSF_AMOUNT_TOTAL2') #get current due
        self.furDue = furDue.contents[0]
        self.curDue = curDue.contents[0]
        #return total current and future due amount
        self.smtName = []
        self.smtDue = []
        self.pendingPmt = []
        self.pendingFafsa = []
        self.totalDue = []

        for i in range (0,4):
            smtCode = "TERM$" + str(i)
            smtName = soup.find(id=smtCode) #search semster
            if str(smtName) == 'None': #break from loop if there is no more class or invalid information
                break
            elif str(smtName.contents[0]) == "Total": #remove total from the array
                break
            else:
                dueCode = "SSF_SS_DERIVED_SSF_TOTAL_CHRGS$" + str(i)
                pdPmtCode = "PAYMENTS$" + str(i)
                fafsaCode = "FA$" + str(i)
                totalCode = "SSF_SS_DERIVED_SSF_TOTAL_DUE$" + str(i)
                dueContent = soup.find(id = dueCode) #semster due amount
                pdPmtContent = soup.find(id=pdPmtCode) #pending charge
                fafsaContent = soup.find(id=fafsaCode) #pending finanical aid
                totalContent = soup.find(id=totalCode) #total due amount
                
                self.smtName.append(smtName.contents[0])
                self.smtDue.append(dueContent.contents[0])
                try: #null check
                    if float(pdPmtContent.contents[0]):
                        self.pendingPmt.append(pdPmtContent.contents[0])
                except ValueError:
                    self.pendingPmt.append(str(0.00))
                try: #null check
                    if float(fafsaContent.contents[0]):
                        self.pendingFafsa.append(fafsaContent.contents[0])
                except ValueError:
                    self.pendingFafsa.append(str(0.00))
                self.totalDue.append(totalContent.contents[0])
                
        if self.smtName == []:
            return False
        else: return True
        
    def loadDueTime(self):
        #get due time page        
        content = openner.open('https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_CHRGS_DUE.GBL?Page=SSF_SS_CHRGS_DUE&')
        soup = BeautifulSoup(content.read(),'lxml')
        
        self.dueTime = []
        self.dueDateAmount = []

        for i in range (0,5):
            dtCode = "DERIVED_SF_2_SF_DUE_DATE_DISP$" + str(i)
            dueDateContent = soup.find(id=dtCode) #get due date
            if str(dueDateContent) == 'None': #break from loop if there is no more class or invalid information
                break
            else:
                raCode = "DERIVED_SF_2_SF_RUNNING_TOTAL$" + str(i) #get total dued amount
                amountContent = soup.find(id=raCode)
                self.dueTime.append(dueDateContent.contents[0])
                self.dueDateAmount.append(amountContent.contents[0])
        if self.dueTime == []:
            return False
        else: return True
          
    def logOut(self):
        #log out from cunyfirst
        openner.open('https://home.cunyfirst.cuny.edu/oam/logout.html')
        
    def optLogout(self):
        #log out from cuny portal MyInfo
        openner.open('https://myinfo.cuny.edu/cfalternate/_logout.jsp')