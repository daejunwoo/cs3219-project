import rake
import operator

def extractKeyWords(description):
        keyWords = []
        text = "Experience with development on Android or iOS mobile platforms"
        stoppath = "cvStopList.txt"
        rake_object = rake.Rake(stoppath, 3, 4, 1)
        results = rake_object.run(description)
        
        resultsLen = len(results)
        for x in range(0,resultsLen):
                keyWords.append(results[x][0])

        
        
        return keyWords
    
    
