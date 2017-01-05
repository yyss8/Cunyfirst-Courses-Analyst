from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import TimeoutException    
import datetime

class ClsSearch(object):
    
    def __inti__ (self,loginID,password,browser):
        self.id = loginID
        self.pw = password
        
    def login(self):
        #login cunyfirst
        global browser
        
        #browser field
        browser = webdriver.PhantomJS()
        #browser = webdriver.Firefox()
        #browser = webdriver.Chrome()
        
        loginId = self.id
        password = self.pw
        browser.get('https://home.cunyfirst.cuny.edu/oam/Portal_Login1.html')
        browser.find_element_by_id('cf-login').send_keys(loginId)
        browser.find_element_by_id('password').send_keys(password)
        browser.find_element_by_name('submit').click()
        if browser.find_element_by_id('crefli_HC_SSS_STUDENT_CENTER'):
            #return login status
            return True
        else:
            return False
    
    def getAjaxData(self,name):
        """
        
        returns JS data from ratemyprofessor.com
       
        """
        s = requests.Session()
        linkOne = "http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=10&callback=jQuery111007111421867084096_1461087056539&q=%s"%(name)
        linkTwo = "AND+schoolid_s%3A222&defType=edismax&qf=teacherfullname_t%5E1000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s"
        requestLink = linkOne + linkTwo
        request_JS = s.get(requestLink)
        return request_JS.text    
    
    def loadCollegeList(self):
        """
        
        returns a dict of college list
        {college code: college name}
       
        """
        clgList = {}       
        browser.get('https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL')
        findCollege = browser.find_element_by_id('CLASS_SRCH_WRK2_INSTITUTION$31$')       
        options = [x for x in findCollege.find_elements_by_tag_name("option")]        
        for college in options:
            clgList[college.get_attribute("value")] = college.text
        del(clgList[""]) # remove empty option from dict
        return clgList
        
    def selectCollege(self,college):
        browser.find_element_by_xpath("//option[@value='%s']"%(college)).click()
        
    def loadClsList(self):
        """
        
        return an array of subject list 
        since available subject might be different for each semster, 
        a new subject list has to be generated everytime the term option is modified.
        
        """        
        #wait until ajax data is loaded
        WebDriverWait(browser, 10).until(lambda browser: Select(browser.find_element_by_id('CLASS_SRCH_WRK2_INSTITUTION$31$')).first_selected_option.text)
        subList = []
        subChosen = browser.find_element_by_id('SSR_CLSRCH_WRK_SUBJECT_SRCH$0')
        options = [x for x in subChosen.find_elements_by_tag_name("option")]
        for subject in options:
            subList.append(subject.get_attribute("value"))
        del(subList[0]) # remove empty subject from array
        return subList
    
    def get_Rating(self,profName):
        #return instructor rating
        getRating = "No Rating"    
        prof_Name = ''
        if profName != "Staff":
            profName_split = profName.split(' ')
            for name in profName_split:
                prof_Name += name + '+'
            data = self.getAjaxData(prof_Name)
            data_split = data.split("\n")
            for item in data_split:    
                if "averageratingscore_rf" in item:
                    Rating = item.split(":")
                    getRating = Rating[1][:-2]
        
        return getRating
    
    def loadTerm(self,term):
        """
        
        selects semester by term code
        
        """  
        WebDriverWait(browser, 10).until(lambda browser: Select(browser.find_element_by_id('CLASS_SRCH_WRK2_INSTITUTION$31$')).first_selected_option.text)
        #wait until ajax data is loaded        
        getTerm = Select(browser.find_element_by_id('CLASS_SRCH_WRK2_STRM$35$'))
        if term != "1162":
            getTerm.select_by_value(term)
    
    def search_One_Class(self):
        course = input("Please enter the course code that you want to search,e.g.,CIS 5800,ACC 2203: ")
        course_split = course.split(' ')
        sub = course_split[0].upper()
        code = course_split[1]
        print("Start Searching................")
        print("")
        WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_id('SSR_CLSRCH_WRK_SUBJECT_SRCH$0'))
        select = Select(browser.find_element_by_id('SSR_CLSRCH_WRK_SUBJECT_SRCH$0'))
        select.select_by_value(sub) #select subject
        browser.find_element_by_id('SSR_CLSRCH_WRK_CATALOG_NBR$1').send_keys(code) #class code 
        browser.find_element_by_id('SSR_CLSRCH_WRK_SSR_OPEN_ONLY$5').click() #display all class including closed or waiting
        browser.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()        
        try:#wait until page finish loading
            WebDriverWait(browser, 8).until(lambda browser: browser.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH').is_displayed())
        except TimeoutException: #report no class found
            print("No Class Found For This Course")
            
        page_content = browser.page_source
        soup = BeautifulSoup(page_content,'lxml')
        sctNumCounter = 0
        sctCode = "win0divSSR_CLSRSLT_WRK_GROUPBOX2$0"
        clsSectContent = soup.find(id = sctCode)
        
        for n in range (0,50): #some subject might have more than 200+ classes
            clsNumCode = "MTG_CLASS_NBR$" + str(n) 
            clsNum = clsSectContent.find(id = clsNumCode)   
            if clsNum == None:
                break
            else:
                statusCode = "win0divDERIVED_CLSRCH_SSR_STATUS_LONG$" + str(n)
                sectCode = "MTG_CLASSNAME$" + str(n)
                rmCode = "MTG_ROOM$" + str(n)
                profCode = "MTG_INSTR$" + str(n)
                timeCode = "MTG_DAYTIME$" + str(n)
                clsStatus = clsSectContent.find(id = statusCode)
                clsStatus = clsStatus.find('img')
                clsSect = clsSectContent.find(id = sectCode) #get class section
                clsRm = clsSectContent.find(id = rmCode) #get class room
                clsProf = clsSectContent.find(id = profCode) #get class instructor
                clsTime = clsSectContent.find(id = timeCode) #get class time
                sect_split = clsSect.contents[2].split("\n") #get splited class section
                rating = self.get_Rating(clsProf.contents[0])
                print("Course: " + sub + " " + code + "  Course Number: " + clsNum.contents[0] + "  Course Section: " + clsSect.contents[0] + " " + sect_split[1])
                print("Course Time: " + clsTime.contents[0] + "   Course Room: " + clsRm.contents[0])               
                print("Course Instructor: " + clsProf.contents[0] + "   Rating: " + rating + "   Status: " + clsStatus['alt'])                
                print("========================================================================")                
                sctNumCounter += 1                        
                  
        
    def search_All_Class(self,fileName,getRating=None):
        """
        
        returns no data, all the data will be stored in the csv file
        takes two parameter:
        1.the filename that user want to save as
        2.if user wants to include professor rating in the csv file or not(optional)

        
        """  
        sub_List = self.loadClsList()
        write_file = open(fileName+'.csv','w')    
        if getRating ==True:
            write_file.write("Class,Class Number,Class Section,Class Section-B,Class Time,Class Room,Class Instructor,Rating\n")
        else:
            write_file.write("Class,Class Number,Class Section,Class Section-B,Class Time,Class Room,Class Instructor\n")
        
        for sub in sub_List:
            start = datetime.datetime.now() #get start time to calculate time cost for loading each class data   
            sctNumCounter = 0 #class counter
            
            #wait until page finish loading
            WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_id('SSR_CLSRCH_WRK_SUBJECT_SRCH$0'))
    
            select = Select(browser.find_element_by_id('SSR_CLSRCH_WRK_SUBJECT_SRCH$0'))
            select.select_by_value(sub) #select subject
            select = Select(browser.find_element_by_id('SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$1')) 
            select.select_by_value('G') #select 'greater than' option
            browser.find_element_by_id('SSR_CLSRCH_WRK_CATALOG_NBR$1').send_keys('0') #class code 
            browser.find_element_by_id('SSR_CLSRCH_WRK_SSR_OPEN_ONLY$5').click() #display all class including closed or waiting
            browser.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click() #click search button
            
            try:#wait until page finish loading
                WebDriverWait(browser, 8).until(lambda browser: browser.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH').is_displayed())
            except TimeoutException: #select next subject if there is no class found
                print("====Finished Loading " + sub + "====== " + "No Classes Found======")
                continue                
            page_content = browser.page_source
            soup = BeautifulSoup(page_content,'lxml')
            
            for i in range (0,50): 
                sctCode = "win0divSSR_CLSRSLT_WRK_GROUPBOX2$" + str(i)
                sctTitleCode = "win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$" + str(i)
                clsSectContent = soup.find(id = sctCode) #find class section    
                if str(clsSectContent) == 'None': #break from loop if there is no more class section
                    break
                else:
                    sectTitle = soup.find(id = sctTitleCode)     
                    sectTitle = sectTitle.contents[1]
                    sectTitle = sectTitle.replace(u'\xa0', '') #remove binary code from title  
                    getClsTitle = sectTitle.split(" " ,4)
                    if getClsTitle[1] == "CUNBA": #the format of subject CUNBA is different from other subjects
                        clsTitle = getClsTitle[0]
                    else:
                        cls_code = getClsTitle[1]
                        if cls_code == '':
                            clsTitle = getClsTitle[0] + " " + getClsTitle[2]
                        else:clsTitle = getClsTitle[0] + " " + getClsTitle[1]
                    for n in range (sctNumCounter,300): #some subject might have more than 200+ classes
                        clsNumCode = "MTG_CLASS_NBR$" + str(n) 
                        clsNum = clsSectContent.find(id = clsNumCode)   
                        if str(clsNum) == 'None':
                            break
                        else:
                            sectCode = "MTG_CLASSNAME$" + str(n)
                            rmCode = "MTG_ROOM$" + str(n)
                            profCode = "MTG_INSTR$" + str(n)
                            timeCode = "MTG_DAYTIME$" + str(n)
                            clsSect = clsSectContent.find(id = sectCode) #get class section
                            clsRm = clsSectContent.find(id = rmCode) #get class room
                            clsProf = clsSectContent.find(id = profCode) #get class instructor
                            clsTime = clsSectContent.find(id = timeCode) #get class time
                            sect_split = clsSect.contents[2].split("\n") #get splited class section
                                    
                            if getRating ==True:
                                rating = self.get_Rating(clsProf.contents[0])
                                write_file.write(clsTitle + "," + clsNum.contents[0] + "," + clsSect.contents[0] + "," + sect_split[1] + "," + clsTime.contents[0] + "," + clsRm.contents[0] + "," + clsProf.contents[0] + ","+ rating + "\n")
                            else:
                                write_file.write(clsTitle + "," + clsNum.contents[0] + "," + clsSect.contents[0] + "," + sect_split[1] + "," + clsTime.contents[0] + "," + clsRm.contents[0] + "," + clsProf.contents[0] + "\n")
                        sctNumCounter += 1
                        
            end = datetime.datetime.now() #get end time
            time_cost = (end - start).seconds #get time cost for loading each class data
            
            print("====Finished Loading " + sub + "====== " + str(sctNumCounter) + " Classes Found====Costed " + str(time_cost) + " secs======") 
            browser.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH').click()
        write_file.close()
    
    def logOut(self):
        browser.close()
