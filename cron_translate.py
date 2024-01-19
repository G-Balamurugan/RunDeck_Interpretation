import json
from cron_descriptor import get_description

jsonFile = '/Users/balamurugan/Desktop/RunDeck/Json_File/final_json.json'

# Generating Cron Format from Schedule Time  
def generateCron(minute , hour , monthDay , month , weekDay):
    return minute + " " + hour + " " + monthDay + " " + month + " " + weekDay

# Providing Description to Corn Format
# cronExpression example "0 1/3 1/1 * *"
def translateCronExpression(cron_expression):             
    description = get_description(cron_expression)
    return description

# Extracting Necessary Details from Raw Input Json 
def extractDetails(inputJson):
    finalJson = {}
    for element in inputJson:
        tempDict = inputJson[element]["joblist"]["job"]
        
        finalJson[element] = {
            "jobName" : tempDict["name"],
            "jobId" : tempDict["id"],
            "jobDescription" : tempDict["description"],
            "logLevel" : tempDict["loglevel"],
            "executionEnabled" : tempDict["executionEnabled"],
            "timeOut" : tempDict["timeout"],
            "uuid" : tempDict["uuid"],
            "scheduleEnabled" : tempDict["scheduleEnabled"],
            "hour" : tempDict["schedule"]["time"]["@hour"],
            "minute" : tempDict["schedule"]["time"]["@minute"],
            "seconds" : tempDict["schedule"]["time"]["@seconds"]
        }
        
        if "month" in tempDict["schedule"]:
            finalJson[element]["month"] = tempDict["schedule"]["month"]["@month"]
            if "@day" in tempDict["schedule"]["month"]:
                finalJson[element]["monthDay"] = tempDict["schedule"]["month"]["@day"]
            else:
                finalJson[element]["monthDay"] = "*"
        else:
            finalJson[element]["month"] = "*"
            finalJson[element]["monthDay"] = "*"
        
        if "year" in tempDict["schedule"]:
            finalJson[element]["year"] = tempDict["schedule"]["year"]["@year"]
        else:
            finalJson[element]["year"] = "*"
        
        if "weekday" in tempDict["schedule"]:
            finalJson[element]["weekDay"] = tempDict["schedule"]["weekday"]["@day"]
        else:
            finalJson[element]["weekDay"] = "*"

        
        if(type(tempDict["sequence"]["command"]) == dict):
            finalJson[element]["script"] , finalJson[element]["errorScript"] = [] , []
            if "script" in tempDict["sequence"]["command"]:
                finalJson[element]["script"].append(tempDict["sequence"]["command"]["script"])
            if "errorhandler" in tempDict["sequence"]["command"]:
                if "script" in tempDict["sequence"]["command"]["errorhandler"]:
                    finalJson[element]["errorScript"].append(tempDict["sequence"]["command"]["errorhandler"]["script"])
        else:       
            scriptList , errorScriptList = [] , []
            for scriptCurl in list(tempDict["sequence"]["command"]):
                if "script" in scriptCurl: 
                    scriptList.append(scriptCurl["script"])
                if "errorhandler" in scriptCurl and "script" in scriptCurl["errorhandler"]:
                    errorScriptList.append(scriptCurl["errorhandler"]["script"])
            finalJson[element]["script"] = scriptList
            finalJson[element]["errorScript"] = errorScriptList

        finalJson[element]["cron"] = generateCron(finalJson[element]["minute"], finalJson[element]["hour"], finalJson[element]["monthDay"],  finalJson[element]["month"], finalJson[element]["weekDay"])
        finalJson[element]["cronDescription"] = translateCronExpression(finalJson[element]["cron"])

    finalJsonObject = json.dumps(finalJson,indent=4)
    with open(jsonFile, "w") as outfile:
        outfile.write(finalJsonObject)
    
    return finalJson