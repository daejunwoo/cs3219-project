import rake
import operator
import re
import string

def extractKeyWords(description):
        keyWords = []
        text = "Senior Software Engineer at Continental Automotive Group February 2008 - Present (7 years 9 months) Windows application developement "
        stoppath = "expStopList.txt"
        rake_object = rake.Rake(stoppath, 3, 3, 1)
        results = rake_object.run(description)
        print results
        resultsLen = len(results)
        for x in range(0,resultsLen):
                keyWords.append(results[x][0])
       
        
        return keyWords
    
def extract():

        #text = "Senior Software Engineer at Continental Automotive Group February 1991 - Present (7 years 9 months) Windows application developement "
        text ="Senior Software Engineer at ReQall Technologies PTE LTD March 2012 - Present (3 years 8 months)"
        date = extractDate(text)
        print extractDuration(text)
        #print extractPositionAndCompany(text,date)
        return


def extractDate(text):
        output ="date"
        #pattern = "(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}"
        pattern = "[January|February|March|April|May|June|July|August|September|October|November|December]+\s+\d{4}\s+[-]\s+[^\s]+"       
        expression = re.compile(pattern)
        matches = expression.findall(text)
        output = matches
        return output

def extractDuration(text):
        output =""
        duration = text[text.find("("):text.find(")")+1]
        output = text.replace(duration,"")
        #text[text.find("("):text.find(")")+1] = ""
        return duration

def extractPositionAndCompany(text,date):
        output =""
        position = text[0:text.find(" at ")]
        text = text.replace(position,"")
        company = text[text.find("at")+3:text.find(date[0])]
        return position,company

def extractExperience(text):
        date = ""
        duration = ""
        position = ""
        company = ""
        date = extractDate(text)
        if(len(date)>0):
                duration = extractDuration(text)
                position,company = extractPositionAndCompany(text,date)
        else:
                date =""
        
        return position,company,date,duration

def getExperience(text):
        detected = False
        tempDate = ""
        tempDuration = ""
        tempJob = ""
        tempCompany = ""
        for x in range(0, len(text)):
                if (detected==False):
                        output = text[x].split("Experience_")
                        if(len(output)>1):
                                detected = True
                                tempJob,tempCompany,tempDate,tempDuration = extractExperience(output[1])
                                if(len(tempJob)>0 and len(tempCompany)>0):
                                        print tempDate
                                        print tempDuration
                                        print tempJob
                                        print tempCompany
                                        x = x + 1
                                        tempJob,tempCompany,tempDate,tempDuration = extractExperience(text[x])
                                        if(len(tempJob)>0 and len(tempCompany)>0):
                                                x = x - 1
                                        else:
                                                extractKeyWords(text[x])
             
                else:
                        tempJob,tempCompany,tempDate,tempDuration = extractExperience(text[x])
                        if(len(tempJob)>0 and len(tempCompany)>0):
                                print tempDate
                                print tempDuration
                                print tempJob
                                print tempCompany
                                if(x< len(text) - 1):
                                        x = x + 1
                                        tempJob,tempCompany,tempDate,tempDuration = extractExperience(text[x])
                                        if(len(tempJob)>0 and len(tempCompany)>0):
                                                x = x - 1
                                        else:
                                                extractKeyWords(text[x])
        print "end"
