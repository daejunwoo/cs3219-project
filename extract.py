import rake
import operator
import re
import string

headerKey = ["Experience","Volunteer Experience","Projects","Languages","Certifications","Skills & Expertise","Education","Interests"]


def get_base(text):
    Name = getName(text)
    str = "'Name':" + Name
    return str

def volunteer_dec(func):
    def func_wrapper(text):
        table = getVolunteerExperience(text)
        str = ",\n'Volunteer':[\n"
        first = True
        #aggregate experience
        for row in table:
            if first:
                str = str + row
                first = False
            else:
                str = str + "\n," + row
        str = str + "]"
        prvStr = func(text)
        return prvStr + str
    return func_wrapper

def language_dec(func):
    def func_wrapper(text):
        table = getLanguage(text)
        str = ",\n'Language':[\n"
        #aggregate experience
        first = True
        for row in table:
            if first:
                str = str + row
                first = False
            else:
                str = str + "," + row
    
        str = str + "]"
        prvStr = func(text)
        return prvStr + str
    return func_wrapper

def experience_dec(func):
    def func_wrapper(text):
        table = getExperience(text)
        str = ",\n'Experience':[\n"
        first = True
        #aggregate experience
        for row in table:
            if first:
                str = str + row
                first = False
            else:
                str = str + "\n," + row
    
    #str = str + "{'title':coder,'company':nus}"
        str = str + "]"
        prvStr = func(text)
        return prvStr + str
    return func_wrapper

def testCVDecorator(text):
    temp = get_base

    dec = experience_dec
    temp = dec(temp)

    dec = language_dec
    temp = dec(temp)

    dec = volunteer_dec
    temp = dec(temp)

    print temp(text)

def detectStartEndLine(text,header):
    start = 0
    end = 0
    for y in range(0, len(text)):
        firstWord = text[y].split("_",1)
        if firstWord[0] == header:
            #print firstWord[0]
            start = y
            break

    for x in range(y+1, len(text)):
        firstWord = text[x].split("_",1)
        if firstWord[0] in headerKey:
            #print firstWord[0]
            end = x
            break
    if(end == 0):
        end = len(text)
    return start,end

def extractKeyWords(description):
        keyWords = []
        text = "Senior Software Engineer at Continental Automotive Group February 2008 - Present (7 years 9 months) Windows application developement "
        stoppath = "expStopList.txt"
        rake_object = rake.Rake(stoppath, 3, 3, 1)
        results = rake_object.run(description)
        #print results
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


def getName(text):
    Name = text[0].split("_",1)[0]
    return Name

def getVolunteerExperience(text):
    tempDate = ""
    tempDuration = ""
    tempJob = ""
    tempOrg = ""
    jobTable = []
    start,end = detectStartEndLine(text,"Volunteer Experience")
    output = text[start].split("Volunteer Experience_",1)
    
    #volunteer experience section found
    if(len(output)> 1):
        
        first = text[start].split("Volunteer Experience_",1)[1]
        tempJob,tempOrg,tempDate,tempDuration = extractExperience(first)
        if((start + 1) <= (end - start)):
            start = start + 1
            tempJob,tempOrg,tempDate,tempDuration = extractExperience(text[start])
            if(len(tempJob)>0 and len(tempOrg)>0):
                start = start - 1
            else:
                extractKeyWords(text[start])
    
        for x in range(start + 1, end):
            jobRow = ""
            tempJob,tempOrg,tempDate,tempDuration = extractExperience(text[x])
            if(len(tempJob)>0 and len(tempOrg)>0):
                jobRow = "{'Title:'" + tempJob + ","
                jobRow = jobRow + "'Org:'" + tempOrg + "}"
                jobTable.append(jobRow)
                if(x< end - 1):
                    x = x + 1
                    tempJob,tempOrg,tempDate,tempDuration = extractExperience(text[x])
                    if(len(tempJob)>0 and len(tempOrg)>0):
                        x = x - 1
                    else:
                        extractKeyWords(text[x])
    else:
        pass
    return jobTable

def getLanguage(text):
    languageTable = []
    start,end = detectStartEndLine(text,"Languages")
    raw = text[start].split("Languages_",1)[1]
    while(1):
        output = raw.split("_",1)
        if(len(output)>1):
            #print output[0]
            languageTable.append(output[0])
            raw = output[1]
        else:
            #print output[0]
            break
    return languageTable


def getExperience(text):
    tempDate = ""
    tempDuration = ""
    tempJob = ""
    tempCompany = ""
    jobTable = []
    
    start,end = detectStartEndLine(text,"Experience")
    first = text[start].split("Experience_",1)[1]
    tempJob,tempCompany,tempDate,tempDuration = extractExperience(first)
    #print tempJob
    #print tempCompany
    #print tempDate
    #print tempDuration
    
    if((start + 1) <= (end - start)):
        start = start + 1
        tempJob,tempCompany,tempDate,tempDuration = extractExperience(text[start])
        if(len(tempJob)>0 and len(tempCompany)>0):
            start = start - 1
        else:
            extractKeyWords(text[start])
            #append keywords to job
    
    for x in range(start + 1, end):
        jobRow = ""
        tempJob,tempCompany,tempDate,tempDuration = extractExperience(text[x])
        if(len(tempJob)>0 and len(tempCompany)>0):
            #print tempJob
            #print tempCompany
            #print tempDate
            #print tempDuration
            jobRow = "{'Title:'" + tempJob + ","
            jobRow = jobRow + "'Company:'" + tempCompany + "}"
            jobTable.append(jobRow)
            if(x< end - 1):
                x = x + 1
                tempJob,tempCompany,tempDate,tempDuration = extractExperience(text[x])
                if(len(tempJob)>0 and len(tempCompany)>0):
                    x = x - 1
                else:
                    extractKeyWords(text[x])

    return jobTable
