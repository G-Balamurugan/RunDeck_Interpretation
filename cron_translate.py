from cron_descriptor import get_description

# Generating Cron Format from Schedule Time  
def generateCron(minute , hour , monthDay , month , weekDay):
    return minute + " " + hour + " " + monthDay + " " + month + " " + weekDay

# Providing Description to Corn Format
# cronExpression example "0 1/3 1/1 * *"
def translateCronExpression(cron_expression):             
    description = get_description(cron_expression)
    return description

def extractServiceType(script):
    if script[:4] != "curl" or script.find("http://") == -1: return ""
    index = script.index("http://") + len("http://")
    dotIndex = script[index:].index(".")
    return script[index : index+dotIndex]

def serviceMapping(service):
    if service == "text-name-1": return "text1"
    elif service == "text-name-2": return "text2"
    elif service == "text-name-3": return "text3"
    elif service[:len('text-name-4')] == "text-name-4": return "text4"
    
# Extracting Necessary Details from Raw Input Json 
def extractDetails(inputJson):
    finalServiceJson = {}
    finalJson = {}
    for element in inputJson:
        serviceTypeList = set()
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
                serviceType = extractServiceType(tempDict["sequence"]["command"]["script"])
                if serviceType != "": serviceTypeList.add(serviceType)
                finalJson[element]["script"].append(tempDict["sequence"]["command"]["script"])
            if "errorhandler" in tempDict["sequence"]["command"]:
                if "script" in tempDict["sequence"]["command"]["errorhandler"]:
                    serviceType = extractServiceType(tempDict["sequence"]["command"]["errorhandler"]["script"])
                    if serviceType != "": serviceTypeList.add(serviceType)
                    finalJson[element]["errorScript"].append(tempDict["sequence"]["command"]["errorhandler"]["script"])
        else:       
            scriptList , errorScriptList = [] , []
            for scriptCurl in list(tempDict["sequence"]["command"]):
                if "script" in scriptCurl: 
                    serviceType = extractServiceType(scriptCurl["script"])
                    if serviceType != "": serviceTypeList.add(serviceType)
                    scriptList.append(scriptCurl["script"])
                if "errorhandler" in scriptCurl and "script" in scriptCurl["errorhandler"]:
                    serviceType = extractServiceType(scriptCurl["errorhandler"]["script"])
                    if serviceType != "": serviceTypeList.add(serviceType)
                    errorScriptList.append(scriptCurl["errorhandler"]["script"])
            finalJson[element]["script"] = scriptList
            finalJson[element]["errorScript"] = errorScriptList

        serviceList = []
        for service in serviceTypeList: serviceList.append(serviceMapping(service))
        finalJson[element]["curlCount"] = len(serviceList)
        finalJson[element]["curlList"] = list(serviceList)
        finalJson[element]["cron"] = generateCron(finalJson[element]["minute"], finalJson[element]["hour"], finalJson[element]["monthDay"],  finalJson[element]["month"], finalJson[element]["weekDay"])
        finalJson[element]["cronDescription"] = translateCronExpression(finalJson[element]["cron"])

        for serviceElement in serviceList:
            if serviceElement not in finalServiceJson:
                finalServiceJson[serviceElement] = { element : {} }
            finalServiceJson[serviceElement][element] = finalJson[element]
    
    return {
        "finalJson" : finalJson,
        "finalServiceJson" : finalServiceJson
    }
