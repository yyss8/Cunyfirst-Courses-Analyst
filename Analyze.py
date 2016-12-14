"""

@author: Group B

"""
import matplotlib.pyplot as plt
from pylab import rcParams


class Rating(object):
    
    def __inti__ (self):
        pass
    
    def report(self,data):
        totalClass = 0
        totalDpt = {}
        instructorArray =[]
        for line in data:
            if line[6] != "Staff":
                instructorArray.append(line[6]) #get instructor number
            totalClass += 1
            dpt_split = line[0].split(" ")
            if dpt_split[0] not in totalDpt:
                avgDpt = []
                if line[7] != 'No Rating' and line[7] != " ":
                    avgDpt.append(1)
                    avgDpt.append(float(line[7]))                
                else:
                    avgDpt.append(0)
                    avgDpt.append(0)
                totalDpt[dpt_split[0]] = avgDpt
            else:
                try:
                    totalDpt[dpt_split[0]][0] += 1                    
                    totalDpt[dpt_split[0]][1] = (totalDpt[dpt_split[0]][1] + float(line[7]))
                except ValueError:
                    pass
        avgForSchool = 0
        dptCounter = 0
        print("")
        print("-----------------------------------------------------------------General Report-----------------------------------------------------------------")
        dpt_num = []
        avg_Dict = {}
        for dpt in totalDpt:
            dptCounter += 1
            dpt_num.append(totalDpt[dpt][0])
            if totalDpt[dpt][1] != 0:
                totalDpt[dpt][1] = totalDpt[dpt][1] / totalDpt[dpt][0]
                avgForSchool += totalDpt[dpt][1]
            else:
                avgForSchool += 0
            avg_Dict[dpt] = float(str(totalDpt[dpt][1])[0:4])
        avgForSchool = avgForSchool / dptCounter
        print("                                           Total Class:" + str(totalClass) + "          School Average: " + str(avgForSchool))
        print("                                           Total Department Number: "+ str(dptCounter))
        mostDpt = 0
        lessDpt = 0
        for dpt in totalDpt:
            if totalDpt[dpt][0] == max(dpt_num):
                mostDpt = dpt
            if totalDpt[dpt][0] == min(dpt_num):
                lessDpt = dpt
        print("                                           Department with most class: " + mostDpt + "       Department with least class: " + lessDpt)
        print("                                           Total Instructor Number: "+ str(len(set(instructorArray))))
        self.showPlot(avg_Dict,'Department','Average Rating',35,8)
        
    def ratingBetweenWdnWk(self,data):
        prof_dict = {}
        for line in data:
            if line[6] not in prof_dict:
                if 'Sa'in line[4] or 'Su' in line[4]:
                    prof_dict[line[6]] = [0,1,line[7]]
                elif line[4] != 'Staff':
                    prof_dict[line[6]] = [1,0,line[7]]
            else:
                if 'Sa'in line[4] or 'Su' in line[4]:
                    prof_dict[line[6]][1] +=1
                elif line[4] != 'Staff':
                    prof_dict[line[6]][0] +=1 
        
        wdProfs = {}
        wknProfs = {}
        for prof in prof_dict:
            if prof_dict[prof][0] >  prof_dict[prof][1]:
                wdProfs[prof] = prof_dict[prof][2]
            elif prof_dict[prof][0] <  prof_dict[prof][1]:
                wknProfs[prof] = prof_dict[prof][2]
        
        wknProfNum = []
        wdProfNum = []

        for prof in wdProfs:
            try:            
                wdProfNum.append(float(wdProfs[prof]))
            except ValueError: #fliter professor with no rating
                continue
        
        for prof in wknProfs:
            try:            
                wknProfNum.append(float(wknProfs[prof]))
            except ValueError: #fliter professor with no rating
                continue
                
        wdAvg = sum(wdProfNum) / len(wdProfNum)
        wknAvg = sum(wknProfNum) / len(wknProfNum)
        
        profDict = {'Weekday Instructor':wdAvg,
                    'Weekend Instructor':wknAvg}
        print("")
        print("        Total Weekday Instructor With Rating: " + str(len(wdProfNum))) 
        print("        Total Weekend Instructor With Rating: " + str(len(wknProfNum)))
        self.showPlot(profDict,'','Average Rating',5,4,xlim = False)
        
    def ratingByTmRange(self,data):
        time_dict = {'Morning':[0,0],
                     'Noon':[0,0],
                     'Evening':[0,0]}
        for line in data:
            if line[4] != 'TBA':
                try:
                    rating = float(line[7])
                    getTime = line[4].split(' ')
                    getTime = getTime[1].split(':')
                    getTime = int(getTime[0])
                    if getTime >= 7 and getTime <= 12:
                        time_dict['Morning'][0] += 1
                        time_dict['Morning'][1] += rating
                    elif getTime >= 12 and getTime <= 17:
                        time_dict['Noon'][0] += 1
                        time_dict['Noon'][1] += rating
                    elif getTime >= 17 and getTime <= 22:
                        time_dict['Evening'][0] += 1
                        time_dict['Evening'][1] += rating
                except ValueError: #fliter class with no rating
                    continue
        morningTotal = time_dict['Morning'][0]
        noonTotal = time_dict['Noon'][0]
        eveningTotal = time_dict['Evening'][0]
        timeDict = {'Morning':time_dict['Morning'][1] / morningTotal,
                     'Noon':time_dict['Noon'][1] / noonTotal,
                     'Evening':time_dict['Evening'][1] / eveningTotal}
       
        print("")
        print("        Total Morning Class With Rating: " + str(morningTotal)) 
        print("        Total Noon Class With Rating: " + str(noonTotal))             
        print("        Total Evening Class With Rating: " + str(eveningTotal))
        self.showPlot(timeDict,'Periods','Average Rating',5,5,xlim = False)
        print("")        
        print("       *Class Start Time")        
        print("        Morning class (7-12), Noon Class (12-17), Evening Class (17-22)")        
        
        
    def showPlot(self,dicts,xlabel,ylabel,w,h,xlim = None):
        rcParams['figure.figsize'] = w,h        
        fig, ax = plt.subplots() #i
        ax.set_xlabel(xlabel,fontsize=20)
        ax.set_ylabel(ylabel,fontsize=20)
        bar = plt.bar(range(len(dicts)), dicts.values(), align='center',facecolor='#9999ff')
        plt.xticks(range(len(dicts)), list(dicts.keys()))
        if xlim != False:
            plt.xlim([0,len(dicts)])  
        for subplot in bar:
            height = subplot.get_height()
            ax.text(subplot.get_x()+subplot.get_width()/2., height, '%.2f'%float(height),
                ha='center', va='bottom') #show subplot text
        plt.show()